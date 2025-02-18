"""empty message

Revision ID: c8e6973bb14f
Revises: b4326d2fff0c
Create Date: 2025-02-16 17:34:49.771536

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c8e6973bb14f'
down_revision = "b4326d2fff0c"
branch_labels = None
depends_on = None


def upgrade():
    # Example of adding a foreign key constraint
    with op.batch_alter_table("order", schema=None) as batch_op:
        batch_op.create_foreign_key("fk_order_user", "user", ["admin_id"], ["id"])


def downgrade():
    # Example of dropping the foreign key constraint
    with op.batch_alter_table("order", schema=None) as batch_op:
        batch_op.drop_constraint("fk_order_user", type_="foreignkey")
