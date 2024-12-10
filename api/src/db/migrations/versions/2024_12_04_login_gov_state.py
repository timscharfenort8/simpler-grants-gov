"""login gov state

Revision ID: 6a23520d2c3c
Revises: 16eaca2334c9
Create Date: 2024-12-04 16:35:29.200758

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6a23520d2c3c"
down_revision = "16eaca2334c9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "login_gov_state",
        sa.Column("login_gov_state_id", sa.UUID(), nullable=False),
        sa.Column("nonce", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("login_gov_state_id", name=op.f("login_gov_state_pkey")),
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("login_gov_state", schema="api")
    # ### end Alembic commands ###