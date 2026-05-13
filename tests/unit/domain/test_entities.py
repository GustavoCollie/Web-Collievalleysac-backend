import pytest
from uuid import uuid4

from domain.entities.user import User, Role
from domain.entities.order import Order, OrderItem, OrderStatus
from domain.entities.product import Product
from domain.entities.brokerage import BrokerageRequest, BrokerageStatus
from domain.entities.advisory import AdvisoryRequest, Urgency
from domain.exceptions.order import InvalidOrder
from domain.value_objects.email import Email
from domain.value_objects.money import Money
from domain.exceptions.base import DomainException


class TestUser:
    def test_create_user(self):
        user = User(email="test@example.com", full_name="Test User", role=Role.IMPORTADOR)
        assert user.email == "test@example.com"
        assert user.role == Role.IMPORTADOR
        assert user.is_active is True

    def test_all_roles_exist(self):
        assert len(Role) == 5
        assert Role.ADMIN.value == "admin"
        assert Role.EXPORTADOR_BROKER.value == "exportador_broker"


class TestOrder:
    def test_create_order_with_items(self):
        item = OrderItem(product_id=uuid4(), quantity_kg=100.0, quality_grade="Premium", unit_price=5.0)
        order = Order(user_id=uuid4(), items=[item])
        assert order.total_amount == 500.0
        assert order.status == OrderStatus.DRAFT

    def test_order_without_items_raises(self):
        with pytest.raises(InvalidOrder, match="al menos un ítem"):
            Order(user_id=uuid4(), items=[])

    def test_order_total_multiple_items(self):
        items = [
            OrderItem(product_id=uuid4(), quantity_kg=100.0, quality_grade="Premium", unit_price=5.0),
            OrderItem(product_id=uuid4(), quantity_kg=200.0, quality_grade="Standard", unit_price=3.5),
        ]
        order = Order(user_id=uuid4(), items=items)
        assert order.total_amount == 1200.0


class TestEmail:
    def test_valid_email(self):
        email = Email("Test@Example.COM")
        assert email.value == "test@example.com"

    def test_invalid_email_raises(self):
        with pytest.raises(DomainException, match="Email inválido"):
            Email("not-an-email")

    def test_email_immutable(self):
        email = Email("test@example.com")
        with pytest.raises(AttributeError):
            email.value = "other@example.com"


class TestMoney:
    def test_valid_money(self):
        money = Money(amount=100.0, currency="USD")
        assert money.amount == 100.0

    def test_negative_amount_raises(self):
        with pytest.raises(DomainException, match="negativo"):
            Money(amount=-10.0)

    def test_invalid_currency_raises(self):
        with pytest.raises(DomainException, match="3 caracteres"):
            Money(amount=10.0, currency="US")


class TestBrokerageRequest:
    def test_create_brokerage(self):
        req = BrokerageRequest(
            user_id=uuid4(),
            origin_country="Peru",
            dest_country="USA",
            product_type="Palta Hass",
            volume_kg=5000.0,
        )
        assert req.status == BrokerageStatus.REQUESTED


class TestAdvisoryRequest:
    def test_create_advisory(self):
        req = AdvisoryRequest(
            user_id=uuid4(),
            crop_type="Palta",
            problem_description="Plagas en hojas",
        )
        assert req.urgency == Urgency.MEDIUM
