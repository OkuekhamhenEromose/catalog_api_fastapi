"""create authors and books

Revision ID: 0001
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("country", sa.String(80), nullable=True),
        sa.UniqueConstraint("name", name="uq_authors_name"),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(6, 2), nullable=False),
        sa.Column("in_stock", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["author_id"], ["authors.id"],
                                name="books_author_id_fkey", ondelete="RESTRICT"),
        sa.CheckConstraint("price >= 0", name="ck_books_price_nonnegative"),
        sa.UniqueConstraint("author_id", "title", name="uq_books_author_title"),
    )


def downgrade() -> None:
    op.drop_table("books")
    op.drop_table("authors")
