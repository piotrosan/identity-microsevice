"""Add group and role, user, and externallogin

Revision ID: c9c98ba4e6f2
Revises: 
Create Date: 2024-10-23 10:25:56.162641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c9c98ba4e6f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('age_range', postgresql.ENUM('young', 'teacher', 'master', name='agerange'), autoincrement=False, nullable=True),
    sa.Column('sector', postgresql.ENUM('it', 'construction', 'gastronomy', name='sector'), autoincrement=False, nullable=True),
    sa.Column('something_about_me', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('create_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user_group_role',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('app', postgresql.ENUM('flashcard', 'exercise', 'wisdom', name='appname'), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('create_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_group_role_pkey'),
    sa.UniqueConstraint('app', 'role', name='unique_constraint_app_role')
    )
    op.create_table('external_login',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gmail', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('facebook', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('create_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='external_login_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='external_login_pkey')
    )
    op.create_table('user_group',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', postgresql.ENUM('student', 'teacher', 'master', name='usergroupname'), autoincrement=False, nullable=True),
    sa.Column('create_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_group_pkey')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group')
    op.drop_table('external_login')
    op.drop_table('user_group_role')
    op.drop_table('user')
    # ### end Alembic commands ###
