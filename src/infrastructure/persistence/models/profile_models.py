import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.database import Base


class ImporterProfileORM(Base):
    __tablename__ = "importer_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    company_name: Mapped[str] = mapped_column(String(200), default="")
    country: Mapped[str] = mapped_column(String(100), default="")
    tax_id: Mapped[str] = mapped_column(String(50), default="")
    preferred_products: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)


class BrokerProfileORM(Base):
    __tablename__ = "broker_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    company_name: Mapped[str] = mapped_column(String(200), default="")
    origin_countries: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    certifications: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    annual_volume: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)


class FarmerProfileORM(Base):
    __tablename__ = "farmer_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    farm_name: Mapped[str] = mapped_column(String(200), default="")
    location: Mapped[str] = mapped_column(String(200), default="")
    hectares: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    main_crops: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    irrigation_type: Mapped[str] = mapped_column(String(50), default="")


class CollieAppProfileORM(Base):
    __tablename__ = "collie_app_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    collie_external_id: Mapped[str] = mapped_column(String(100), unique=True, default="")
    sso_token: Mapped[str] = mapped_column(String(512), default="")
    subscription_plan: Mapped[str] = mapped_column(String(50), default="")
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
