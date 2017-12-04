import logging
import os
import sys
import click
from functools import partial

from .config import load_config
from .models import Snapshot, Peer, Table, Base
from .operations import (
    copy_database,
    create_database,
    database_exists,
    remove_database,
    rename_database,
    terminate_database_connections,
    list_of_databases,
    import_database
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from psutil import pid_exists


__version__ = '0.4.4'
logger = logging.getLogger(__name__)


class Operations(object):
    def __init__(self, raw_connection, config):
        self.terminate_database_connections = partial(
            terminate_database_connections, raw_connection
        )
        self.create_database = partial(create_database, raw_connection)
        self.copy_database = partial(copy_database, raw_connection)
        self.database_exists = partial(database_exists, raw_connection)
        self.rename_database = partial(rename_database, raw_connection)
        self.remove_database = partial(remove_database, raw_connection)
        self.list_of_databases = partial(list_of_databases, raw_connection)
        self.import_database = partial(import_database, raw_connection)

class Stellar(object):
    def __init__(self):
        logger.debug('Initialized Stellar()')
        self.load_config()
        self.init_database()

    def load_config(self):
        self.config = load_config()
        logging.basicConfig(level=self.config['logging'])

    def init_database(self):
        self.raw_db = create_engine(self.config['url'], echo=False)
        self.raw_conn = self.raw_db.connect()
        self.operations = Operations(self.raw_conn, self.config)

        try:
            self.raw_conn.connection.set_isolation_level(0)
        except AttributeError:
            logger.info('Could not set isolation level to 0')

        self.db = create_engine(self.config['stellar_url'], echo=False)
        self.db.session = sessionmaker(bind=self.db)()
        self.raw_db.session = sessionmaker(bind=self.raw_db)()
        tables_missing = self.create_stellar_database()

        self.create_stellar_tables()

        # logger.getLogger('sqlalchemy.engine').setLevel(logger.WARN)


    def init_remote_database(self, peer_url):
        self.remote_raw_db = create_engine(peer_url, echo=False)
        self.remote_raw_conn = self.remote_raw_db.connect()
        self.remote_operations = Operations(self.remote_raw_conn, self.config)

        try:
            self.remote_raw_conn.connection.set_isolation_level(0)
        except AttributeError:
            logger.info('Could not set isolation level to 0 on remote peer')

        self.remote_db = create_engine(peer_url, echo=False)
        self.remote_db.session = sessionmaker(bind=self.remote_db)()
        self.remote_raw_db.session = sessionmaker(bind=self.remote_raw_db)()
        tables_missing = self.create_stellar_database()

        self.create_stellar_tables()


    def create_stellar_database(self):
        if not self.operations.database_exists('stellar_data'):
            self.operations.create_database('stellar_data')
            return True
        else:
            return False

    def create_stellar_tables(self):
        Base.metadata.create_all(self.db)
        self.db.session.commit()

    def get_peer(self, peer_name):
        try:
            peer = self.db.session.query(Peer).filter(
                Peer.peer_name == peer_name,
                ).first()
        except:
            click.echo('Fetching peer "%s" failed.' % name)
            exit(1)
        return peer


    def get_peers(self):
        return self.db.session.query(Peer).all()

    def create_peer(self, peer_name, url, regex):
        if self.get_peer(peer_name):
            click.echo("Peer (%s) already exists." % peer_name)
            sys.exit(1)
        peer = Peer(
            peer_name=peer_name,
            url=url,
            regex=regex
        )
        self.db.session.add(peer)
        self.db.session.flush()
        self.db.session.commit()

    def remove_peer(self, peer):
        if not self.get_peer(peer_name):
            click.echo("Peer (%s) does not exist." % peer_name)
            sys.exit(1)
        self.db.session.delete(peer)
        self.db.session.commit()

    def get_remote_snapshots(self, peer_name):
        if not self.get_peer(peer_name):
            click.echo("Peer (%s) does not exist." % peer_name)
            sys.exit(1)

        peer_url = self.db.session.query(Peer).filter(Peer.peer_name == peer_name,).first().url
        self.init_remote_database(peer_url)

        return self.remote_db.session.query(Snapshot).filter(
            Snapshot.project_name == self.config['project_name']
        ).order_by(
            Snapshot.created_at.desc()
        ).all()

    def get_remote_snapshot(self, peer_name, snapshot_name):
        if not self.get_peer(peer_name):
            click.echo("Peer (%s) does not exist." % peer_name)
            sys.exit(1)

        peer_url = self.db.session.query(Peer).filter(Peer.peer_name == peer_name,).first().url
        self.init_remote_database(peer_url)

        return self.remote_db.session.query(Snapshot).filter(
            Snapshot.snapshot_name == snapshot_name,
            Snapshot.project_name == self.config['project_name']
        ).first()

    def import_remote_snapshot(self, peer_name, remote_snapshot, before_copy=None):
        if not self.get_peer(peer_name):
            click.echo("Peer (%s) does not exist." % peer_name)
            sys.exit(1)

        if not remote_snapshot:
            click.echo("An error occured! Snapshot %s is not valid." % remote_snapshot)
            sys.exit(1)

        remote_url = self.db.session.query(Peer).filter(Peer.peer_name == peer_name,).first().url
        sed_regex = self.db.session.query(Peer).filter(Peer.peer_name == peer_name,).first().regex
        local_url = self.config['url']
        snapshot = Snapshot(
            snapshot_name = remote_snapshot.snapshot_name,
            project_name = remote_snapshot.project_name,
            hash = remote_snapshot.hash,
            created_at = remote_snapshot.created_at
        )

        click.echo("Importing snapshot %s" % remote_snapshot.snapshot_name)
        for table in remote_snapshot.tables:
            if not self.remote_operations.database_exists(
                table.get_table_name('slave')
            ):
                click.echo(
                    "Database %s does not exist."
                    % table.get_table_name('slave')
                )
                sys.exit(1)
            try:
                self.operations.import_database(
                    remote_url,
                    table.get_table_name('slave'),
                    local_url,
                    table.get_table_name('slave'),
                    sed_regex
                    )
            except ProgrammingError:
                logger.warn('Database %s does not exist.' % table.get_table_name('slave'))
           
            if not self.operations.database_exists(
                table.get_table_name('slave')
            ):
                click.echo(
                    "Database import failed for %s."
                    % table.get_table_name('slave')
                )
                sys.exit(1)

            if self.operations.database_exists(
                table.get_table_name('master')
            ):
                self.operations.remove_database(
                    table.get_table_name('master')
                )
            self.operations.rename_database(
                table.get_table_name('slave'),
                table.get_table_name('master')
            )     

        self.db.session.add(snapshot)
        self.db.session.commit()
        self.inline_slave_copy(snapshot)
        click.echo("Done.")

    def get_snapshot(self, snapshot_name):
        return self.db.session.query(Snapshot).filter(
            Snapshot.snapshot_name == snapshot_name,
            Snapshot.project_name == self.config['project_name']
        ).first()

    def get_snapshots(self):
        return self.db.session.query(Snapshot).filter(
            Snapshot.project_name == self.config['project_name']
        ).order_by(
            Snapshot.created_at.desc()
        ).all()

    def get_latest_snapshot(self):
        return self.db.session.query(Snapshot).filter(
            Snapshot.project_name == self.config['project_name']
        ).order_by(Snapshot.created_at.desc()).first()

    def create_snapshot(self, snapshot_name, before_copy=None):
        snapshot = Snapshot(
            snapshot_name=snapshot_name,
            project_name=self.config['project_name']
        )
        self.db.session.add(snapshot)
        self.db.session.flush()

        for table_name in self.config['tracked_databases']:
            if before_copy:
                before_copy(table_name)
            table = Table(
                table_name=table_name,
                snapshot=snapshot
            )
            logger.debug('Copying %s to %s' % (
                table_name,
                table.get_table_name('master')
            ))
            self.operations.copy_database(
                table_name,
                table.get_table_name('master')
            )
            self.db.session.add(table)
        self.db.session.commit()

        self.start_background_slave_copy(snapshot)

    def remove_snapshot(self, snapshot):
        for table in snapshot.tables:
            try:
                self.operations.remove_database(
                    table.get_table_name('master')
                )
            except ProgrammingError:
                pass
            try:
                self.operations.remove_database(
                    table.get_table_name('slave')
                )
            except ProgrammingError:
                pass
            self.db.session.delete(table)
        self.db.session.delete(snapshot)
        self.db.session.commit()

    def rename_snapshot(self, snapshot, new_name):
        snapshot.snapshot_name = new_name
        self.db.session.commit()

    def restore(self, snapshot):
        for table in snapshot.tables:
            click.echo("Restoring database %s" % table.table_name)
            if not self.operations.database_exists(
                table.get_table_name('slave')
            ):
                click.echo(
                    "Database %s does not exist."
                    % table.get_table_name('slave')
                )
                sys.exit(1)
            try:
                self.operations.remove_database(table.table_name)
            except ProgrammingError:
                logger.warn('Database %s does not exist.' % table.table_name)
            self.operations.rename_database(
                table.get_table_name('slave'),
                table.table_name
            )
        snapshot.worker_pid = 1
        self.db.session.commit()

        self.start_background_slave_copy(snapshot)

    def start_background_slave_copy(self, snapshot):
        logger.debug('Starting background slave copy')
        snapshot_id = snapshot.id

        self.raw_conn.close()
        self.raw_db.session.close()
        self.db.session.close()

        pid = os.fork() if hasattr(os, 'fork') else None
        if pid:
            return

        self.init_database()
        self.operations = Operations(self.raw_conn, self.config)

        snapshot = self.db.session.query(Snapshot).get(snapshot_id)
        snapshot.worker_pid = os.getpid()
        self.db.session.commit()
        self.inline_slave_copy(snapshot)
        sys.exit()

    def inline_slave_copy(self, snapshot):
        for table in snapshot.tables:
            self.operations.copy_database(
                table.get_table_name('master'),
                table.get_table_name('slave')
            )
        snapshot.worker_pid = None
        self.db.session.commit()

    def is_copy_process_running(self, snapshot):
        return pid_exists(snapshot.worker_pid)

    def is_old_database(self):
        for snapshot in self.db.session.query(Snapshot):
            for table in snapshot.tables:
                for postfix in ('master', 'slave'):
                    old_name = table.get_table_name(postfix=postfix, old=True)
                    if self.operations.database_exists(old_name):
                        return True
        return False

    def update_database_names_to_new_version(self, after_rename=None):
        for snapshot in self.db.session.query(Snapshot):
            for table in snapshot.tables:
                for postfix in ('master', 'slave'):
                    old_name = table.get_table_name(postfix=postfix, old=True)
                    new_name = table.get_table_name(postfix=postfix, old=False)
                    if self.operations.database_exists(old_name):
                        self.operations.rename_database(old_name, new_name)
                        if after_rename:
                            after_rename(old_name, new_name)

    def delete_orphan_snapshots(self, after_delete=None):
        stellar_databases = set()
        for snapshot in self.db.session.query(Snapshot):
            for table in snapshot.tables:
                stellar_databases.add(table.get_table_name('master'))
                stellar_databases.add(table.get_table_name('slave'))

        databases = set(self.operations.list_of_databases())

        for database in filter(
            lambda database: (
                database.startswith('stellar_') and
                database != 'stellar_data'
            ),
            (databases-stellar_databases)
        ):
            self.operations.remove_database(database)
            if after_delete:
                after_delete(database)

    @property
    def default_snapshot_name(self):
        n = 1
        while self.db.session.query(Snapshot).filter(
            Snapshot.snapshot_name == 'snap%d' % n,
            Snapshot.project_name == self.config['project_name']
        ).count():
            n += 1
        return 'snap%d' % n
