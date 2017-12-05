"""Add audit table to DB schema

Revision ID: 1a69e5e5e2ac
Revises: 37e6b49fc686
Create Date: 2016-11-25 18:37:00.920703

"""

# revision identifiers, used by Alembic.
revision = '1a69e5e5e2ac'
down_revision = '37e6b49fc686'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        ### commands auto generated by Alembic - please adjust! ###
        op.create_table('pidea_audit',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('date', sa.DateTime(), nullable=True),
            sa.Column('signature', sa.String(length=620), nullable=True),
            sa.Column('action', sa.String(length=50), nullable=True),
            sa.Column('success', sa.Integer(), nullable=True),
            sa.Column('serial', sa.String(length=20), nullable=True),
            sa.Column('token_type', sa.String(length=12), nullable=True),
            sa.Column('user', sa.String(length=20), nullable=True),
            sa.Column('realm', sa.String(length=20), nullable=True),
            sa.Column('administrator', sa.String(length=20), nullable=True),
            sa.Column('action_detail', sa.String(length=50), nullable=True),
            sa.Column('info', sa.String(length=50), nullable=True),
            sa.Column('privacyidea_server', sa.String(length=255), nullable=True),
            sa.Column('client', sa.String(length=50), nullable=True),
            sa.Column('loglevel', sa.String(length=12), nullable=True),
            sa.Column('clearance_level', sa.String(length=12), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_pidea_audit_id'), 'pidea_audit', ['id'], unique=False)

    except Exception as exx:
        print ("pidea_audit table obviously already exists.")
        print (exx)


def downgrade():
    op.drop_index(op.f('ix_pidea_audit_id'), table_name='pidea_audit')
    op.drop_table('pidea_audit')
