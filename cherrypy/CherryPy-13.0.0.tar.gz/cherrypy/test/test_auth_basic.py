# This file is part of CherryPy <http://www.cherrypy.org/>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab:fileencoding=utf-8

from hashlib import md5

import cherrypy
from cherrypy._cpcompat import ntob
from cherrypy.lib import auth_basic
from cherrypy.test import helper


class BasicAuthTest(helper.CPWebCase):

    @staticmethod
    def setup_server():
        class Root:

            @cherrypy.expose
            def index(self):
                return 'This is public.'

        class BasicProtected:

            @cherrypy.expose
            def index(self):
                return "Hello %s, you've been authorized." % (
                    cherrypy.request.login)

        class BasicProtected2:

            @cherrypy.expose
            def index(self):
                return "Hello %s, you've been authorized." % (
                    cherrypy.request.login)

        userpassdict = {'xuser': 'xpassword'}
        userhashdict = {'xuser': md5(ntob('xpassword')).hexdigest()}

        def checkpasshash(realm, user, password):
            p = userhashdict.get(user)
            return p and p == md5(ntob(password)).hexdigest() or False

        basic_checkpassword_dict = auth_basic.checkpassword_dict(userpassdict)
        conf = {
            '/basic': {
                'tools.auth_basic.on': True,
                'tools.auth_basic.realm': 'wonderland',
                'tools.auth_basic.checkpassword': basic_checkpassword_dict
            },
            '/basic2': {
                'tools.auth_basic.on': True,
                'tools.auth_basic.realm': 'wonderland',
                'tools.auth_basic.checkpassword': checkpasshash
            },
        }

        root = Root()
        root.basic = BasicProtected()
        root.basic2 = BasicProtected2()
        cherrypy.tree.mount(root, config=conf)

    def testPublic(self):
        self.getPage('/')
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')
        self.assertBody('This is public.')

    def testBasic(self):
        self.getPage('/basic/')
        self.assertStatus(401)
        self.assertHeader('WWW-Authenticate', 'Basic realm="wonderland"')

        self.getPage('/basic/',
                     [('Authorization', 'Basic eHVzZXI6eHBhc3N3b3JX')])
        self.assertStatus(401)

        self.getPage('/basic/',
                     [('Authorization', 'Basic eHVzZXI6eHBhc3N3b3Jk')])
        self.assertStatus('200 OK')
        self.assertBody("Hello xuser, you've been authorized.")

    def testBasic2(self):
        self.getPage('/basic2/')
        self.assertStatus(401)
        self.assertHeader('WWW-Authenticate', 'Basic realm="wonderland"')

        self.getPage('/basic2/',
                     [('Authorization', 'Basic eHVzZXI6eHBhc3N3b3JX')])
        self.assertStatus(401)

        self.getPage('/basic2/',
                     [('Authorization', 'Basic eHVzZXI6eHBhc3N3b3Jk')])
        self.assertStatus('200 OK')
        self.assertBody("Hello xuser, you've been authorized.")
