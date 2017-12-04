#!/usr/bin/env python3
#
# This file is part of sarracenia.
# The sarracenia suite is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2008-2015
#
# Questions or bugs report: dps-client@ec.gc.ca
# sarracenia repository: git://git.code.sf.net/p/metpx/git
# Documentation: http://metpx.sourceforge.net/#SarraDocumentation
#
# sr_poll.py : python3 program allowing users to poll a remote server (destination)
#              browse directories and get a list of products of interest. Each product
#              is announced (AMQP) as ready to be downloaded.
#
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  Last Changed   : Dec 29 13:12:43 EST 2015
#
########################################################################
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#
#============================================================
# usage example
#
# sr_poll [options] [config] [foreground|start|stop|restart|reload|status|cleanup|setup]
#
# sr_poll connects to a destination. For each directory given, it lists its content
# and match the accept/reject products in that directory. Each file is announced and
# the list of announced product is kept.
#
# conditions:
#
# (polling)
# do_poll                 = a script supporting the protocol defined in the destination
# destination             = an url of the credentials of the remote server and its options (see credentials)
# directory               = one or more directories to browse
# accept/reject           = pattern matching what we want to poll in that directory
# do_line                 = a script reformatting the content of the list directory...
#                           (it is needed sometimes to takeaway useless or unstable fields)
# (messaging)
# post_broker             = where the message is announced... one specific user per poll source
# post_exchange           = xs_source_user
# post_base_url           = taken from the destination
# sum                     = 0   no sum computed... if we dont download the product
#                           x   if we download the product
# part                    = 1   file entirely downloaded (for now) ... find filesize from ls ?
# rename                  = which path under root, the file should appear
# source                  = None (fixed by sr_sarra)
# cluster                 = None (fixed by sr_sarra)
# to                      = message.headers['to_clusters'] MANDATORY
#
# option to only post... no download ... or only post
#============================================================

#

import os,sys,time

#============================================================
# DECLARE TRICK for false self.poster

from collections import *

#============================================================

try :    
         from sr_cache          import *
         from sr_file           import *
         from sr_ftp            import *
         from sr_http           import *
         from sr_message        import *
         from sr_post           import *
         from sr_util           import *
except : 
         from sarra.sr_cache     import *
         from sarra.sr_file      import *
         from sarra.sr_ftp       import *
         from sarra.sr_http      import *
         from sarra.sr_message   import *
         from sarra.sr_post      import *
         from sarra.sr_util      import *

