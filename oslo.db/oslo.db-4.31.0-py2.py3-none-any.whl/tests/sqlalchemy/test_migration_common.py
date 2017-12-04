# Copyright 2013 Mirantis Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import os
import tempfile

from migrate import exceptions as migrate_exception
from migrate.versioning import api as versioning_api
import mock
import sqlalchemy

from oslo_db import exception as db_exception
from oslo_db.sqlalchemy import migration
from oslo_db.tests.sqlalchemy import base as test_base
from oslo_db.tests import utils as test_utils


class TestMigrationCommon(test_base.DbTestCase):
    def setUp(self):
        super(TestMigrationCommon, self).setUp()

        migration._REPOSITORY = None
        self.path = tempfile.mkdtemp('test_migration')
        self.path1 = tempfile.mkdtemp('test_migration')
        self.return_value = '/home/openstack/migrations'
        self.return_value1 = '/home/extension/migrations'
        self.init_version = 1
        self.test_version = 123

        self.patcher_repo = mock.patch.object(migration, 'Repository')
        self.repository = self.patcher_repo.start()
        self.repository.side_effect = [self.return_value, self.return_value1]

        self.mock_api_db = mock.patch.object(versioning_api, 'db_version')
        self.mock_api_db_version = self.mock_api_db.start()
        self.mock_api_db_version.return_value = self.test_version

    def tearDown(self):
        os.rmdir(self.path)
        self.mock_api_db.stop()
        self.patcher_repo.stop()
        super(TestMigrationCommon, self).tearDown()

    def test_find_migrate_repo_path_not_found(self):
        self.assertRaises(
            db_exception.DBMigrationError,
            migration._find_migrate_repo,
            "/foo/bar/",
        )
        self.assertIsNone(migration._REPOSITORY)

    def test_find_migrate_repo_called_once(self):
        my_repository = migration._find_migrate_repo(self.path)
        self.repository.assert_called_once_with(self.path)
        self.assertEqual(self.return_value, my_repository)

    def test_find_migrate_repo_called_few_times(self):
        repo1 = migration._find_migrate_repo(self.path)
        repo2 = migration._find_migrate_repo(self.path1)
        self.assertNotEqual(repo1, repo2)

    def test_db_version_control(self):
        with test_utils.nested(
            mock.patch.object(migration, '_find_migrate_repo'),
            mock.patch.object(versioning_api, 'version_control'),
        ) as (mock_find_repo, mock_version_control):
            mock_find_repo.return_value = self.return_value

            version = migration.db_version_control(
                self.engine, self.path, self.test_version)

            self.assertEqual(self.test_version, version)
            mock_version_control.assert_called_once_with(
                self.engine, self.return_value, self.test_version)

    @mock.patch.object(migration, '_find_migrate_repo')
    @mock.patch.object(versioning_api, 'version_control')
    def test_db_version_control_version_less_than_actual_version(
            self, mock_version_control, mock_find_repo):
        mock_find_repo.return_value = self.return_value
        mock_version_control.side_effect = (migrate_exception.
                                            DatabaseAlreadyControlledError)
        self.assertRaises(db_exception.DBMigrationError,
                          migration.db_version_control, self.engine,
                          self.path, self.test_version - 1)

    @mock.patch.object(migration, '_find_migrate_repo')
    @mock.patch.object(versioning_api, 'version_control')
    def test_db_version_control_version_greater_than_actual_version(
            self, mock_version_control, mock_find_repo):
        mock_find_repo.return_value = self.return_value
        mock_version_control.side_effect = (migrate_exception.
                                            InvalidVersionError)
        self.assertRaises(db_exception.DBMigrationError,
                          migration.db_version_control, self.engine,
                          self.path, self.test_version + 1)

    def test_db_version_return(self):
        ret_val = migration.db_version(self.engine, self.path,
                                       self.init_version)
        self.assertEqual(self.test_version, ret_val)

    def test_db_version_raise_not_controlled_error_first(self):
        with mock.patch.object(migration, 'db_version_control') as mock_ver:

            self.mock_api_db_version.side_effect = [
                migrate_exception.DatabaseNotControlledError('oups'),
                self.test_version]

            ret_val = migration.db_version(self.engine, self.path,
                                           self.init_version)
            self.assertEqual(self.test_version, ret_val)
            mock_ver.assert_called_once_with(self.engine, self.path,
                                             version=self.init_version)

    def test_db_version_raise_not_controlled_error_tables(self):
        with mock.patch.object(sqlalchemy, 'MetaData') as mock_meta:
            self.mock_api_db_version.side_effect = \
                migrate_exception.DatabaseNotControlledError('oups')
            my_meta = mock.MagicMock()
            my_meta.tables = {'a': 1, 'b': 2}
            mock_meta.return_value = my_meta

            self.assertRaises(
                db_exception.DBMigrationError, migration.db_version,
                self.engine, self.path, self.init_version)

    @mock.patch.object(versioning_api, 'version_control')
    def test_db_version_raise_not_controlled_error_no_tables(self, mock_vc):
        with mock.patch.object(sqlalchemy, 'MetaData') as mock_meta:
            self.mock_api_db_version.side_effect = (
                migrate_exception.DatabaseNotControlledError('oups'),
                self.init_version)
            my_meta = mock.MagicMock()
            my_meta.tables = {}
            mock_meta.return_value = my_meta
            migration.db_version(self.engine, self.path, self.init_version)

            mock_vc.assert_called_once_with(self.engine, self.return_value1,
                                            self.init_version)

    @mock.patch.object(versioning_api, 'version_control')
    def test_db_version_raise_not_controlled_alembic_tables(self, mock_vc):
        # When there are tables but the alembic control table
        # (alembic_version) is present, attempt to version the db.
        # This simulates the case where there is are multiple repos (different
        # abs_paths) and a different path has been versioned already.
        with mock.patch.object(sqlalchemy, 'MetaData') as mock_meta:
            self.mock_api_db_version.side_effect = [
                migrate_exception.DatabaseNotControlledError('oups'), None]
            my_meta = mock.MagicMock()
            my_meta.tables = {'alembic_version': 1, 'b': 2}
            mock_meta.return_value = my_meta

            migration.db_version(self.engine, self.path, self.init_version)

            mock_vc.assert_called_once_with(self.engine, self.return_value1,
                                            self.init_version)

    @mock.patch.object(versioning_api, 'version_control')
    def test_db_version_raise_not_controlled_migrate_tables(self, mock_vc):
        # When there are tables but the sqlalchemy-migrate control table
        # (migrate_version) is present, attempt to version the db.
        # This simulates the case where there is are multiple repos (different
        # abs_paths) and a different path has been versioned already.
        with mock.patch.object(sqlalchemy, 'MetaData') as mock_meta:
            self.mock_api_db_version.side_effect = [
                migrate_exception.DatabaseNotControlledError('oups'), None]
            my_meta = mock.MagicMock()
            my_meta.tables = {'migrate_version': 1, 'b': 2}
            mock_meta.return_value = my_meta

            migration.db_version(self.engine, self.path, self.init_version)

            mock_vc.assert_called_once_with(self.engine, self.return_value1,
                                            self.init_version)

    def test_db_sync_wrong_version(self):
        self.assertRaises(db_exception.DBMigrationError,
                          migration.db_sync, self.engine, self.path, 'foo')

    @mock.patch.object(versioning_api, 'upgrade')
    def test_db_sync_script_not_present(self, upgrade):
        # For non existent migration script file sqlalchemy-migrate will raise
        # VersionNotFoundError which will be wrapped in DBMigrationError.
        upgrade.side_effect = migrate_exception.VersionNotFoundError
        self.assertRaises(db_exception.DBMigrationError,
                          migration.db_sync, self.engine, self.path,
                          self.test_version + 1)

    @mock.patch.object(versioning_api, 'upgrade')
    def test_db_sync_known_error_raised(self, upgrade):
        upgrade.side_effect = migrate_exception.KnownError
        self.assertRaises(db_exception.DBMigrationError,
                          migration.db_sync, self.engine, self.path,
                          self.test_version + 1)

    def test_db_sync_upgrade(self):
        init_ver = 55
        with test_utils.nested(
            mock.patch.object(migration, '_find_migrate_repo'),
            mock.patch.object(versioning_api, 'upgrade')
        ) as (mock_find_repo, mock_upgrade):

            mock_find_repo.return_value = self.return_value
            self.mock_api_db_version.return_value = self.test_version - 1

            migration.db_sync(self.engine, self.path, self.test_version,
                              init_ver)

            mock_upgrade.assert_called_once_with(
                self.engine, self.return_value, self.test_version)

    def test_db_sync_downgrade(self):
        with test_utils.nested(
            mock.patch.object(migration, '_find_migrate_repo'),
            mock.patch.object(versioning_api, 'downgrade')
        ) as (mock_find_repo, mock_downgrade):

            mock_find_repo.return_value = self.return_value
            self.mock_api_db_version.return_value = self.test_version + 1

            migration.db_sync(self.engine, self.path, self.test_version)

            mock_downgrade.assert_called_once_with(
                self.engine, self.return_value, self.test_version)

    def test_db_sync_sanity_called(self):
        with test_utils.nested(
            mock.patch.object(migration, '_find_migrate_repo'),
            mock.patch.object(migration, '_db_schema_sanity_check'),
            mock.patch.object(versioning_api, 'downgrade')
        ) as (mock_find_repo, mock_sanity, mock_downgrade):

            mock_find_repo.return_value = self.return_value
            migration.db_sync(self.engine, self.path, self.test_version)

            self.assertEqual([mock.call(self.engine), mock.call(self.engine)],
                             mock_sanity.call_args_list)

    def test_db_sync_sanity_skipped(self):
        with test_utils.nested(
            mock.patch.object(migration, '_find_migrate_repo'),
            mock.patch.object(migration, '_db_schema_sanity_check'),
            mock.patch.object(versioning_api, 'downgrade')
        ) as (mock_find_repo, mock_sanity, mock_downgrade):

            mock_find_repo.return_value = self.return_value
            migration.db_sync(self.engine, self.path, self.test_version,
                              sanity_check=False)

            self.assertFalse(mock_sanity.called)

    def test_db_sanity_table_not_utf8(self):
        with mock.patch.object(self, 'engine') as mock_eng:
            type(mock_eng).name = mock.PropertyMock(return_value='mysql')
            mock_eng.execute.return_value = [['table_A', 'latin1'],
                                             ['table_B', 'latin1']]

            self.assertRaises(ValueError, migration._db_schema_sanity_check,
                              mock_eng)

    def test_db_sanity_table_not_utf8_exclude_migrate_tables(self):
        with mock.patch.object(self, 'engine') as mock_eng:
            type(mock_eng).name = mock.PropertyMock(return_value='mysql')
            # NOTE(morganfainberg): Check both lower and upper case versions
            # of the migration table names (validate case insensitivity in
            # the sanity check.
            mock_eng.execute.return_value = [['migrate_version', 'latin1'],
                                             ['alembic_version', 'latin1'],
                                             ['MIGRATE_VERSION', 'latin1'],
                                             ['ALEMBIC_VERSION', 'latin1']]

            migration._db_schema_sanity_check(mock_eng)
