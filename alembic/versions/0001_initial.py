"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2025-11-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("incident_type", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("date_time", sa.DateTime(), nullable=True),
        sa.Column("severity_level", sa.String(length=50), nullable=False),
        sa.Column("contact_information", sa.String(length=255), nullable=True),
        sa.UniqueConstraint(
            "contact_information", name="uq_incidents_contact_information"
        ),
    )


def downgrade() -> None:
    op.drop_table("incidents")
