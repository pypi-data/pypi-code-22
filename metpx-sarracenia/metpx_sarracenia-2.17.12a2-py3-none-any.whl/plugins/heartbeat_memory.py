#!/usr/bin/python3

"""
  default on_heartbeat handler that restarts program when detecting a memory leak... 
  Memory threshold is set to 10 x the program memory size after 100 files have been processed 
"""

class Heartbeat_Memory(object): 

    def __init__(self,parent):

        self.threshold  = 0

        # make parent know about these possible options

        parent.declare_option('heartbeat_memory_max')

          
    def perform(self,parent):
        import psutil
        self.logger = parent.logger

        # get set value

        if hasattr(parent,'heartbeat_memory_max'):
            if type(parent.heartbeat_memory_max) is list:
               maxstr = parent.heartbeat_memory_max[0]
            else:
               maxstr = parent.heartbeat_memory_max
            self.threshold  = parent.chunksize_from_str(maxstr)
            self.logger.info("memory threshold set to %d" % self.threshold)

        self.logger.debug("heartbeat_memory")

        if self.threshold == 0 and parent.message_count < 100 : return True

        # from doc memory_full_info()  # "real" USS memory usage (Linux, OSX, Win only)
        # mem(rss=10199040, vms=52133888, shared=3887104, text=2867200, lib=0,\
        #          data=5967872, dirty=0, uss=6545408, pss=6872064, swap=0)

        p = psutil.Process(parent.pid)
        mem = p.memory_info()

        if self.threshold == 0 :
           self.threshold = 10 * mem.vms
           self.logger.info("memory threshold set to %d" % self.threshold)
           return True

        if mem.vms > self.threshold : self.restart(parent)

        return True

    def restart(self,parent):
        import subprocess
        cmd = []
        cmd.append(parent.program_name)
        if parent.user_args and len(parent.user_args) > 0: cmd.extend(parent.user_args)
        if parent.user_config: cmd.append( parent.user_config )

        cmd.append('restart')

        parent.logger.info("leak detected")
        parent.logger.info("restarting with %s" % cmd)
        subprocess.check_call( cmd )

        return

heartbeat_memory  = Heartbeat_Memory(self)
self.on_heartbeat = heartbeat_memory.perform
