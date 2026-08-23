from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = '0001_initial'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'hotel_reservations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('booking_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('no_of_adults', sa.Integer(), nullable=False),
        sa.Column('no_of_children', sa.Integer(), nullable=False),
        sa.Column('no_of_weekend_nights', sa.Integer(), nullable=False),
        sa.Column('no_of_week_nights', sa.Integer(), nullable=False),
        sa.Column('required_car_parking_space', sa.Integer(), nullable=False),
        sa.Column('lead_time', sa.Integer(), nullable=False),
        sa.Column('arrival_year', sa.Integer(), nullable=False),
        sa.Column('arrival_month', sa.Integer(), nullable=False),
        sa.Column('arrival_date', sa.Integer(), nullable=False),
        sa.Column('repeated_guest', sa.Integer(), nullable=False),
        sa.Column('no_of_previous_cancellations', sa.Integer(), nullable=False),
        sa.Column('no_of_previous_bookings_not_canceled', sa.Integer(), nullable=False),
        sa.Column('avg_price_per_room', sa.Float(), nullable=False),
        sa.Column('no_of_special_requests', sa.Integer(), nullable=False),
        sa.Column('type_of_meal_plan', sa.String(), nullable=False),
        sa.Column('room_type_reserved', sa.String(), nullable=False),
        sa.Column('market_segment_type', sa.String(), nullable=False),
        sa.Column('customer_image_path', sa.Text(), nullable=True),
        sa.Column('ocr_raw_text', sa.Text(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('prediction_score', sa.Float(), nullable=True),
        sa.Column(
            'discounts',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_hotel_reservations_id', 'hotel_reservations', ['id'], unique=False)
    op.create_index('ix_hotel_reservations_booking_id', 'hotel_reservations', ['booking_id'], unique=True)
    op.create_index('ix_hotel_reservations_email', 'hotel_reservations', ['email'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_hotel_reservations_email', table_name='hotel_reservations')
    op.drop_index('ix_hotel_reservations_booking_id', table_name='hotel_reservations')
    op.drop_index('ix_hotel_reservations_id', table_name='hotel_reservations')
    op.drop_table('hotel_reservations')
