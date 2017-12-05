# All Rights Reserved.
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

"""fill_missed_workload_info

Absorbed by fab4f4f31f8a_fill_missed_workload_info

Revision ID: c517b0011857
Revises: 35fe16d4ab1c
Create Date: 2017-06-22 18:46:09.281312

"""

from rally import exceptions

# revision identifiers, used by Alembic.
revision = "c517b0011857"
down_revision = "35fe16d4ab1c"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    raise exceptions.DowngradeNotSupported()
