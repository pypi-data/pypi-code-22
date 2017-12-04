# coding: utf-8
from .default import Config


class ProductionConfig(Config):
    # Session config
    SESSION_COOKIE_NAME = 'modislock_session'

    # Site domain
    SITE_DOMAIN = "https://modislock.local"

    # Db config
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://modisweb:l3j4lkjlskjd@localhost/modislock"

    # Sentry
    SENTRY_DSN = ''

    # Minification
    MINIFY_PAGE = True

    # Assets
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True
