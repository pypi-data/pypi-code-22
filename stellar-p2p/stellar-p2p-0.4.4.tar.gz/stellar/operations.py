import click
import logging
import sqlalchemy_utils
from .cmd import (
    get_temp,
    remove_temp,
    dump_database,
    restore_database,
    apply_regex)
from urlparse import urlparse, parse_qs

logger = logging.getLogger(__name__)


SUPPORTED_DIALECTS = (
    'postgresql',
    'mysql'
)

class NotSupportedDatabase(Exception):
    pass


def get_engine_url(raw_conn, database):
    url = str(raw_conn.engine.url)
    if url.count('/') == 3 and url.endswith('/'):
        return '%s%s' % (url, database)
    else:
        if not url.endswith('/'):
            url += '/'
        return '%s/%s' % ('/'.join(url.split('/')[0:-2]), database)


def _get_pid_column(raw_conn):
    version = [int(x) for x in raw_conn.execute('SHOW server_version;').first()[0].split('.')]
    return 'pid' if version >= [9, 2] else 'procpid'


def terminate_database_connections(raw_conn, database):
    logger.debug('terminate_database_connections(%r)', database)
    if raw_conn.engine.dialect.name == 'postgresql':
        pid_column = _get_pid_column(raw_conn)

        raw_conn.execute(
            '''
                SELECT pg_terminate_backend(pg_stat_activity.%(pid_column)s)
                FROM pg_stat_activity
                WHERE
                    pg_stat_activity.datname = '%(database)s' AND
                    %(pid_column)s <> pg_backend_pid();
            ''' % {'pid_column': pid_column, 'database': database}
        )
    else:
        # NotYetImplemented
        pass


def create_database(raw_conn, database):
    logger.debug('create_database(%r)', database)
    return sqlalchemy_utils.functions.create_database(
        get_engine_url(raw_conn, database)
    )


def copy_database(raw_conn, from_database, to_database):
    logger.debug('copy_database(%r, %r)', from_database, to_database)
    terminate_database_connections(raw_conn, from_database)

    if raw_conn.engine.dialect.name == 'postgresql':
        raw_conn.execute(
            '''
                CREATE DATABASE "%s" WITH TEMPLATE "%s";
            ''' %
            (
                to_database,
                from_database
            )
        )
    elif raw_conn.engine.dialect.name == 'mysql':
        # Horribly slow implementation.
        create_database(raw_conn, to_database)
        for row in raw_conn.execute('SHOW TABLES in %s;' % from_database):
            raw_conn.execute('''
                CREATE TABLE %s.%s LIKE %s.%s
            ''' % (
                to_database,
                row[0],
                from_database,
                row[0]
            ))
            raw_conn.execute('ALTER TABLE %s.%s DISABLE KEYS' % (
                to_database,
                row[0]
            ))
            raw_conn.execute('''
                INSERT INTO %s.%s SELECT * FROM %s.%s
            ''' % (
                to_database,
                row[0],
                from_database,
                row[0]
            ))
            raw_conn.execute('ALTER TABLE %s.%s ENABLE KEYS' % (
                to_database,
                row[0]
            ))
    else:
        raise NotSupportedDatabase()


def database_exists(raw_conn, database):
    logger.debug('database_exists(%r)', database)
    return sqlalchemy_utils.functions.database_exists(
        get_engine_url(raw_conn, database)
    )


def remove_database(raw_conn, database):
    logger.debug('remove_database(%r)', database)
    terminate_database_connections(raw_conn, database)
    return sqlalchemy_utils.functions.drop_database(
        get_engine_url(raw_conn, database)
    )


def rename_database(raw_conn, from_database, to_database):
    logger.debug('rename_database(%r, %r)', from_database, to_database)
    terminate_database_connections(raw_conn, from_database)
    if raw_conn.engine.dialect.name == 'postgresql':
        raw_conn.execute(
            '''
                ALTER DATABASE "%s" RENAME TO "%s"
            ''' %
            (
                from_database,
                to_database
            )
        )
    elif raw_conn.engine.dialect.name == 'mysql':
        create_database(raw_conn, to_database)
        for row in raw_conn.execute('SHOW TABLES in %s;' % from_database):
            raw_conn.execute('''
                RENAME TABLE %s.%s TO %s.%s;
            ''' % (
                from_database,
                row[0],
                to_database,
                row[0]
            ))
        remove_database(raw_conn, from_database)
    else:
        raise NotSupportedDatabase()


def list_of_databases(raw_conn):
    logger.debug('list_of_databases()')
    if raw_conn.engine.dialect.name == 'postgresql':
        return [
            row[0]
            for row in raw_conn.execute('''
                SELECT datname FROM pg_database
                WHERE datistemplate = false
            ''')
        ]
    elif raw_conn.engine.dialect.name == 'mysql':
        return [
            row[0]
            for row in raw_conn.execute('''SHOW DATABASES''')
        ]
    else:
        raise NotSupportedDatabase()


def import_database(raw_conn, remote_url, from_database, local_url, to_database, regex=None):
    remote = {
        'username': urlparse(remote_url).username,
        'password': urlparse(remote_url).password,
        'hostname': urlparse(remote_url).hostname,
        'port': urlparse(remote_url).port
        }
    if not remote['username']:
            click.echo("Username missing from peer URL.")
            sys.exit(1)
    if not remote['password']:
            click.echo("Password missing from peer URL.")
            sys.exit(1)

    local = {
        'username': urlparse(local_url).username,
        'password': urlparse(local_url).password,
        'hostname': urlparse(local_url).hostname,
        'port': urlparse(local_url).port,
        }
    if not local['username']:
            click.echo("Username missing from local URL.")
            sys.exit(1)
    if not local['password']:
            click.echo("Password missing from local URL.")
            sys.exit(1)

    if raw_conn.engine.dialect.name == 'postgresql':
        tmp = get_temp()
        click.echo("Dumping from database %s to file %s." % (from_database, tmp))
        stdout,stderr = dump_database(
            remote['hostname'],
            remote['port'],
            from_database,
            remote['username'],
            remote['password'],
            tmp)
        # if stdout:
        #     click.echo('%s' % stdout)
        if stderr:
            click.echo('%s' % stderr)

        if regex:
            click.echo("Running regex on file %s." % tmp)
            stdout, stderr = apply_regex(tmp, regex)
            if stderr:
                click.echo('%s' % stderr)
            if stdout:
                click.echo('%s' % stdout)

        click.echo("Restoring to database %s from file %s." % (to_database, tmp))    
        sqlalchemy_utils.functions.create_database(
            get_engine_url(raw_conn, to_database))    
        stdout,stderr = restore_database(
            local['hostname'],
            local['port'],
            to_database,
            local['username'],
            local['password'],
            tmp)
        # if stdout:
        #     click.echo('%s' % stdout)
        if stderr:
            click.echo('%s' % stderr)
        remove_temp(tmp)
        click.echo("Temp file %s removed." % tmp)
    else:
        raise NotSupportedDatabase()                