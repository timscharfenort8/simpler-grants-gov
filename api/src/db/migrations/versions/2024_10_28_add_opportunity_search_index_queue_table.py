"""Add opportunity_search_index_queue table

Revision ID: a2e9144cdc6b
Revises: 39f7f941fc6c
Create Date: 2024-10-28 17:09:18.569197

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a2e9144cdc6b"
down_revision = "39f7f941fc6c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "opportunity_search_index_queue",
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("has_update", sa.Boolean(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("opportunity_search_index_queue_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint("opportunity_id", name=op.f("opportunity_search_index_queue_pkey")),
        schema="api",
    )
    op.create_index(
        op.f("opportunity_search_index_queue_opportunity_id_idx"),
        "opportunity_search_index_queue",
        ["opportunity_id"],
        unique=False,
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("opportunity_search_index_queue_opportunity_id_idx"),
        table_name="opportunity_search_index_queue",
        schema="api",
    )
    op.drop_table("opportunity_search_index_queue", schema="api")
    # ### end Alembic commands ###