class sr_poll(sr_post):

    def cd(self, path):
        try   :
                  self.dest.cd(path)
                  return True
        except :
                  self.logger.warning("Could not cd to directory %s" % path )
                  (stype, svalue, tb) = sys.exc_info()
                  self.logger.warning(" Type: %s, Value: %s" % (stype ,svalue))
        return False

    def check(self):

        if self.config_name == None : return

        # check destination

        self.details = None
        if self.destination != None :
           ok, self.details = self.credentials.get(self.destination)

        if self.destination == None or self.details == None :
           self.logger.error("destination option incorrect or missing\n")
           self.help()
           sys.exit(1)

        self.post_base_url = self.details.url.geturl()
        if self.post_base_url[-1] != '/' : self.post_base_url += '/'
        if self.post_base_url.startswith('file:'): self.post_base_url = 'file:'

        sr_post.check(self)

        self.sleeping      = False
        self.connected     = False 

        # rebuild mask as pulls instructions
        # pulls[directory] = [mask1,mask2...]

        self.pulls   = {}
        for mask in self.masks:
            pattern, maskDir, maskFileOption, mask_regexp, accepting = mask
            self.logger.debug(mask)
            if not maskDir in self.pulls :
               self.pulls[maskDir] = []
            self.pulls[maskDir].append(mask)

    # =============
    # default_poll
    # =============

    def default_poll(self):

        # instantiate according to the protocol

        url = self.details.url

        self.dest = None
        if url.scheme == 'file' : self.dest = sr_file(self)
        if url.scheme == 'ftp'  : self.dest = sr_ftp(self)
        if url.scheme == 'ftps' : self.dest = sr_ftp(self)

        if url.scheme == 'http' : self.dest = sr_http(self)

        if url.scheme == 'sftp' :
           try    : from sr_sftp       import sr_sftp
           except : from sarra.sr_sftp import sr_sftp
           self.dest = sr_sftp(self)

        # General Attributes

        self.ls          = {}
        self.lsold       = {}
        self.lspath      = ''
        self.pulllst     = []
        self.originalDir = ''
        self.destDir     = ''

        ok = self.post_new_urls()

        return ok

    # find differences between current ls and last ls
    # only the newer or modified files will be kept...

    def differ(self):

        # get new list and description
        new_lst  = []
        for k in self.ls.keys():
            new_lst.append(k)
        new_desc = self.ls
        new_lst.sort()

        # get old list and description
        self.load_ls_file(self.lspath)

        old_lst  = []
        for k in self.lsold.keys():
            old_lst.append(k)
        old_desc = self.lsold
        old_lst.sort()

        # compare

        filelst  = []
        desclst  = {}

        for f in new_lst :

            # keep a newer entry
            if not f in old_lst :
               filelst.append(f)
               desclst[f] = new_desc[f]
               continue

            # keep a modified entry
            if new_desc[f] != old_desc[f] :
               filelst.append(f)
               desclst[f] = new_desc[f]
               continue

        return filelst,desclst


    # check for pattern matching in directory name

    def dirPattern(self,path) :
        """
        Replace pattern in directory... 
        """

        ndestDir = ''

        DD = path.split("/")
        for  ddword in DD[1:] :
             ndestDir += '/'
             if ddword == "" : continue

             nddword = ""
             DW = ddword.split("$")
             for dwword in DW :
                 nddword += self.matchPattern(dwword,dwword)

             ndestDir += nddword

        return ndestDir

    # =============
    # __do_poll__
    # =============

    def __do_poll__(self):

        if self.do_poll :
           ok = self.do_poll(self)
           return ok

        ok = self.default_poll()
        return ok

    def help(self):
        print("Usage: %s [OPTIONS] configfile [foreground|start|stop|restart|reload|status|cleanup|setup]\n" % self.program_name )
        print("version: %s \n" % sarra.__version__ )
        print("\n\tPoll a remote server to produce announcements of new files appearing there\n" +
          "\npoll.conf file settings, MANDATORY ones must be set for a valid configuration:\n" +
          "\nAMQP broker settings:\n" +
          "\tpost_broker amqp{s}://<user>:<pw>@<brokerhost>[:port]/<vhost>\n" +
          "\t\t(default: amqp://anonymous:anonymous@dd.weather.gc.ca/ ) \n" +
          "\nAMQP Queue bindings:\n" +
          "\tpost_exchange      <name>         (default: xreport for feeders, xs_<user>)\n" +
          "\ttopic_prefix  <amqp pattern> (invariant prefix, currently v02.report)\n" +
          "\tsubtopic      <amqp pattern> (MANDATORY)\n" +
          "\t\t  <amqp pattern> = <directory>.<directory>.<directory>...\n" +
          "\t\t\t* single directory wildcard (matches one directory)\n" +
          "\t\t\t# wildcard (matches rest)\n" +
          "\nAMQP Queue settings:\n" +
          "\tdurable       <boolean>      (default: False)\n" +
          "\texpire        <minutes>      (default: None)\n" +
          "\tmessage-ttl   <minutes>      (default: None)\n" +
          "\tqueue_name    <name>         (default: program set it for you)\n" +
          "\nProcessing:\n" +
          "\tdo_line           <script>        (default None)\n" +
          "\tdo_poll           <script>        (default None)\n" +
          "\ton_post           <script>        (default None)\n" +
          "" )

  
        print("OPTIONS:")
        print("DEBUG:")
        print("-debug")

    def load_ls_file(self,path):
        self.lsold = {}

        if not os.path.isfile(path) : return True
        try : 
                file=open(path,'r')
                lines=file.readlines()
                file.close()

                for line in lines :
                    parts = line.split()
                    fil   = parts[-1]
                    self.lsold[fil] = line[:-1]

                return True

        except:
                self.logger.error("load_ls_file: Unable to parse files from %s" % path )

        return False

    def lsdir(self):
        try :
            self.ls = self.dest.ls()
            new_ls  = {}
            # apply selection on the list

            for f in self.ls :
                matched = False
                self.line = self.ls[f]

                ok = True
                if self.on_line_list : 
                    for plugin in self.on_line_list :
                        ok = plugin(self)
                        if not ok: break
      
                if ok:
                    if self.line[0] == 'd' :
                       self.logger.debug("directory %s skipped" % f)
                       continue

                    for mask in self.pulllst :
                       pattern, maskDir, maskFileOption, mask_regexp, accepting = mask
                       if mask_regexp.match(f):
                           if accepting:
                               matched=True
                               new_ls[f] = self.line
                           break

                # debug for developper
                #if matched:
                #    self.logger.debug("lsdir: accept line: %s" % self.line)
                #else:
                #    self.logger.debug("lsdir: rejected line: %s" % self.line)

            self.ls = new_ls
            return True
        except:
            (stype, svalue, tb) = sys.exc_info()
            self.logger.warning("dest.lsdir: Could not ls directory %s" % self.destDir)
            self.logger.warning(" Type: %s, Value: %s" % (stype ,svalue))

        return False

    def matchPattern(self,keywd,defval) :
        """
        Matching keyword with different patterns
        """
        if keywd[:6] == "{YYYY}"         : 
                                           return   time.strftime("%Y", time.gmtime()) + keywd[6:]

        if keywd[:9] == "{YYYY-1D}"      : 
                                           epoch  = time.mktime(time.gmtime()) - 24*60*60
                                           return   time.strftime("%Y", time.localtime(epoch) ) + keywd[9:]

        if keywd[:4] == "{MM}"           : 
                                           return   time.strftime("%m", time.gmtime()) + keywd[4:]

        if keywd[:7] == "{MM-1D}"        : 
                                           epoch  = time.mktime(time.gmtime()) - 24*60*60
                                           return   time.strftime("%m", time.localtime(epoch) ) + keywd[7:]

        if keywd[:5] == "{JJJ}"          : 
                                           return   time.strftime("%j", time.gmtime()) + keywd[5:]

        if keywd[:8] == "{JJJ-1D}"       : 
                                           epoch  = time.mktime(time.gmtime()) - 24*60*60
                                           return   time.strftime("%j", time.localtime(epoch) ) + keywd[8:]

        if keywd[:4] == "{HH}"           : 
                                           return   time.strftime("%H", time.gmtime()) + keywd[4:]


        if keywd[:10] == "{YYYYMMDD}"    : 
                                           return   time.strftime("%Y%m%d", time.gmtime()) + keywd[10:]

        if keywd[:13] == "{YYYYMMDD-1D}" :
                                           epoch  = time.mktime(time.gmtime()) - 24*60*60
                                           return   time.strftime("%Y%m%d", time.localtime(epoch) ) + keywd[13:]

        if keywd[:13] == "{YYYYMMDD-2D}" :
                                           epoch  = time.mktime(time.gmtime()) - 48*60*60
                                           return   time.strftime("%Y%m%d", time.localtime(epoch) ) + keywd[13:]

        if keywd[:13] == "{YYYYMMDD-3D}" :
                                           epoch  = time.mktime(time.gmtime()) - 72*60*60
                                           return   time.strftime("%Y%m%d", time.localtime(epoch) ) + keywd[13:]

        if keywd[:13] == "{YYYYMMDD-4D}" :
                                           epoch  = time.mktime(time.gmtime()) - 96*60*60
                                           return   time.strftime("%Y%m%d", time.localtime(epoch) ) + keywd[13:]

        if keywd[:13] == "{YYYYMMDD-5D}" : 
                                           epoch  = time.mktime(time.gmtime()) - 120*60*60
                                           return   time.strftime("%Y%m%d", time.localtime(epoch) ) + keywd[13:]

        return defval

    def overwrite_defaults(self):
        sr_post.overwrite_defaults(self)

        # Set minimum permissions to something that might work most of the time.
        self.chmod = 0o400

        # cache initialisation

        self.caching     = 1200

        # set parts to '1' so we always announce download the entire file

        self.parts       = '1'

        # need to compute checksum with d algo... in sarra

        self.sumflg      = 'z,d'

        self.accept_unmatch = False


    def post(self,post_exchange,post_base_url,post_relpath,to_clusters, \
                  partstr=None,sumstr=None,rename=None,mtime=None,atime=None,mode=None,link=None):

        self.msg.exchange = post_exchange
        
        self.msg.set_topic(self.topic_prefix,post_relpath)
        if self.subtopic != None : self.msg.set_topic_usr(self.topic_prefix,self.subtopic)

        self.msg.set_notice(post_base_url,post_relpath)

        # set message headers
        self.msg.headers = {}

        self.msg.headers['to_clusters'] = to_clusters

        if partstr  != None : self.msg.headers['parts']        = partstr
        if sumstr   != None : self.msg.headers['sum']          = sumstr
        if rename   != None : self.msg.headers['rename']       = rename
        if mtime    != None : self.msg.headers['mtime']        = mtime
        if atime    != None : self.msg.headers['atime']        = atime
        if mode     != None : self.msg.headers['mode']         = "%o" % ( mode & 0o7777 )
        if link     != None : self.msg.headers['link']         = link

        if self.cluster != None : self.msg.headers['from_cluster'] = self.cluster
        if self.source  != None : self.msg.headers['source']       = self.source

        # ========================================
        # cache testing
        # ========================================

        if not self.cache.check(sumstr,post_relpath,partstr):
            self.logger.debug("Ignored %s" % (self.msg.notice))
            return False

        self.logger.debug("Added %s" % (self.msg.notice))

        self.msg.trim_headers()

        ok = self.__on_post__()

        return ok

    # =============
    # for all directories, get urls to post
    # if True is returned it means : no sleep, retry on return
    # False means, go to sleep and retry after sleep seconds
    # =============

    def post_new_urls(self):

        # number of post files

        npost = 0

        # connection did not work

        try:
             self.dest.connect()
        except:
            (stype, svalue, tb) = sys.exc_info()
            self.logger.warning(" Type: %s, Value: %s" % (stype ,svalue))
            self.logger.error("Unable to connect to %s. Type: %s, Value: %s" % (self.destination, stype ,svalue))
            self.logger.error("Sleeping 30 secs and retry")
            time.sleep(30)
            return True

        # loop on all directories where there are pulls to do

        for destDir in self.pulls :

            self.destDir = destDir
            self.pulllst = self.pulls[destDir]

            pdir = self.dirPattern(self.destDir)
            if pdir != '' : self.destDir = pdir
            #self.destDir = self.destDir[1:]

            # cd to that directory

            self.logger.debug(" cd %s" % self.destDir)
            ok = self.cd(self.destDir)
            if not ok : continue

            # create ls filename for that directory

            pdir = destDir
            pdir = pdir.replace('${','')
            pdir = pdir.replace('}','')
            pdir = pdir.replace('/','_')

            self.lspath = self.user_cache_dir + os.sep + 'ls' + pdir

            # ls that directory

            ok = self.lsdir()
            if not ok : continue

            #self.logger.debug("post_new_urls: back from lsdir ok sleeping=%s #files: %d" % ( self.sleeping, len(self.ls.keys())) )

            # if we are sleeping and we are here it is because
            # this pull is retrieving difference between directory content
            # so write the directory content without retrieving files

            if self.sleeping :
               ok = self.write_ls_file(self.lspath)
               continue

            #self.logger.debug("post_new_urls: not sleeping " )

            # get the file list from the ls
            
            filelst = []
            for k in self.ls.keys():
                filelst.append(k)
            desclst = self.ls

            # get file list from difference in ls

            filelst,desclst = self.differ()
            self.logger.debug("post_new_urls: after differ, len=%d" % len(filelst) )

            if len(filelst) == 0 :
               ok = self.write_ls_file(self.lspath)
               continue

            # for all files make a post
            for idx,remote_file in enumerate(filelst) :

                FileOption = None
                for mask in self.pulllst :
                    pattern, maskDir, maskFileOption, mask_regexp, accepting = mask
                    if mask_regexp.match(remote_file) and accepting :
                       FileOption = maskFileOption

                path = self.destDir + '/'+ remote_file

                # posting a localfile
                if self.post_base_url.startswith('file:') :
                   if os.path.isfile(path)   :
                      try   : lstat = os.stat(path)
                      except: lstat = None
                      ok    = self.post1file(path,lstat)
                      if ok : npost += 1
                      continue

                self.post_relpath = self.destDir + '/'+ remote_file

                desc         = desclst[remote_file]
                ssiz         = desc.split()[4]

                self.sumstr  = self.sumflg
                self.partstr = None

                try :
                        isiz = int(ssiz)
                        self.partstr = '1,%d,1,0,0' % isiz
                except: pass

                this_rename  = self.rename

                # FIX ME generalized fileOption
                if FileOption != None :
                   parts = FileOption.split('=')
                   option = parts[0].strip()
                   if option == 'rename' and len(parts) == 2 : 
                      this_rename = parts[1].strip()

                if this_rename != None and this_rename[-1] == '/' :
                   this_rename += remote_file
                
                ok = self.post(self.post_exchange,self.post_base_url,self.post_relpath,self.to_clusters, \
                               self.partstr,self.sumstr,this_rename)

                if ok : npost += 1


            ok = self.write_ls_file(self.lspath)

        # close connection

        try   : self.dest.close()
        except: pass

        #dev logging
        #if self.sleeping:
        #   self.logger.info("oh! we are sleeping...")

        return npost > 0


    # write ls file

    def write_ls_file(self,path):

        filelst = []
        for k in self.ls.keys():
            filelst.append(k)
        desclst = self.ls
        filelst.sort()

        try : 
                fp=open(path,'w')
                for f in filelst :
                    fp.write(desclst[f]+'\n')
                fp.close()

                return True

        except:
                self.logger.error("Unable to write ls to file %s" % path )

        return False

    def run(self):

        self.logger.info("sr_poll run")

        # connect to broker

        self.connect()

        # do pulls instructions

        if self.vip : last = self.has_vip()

        while True :

              #  heartbeat (may be used to check if program is alive if not "has_vip")
              ok = self.heartbeat_check()

              # if vip provided, check if has vip
              if self.vip :
                 self.sleeping = not self.has_vip()

                 #  sleeping
                 if self.sleeping:
                    if not last: self.logger.info("%s is sleeping without vip=%s"% (self.program_name,self.vip))
                 #  active
                 else:
                    if last:     self.logger.info("%s is active on vip=%s"%        (self.program_name,self.vip))

                 last  = self.sleeping

              if not self.sleeping: self.logger.debug("poll %s is waking up" % self.config_name )

              # if pull is sleeping and we delete files... nothing to do
              # if we don't delete files, we will keep the directory state

              ok = False

              try  :
                      #  get a list of url to post
                      ok = self.__do_poll__()

              except:
                      (stype, svalue, tb) = sys.exc_info()
                      self.logger.error("Type: %s, Value: %s,  ..." % (stype, svalue))

              self.logger.debug("poll is sleeping %d seconds " % self.sleep)
              time.sleep(self.sleep)

# ===================================
# MAIN
# ===================================

def main():

    args,action,config,old = startup_args(sys.argv)

    poll = sr_poll(config,args,action)
    poll.exec_action(action,old)

    os._exit(0)

# =========================================
# direct invocation
# =========================================

if __name__=="__main__":
   main()
