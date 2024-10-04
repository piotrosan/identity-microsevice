"""Added user table

Revision ID: e3fea17201fe
Revises: 
Create Date: 2024-10-04 12:30:35.894582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e3fea17201fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('external_login')
    op.drop_table('user')
    # ### end Alembic commands ###


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('age_range', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('sector', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('something_about_me', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('create_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    postgresql_ignore_search_path=False
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
    # ### end Alembic commands ###
