"""Updates for summary tables

Revision ID: 578c80acb29c
Revises: ac80e949bcf8
Create Date: 2024-03-07 10:44:08.694002

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "578c80acb29c"
down_revision = "ac80e949bcf8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "opportunity",
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_number", sa.Text(), nullable=True),
        sa.Column("opportunity_title", sa.Text(), nullable=True),
        sa.Column("agency", sa.Text(), nullable=True),
        sa.Column("opportunity_category_id", sa.Integer(), nullable=True),
        sa.Column("category_explanation", sa.Text(), nullable=True),
        sa.Column("is_draft", sa.Boolean(), nullable=False),
        sa.Column("revision_number", sa.Text(), nullable=True),
        sa.Column("modified_comments", sa.Text(), nullable=True),
        sa.Column("publisher_user_id", sa.Text(), nullable=True),
        sa.Column("publisher_profile_id", sa.BigInteger(), nullable=True),
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
            ["opportunity_category_id"],
            ["lk_opportunity_category.opportunity_category_id"],
            name=op.f("opportunity_opportunity_category_id_lk_opportunity_category_fkey"),
        ),
        sa.PrimaryKeyConstraint("opportunity_id", name=op.f("opportunity_pkey")),
    )
    op.create_index(op.f("opportunity_is_draft_idx"), "opportunity", ["is_draft"], unique=False)
    op.create_index(
        op.f("opportunity_opportunity_category_id_idx"),
        "opportunity",
        ["opportunity_category_id"],
        unique=False,
    )
    op.create_index(
        op.f("opportunity_opportunity_title_idx"),
        "opportunity",
        ["opportunity_title"],
        unique=False,
    )
    op.create_table(
        "opportunity_assistance_listing",
        sa.Column("opportunity_assistance_listing_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("assistance_listing_number", sa.Text(), nullable=True),
        sa.Column("program_title", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["opportunity.opportunity_id"],
            name=op.f("opportunity_assistance_listing_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_assistance_listing_id", name=op.f("opportunity_assistance_listing_pkey")
        ),
    )
    op.create_index(
        op.f("opportunity_assistance_listing_opportunity_id_idx"),
        "opportunity_assistance_listing",
        ["opportunity_id"],
        unique=False,
    )
    op.create_table(
        "opportunity_summary",
        sa.Column("opportunity_summary_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("summary_description", sa.Text(), nullable=True),
        sa.Column("is_cost_sharing", sa.Boolean(), nullable=True),
        sa.Column("is_forecast", sa.Boolean(), nullable=False),
        sa.Column("post_date", sa.Date(), nullable=True),
        sa.Column("close_date", sa.Date(), nullable=True),
        sa.Column("close_date_description", sa.Text(), nullable=True),
        sa.Column("archive_date", sa.Date(), nullable=True),
        sa.Column("unarchive_date", sa.Date(), nullable=True),
        sa.Column("expected_number_of_awards", sa.Integer(), nullable=True),
        sa.Column("estimated_total_program_funding", sa.BigInteger(), nullable=True),
        sa.Column("award_floor", sa.BigInteger(), nullable=True),
        sa.Column("award_ceiling", sa.BigInteger(), nullable=True),
        sa.Column("additional_info_url", sa.Text(), nullable=True),
        sa.Column("additional_info_url_description", sa.Text(), nullable=True),
        sa.Column("forecasted_post_date", sa.Date(), nullable=True),
        sa.Column("forecasted_close_date", sa.Date(), nullable=True),
        sa.Column("forecasted_close_date_description", sa.Text(), nullable=True),
        sa.Column("forecasted_award_date", sa.Date(), nullable=True),
        sa.Column("forecasted_project_start_date", sa.Date(), nullable=True),
        sa.Column("fiscal_year", sa.Integer(), nullable=True),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column("modification_comments", sa.Text(), nullable=True),
        sa.Column("funding_category_description", sa.Text(), nullable=True),
        sa.Column("applicant_eligibility_description", sa.Text(), nullable=True),
        sa.Column("agency_code", sa.Text(), nullable=True),
        sa.Column("agency_name", sa.Text(), nullable=True),
        sa.Column("agency_phone_number", sa.Text(), nullable=True),
        sa.Column("agency_contact_description", sa.Text(), nullable=True),
        sa.Column("agency_email_address", sa.Text(), nullable=True),
        sa.Column("agency_email_address_description", sa.Text(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("can_send_mail", sa.Boolean(), nullable=True),
        sa.Column("publisher_profile_id", sa.BigInteger(), nullable=True),
        sa.Column("publisher_user_id", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["opportunity.opportunity_id"],
            name=op.f("opportunity_summary_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint("opportunity_summary_id", name=op.f("opportunity_summary_pkey")),
    )
    op.create_table(
        "current_opportunity_summary",
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_summary_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_status_id", sa.Integer(), nullable=False),
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
            ["opportunity.opportunity_id"],
            name=op.f("current_opportunity_summary_opportunity_id_opportunity_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_status_id"],
            ["lk_opportunity_status.opportunity_status_id"],
            name=op.f(
                "current_opportunity_summary_opportunity_status_id_lk_opportunity_status_fkey"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_summary_id"],
            ["opportunity_summary.opportunity_summary_id"],
            name=op.f(
                "current_opportunity_summary_opportunity_summary_id_opportunity_summary_fkey"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_id",
            "opportunity_summary_id",
            name=op.f("current_opportunity_summary_pkey"),
        ),
    )
    op.create_table(
        "link_opportunity_summary_applicant_type",
        sa.Column("opportunity_summary_id", sa.BigInteger(), nullable=False),
        sa.Column("applicant_type_id", sa.Integer(), nullable=False),
        sa.Column("legacy_applicant_type_id", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["applicant_type_id"],
            ["lk_applicant_type.applicant_type_id"],
            name=op.f(
                "link_opportunity_summary_applicant_type_applicant_type_id_lk_applicant_type_fkey"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_summary_id"],
            ["opportunity_summary.opportunity_summary_id"],
            name=op.f(
                "link_opportunity_summary_applicant_type_opportunity_summary_id_opportunity_summary_fkey"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_summary_id",
            "applicant_type_id",
            name=op.f("link_opportunity_summary_applicant_type_pkey"),
        ),
    )
    op.create_table(
        "link_opportunity_summary_funding_category",
        sa.Column("opportunity_summary_id", sa.BigInteger(), nullable=False),
        sa.Column("funding_category_id", sa.Integer(), nullable=False),
        sa.Column("legacy_funding_category_id", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["funding_category_id"],
            ["lk_funding_category.funding_category_id"],
            name=op.f(
                "link_opportunity_summary_funding_category_funding_category_id_lk_funding_category_fkey"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_summary_id"],
            ["opportunity_summary.opportunity_summary_id"],
            name=op.f(
                "link_opportunity_summary_funding_category_opportunity_summary_id_opportunity_summary_fkey"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_summary_id",
            "funding_category_id",
            name=op.f("link_opportunity_summary_funding_category_pkey"),
        ),
    )
    op.create_table(
        "link_opportunity_summary_funding_instrument",
        sa.Column("opportunity_summary_id", sa.BigInteger(), nullable=False),
        sa.Column("funding_instrument_id", sa.Integer(), nullable=False),
        sa.Column("legacy_funding_instrument_id", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["funding_instrument_id"],
            ["lk_funding_instrument.funding_instrument_id"],
            name=op.f(
                "link_opportunity_summary_funding_instrument_funding_instrument_id_lk_funding_instrument_fkey"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_summary_id"],
            ["opportunity_summary.opportunity_summary_id"],
            name=op.f(
                "link_opportunity_summary_funding_instrument_opportunity_summary_id_opportunity_summary_fkey"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_summary_id",
            "funding_instrument_id",
            name=op.f("link_opportunity_summary_funding_instrument_pkey"),
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("link_opportunity_summary_funding_instrument")
    op.drop_table("link_opportunity_summary_funding_category")
    op.drop_table("link_opportunity_summary_applicant_type")
    op.drop_table("current_opportunity_summary")
    op.drop_table("opportunity_summary")
    op.drop_index(
        op.f("opportunity_assistance_listing_opportunity_id_idx"),
        table_name="opportunity_assistance_listing",
    )
    op.drop_table("opportunity_assistance_listing")
    op.drop_index(op.f("opportunity_opportunity_title_idx"), table_name="opportunity")
    op.drop_index(op.f("opportunity_opportunity_category_id_idx"), table_name="opportunity")
    op.drop_index(op.f("opportunity_is_draft_idx"), table_name="opportunity")
    op.drop_table("opportunity")
    # ### end Alembic commands ###