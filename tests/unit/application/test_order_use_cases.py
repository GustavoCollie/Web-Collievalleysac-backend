import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.order import Order, OrderItem, OrderStatus
from domain.entities.product import Product
from domain.exceptions.order import InvalidOrder, OrderNotModifiable
from domain.exceptions.auth import InsufficientPermissions
from application.dtos.order_dto import CreateOrderInput, OrderItemInput, UpdateOrderStatusInput
from application.use_cases.orders.create_order import CreateOrderUseCase
from application.use_cases.orders.list_orders import ListOrdersUseCase
from application.use_cases.orders.update_order_status import UpdateOrderStatusUseCase


@pytest.fixture
def mock_order_repo():
    return AsyncMock()


@pytest.fixture
def mock_product_repo():
    return AsyncMock()


@pytest.fixture
def sample_product():
    return Product(
        id=uuid4(),
        name="Palta Hass",
        slug="palta-hass",
        category="fruta",
        price_per_kg=5.0,
        is_available=True,
    )


class TestCreateOrder:
    @pytest.mark.asyncio
    async def test_create_order_success(self, mock_order_repo, mock_product_repo, sample_product):
        mock_product_repo.find_by_id.return_value = sample_product

        user_id = uuid4()
        order = Order(
            user_id=user_id,
            items=[OrderItem(product_id=sample_product.id, quantity_kg=100, quality_grade="Premium", unit_price=5.0)],
        )
        mock_order_repo.save.return_value = order

        use_case = CreateOrderUseCase(mock_order_repo, mock_product_repo)
        result = await use_case.execute(
            CreateOrderInput(
                user_id=user_id,
                items=[OrderItemInput(product_id=sample_product.id, quantity_kg=100, quality_grade="Premium")],
            )
        )

        assert result.total_amount == 500.0
        mock_order_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_product_not_found(self, mock_order_repo, mock_product_repo):
        mock_product_repo.find_by_id.return_value = None

        use_case = CreateOrderUseCase(mock_order_repo, mock_product_repo)
        with pytest.raises(InvalidOrder, match="no encontrado"):
            await use_case.execute(
                CreateOrderInput(
                    user_id=uuid4(),
                    items=[OrderItemInput(product_id=uuid4(), quantity_kg=100, quality_grade="Standard")],
                )
            )

    @pytest.mark.asyncio
    async def test_create_order_product_unavailable(self, mock_order_repo, mock_product_repo, sample_product):
        sample_product.is_available = False
        mock_product_repo.find_by_id.return_value = sample_product

        use_case = CreateOrderUseCase(mock_order_repo, mock_product_repo)
        with pytest.raises(InvalidOrder, match="no está disponible"):
            await use_case.execute(
                CreateOrderInput(
                    user_id=uuid4(),
                    items=[OrderItemInput(product_id=sample_product.id, quantity_kg=100, quality_grade="Standard")],
                )
            )


class TestListOrders:
    @pytest.mark.asyncio
    async def test_list_orders(self, mock_order_repo):
        user_id = uuid4()
        mock_order_repo.find_by_user.return_value = []

        use_case = ListOrdersUseCase(mock_order_repo)
        result = await use_case.execute(user_id)

        assert result == []
        mock_order_repo.find_by_user.assert_called_once_with(user_id)


class TestUpdateOrderStatus:
    @pytest.mark.asyncio
    async def test_update_draft_to_pending(self, mock_order_repo):
        user_id = uuid4()
        order = Order(
            id=uuid4(),
            user_id=user_id,
            items=[OrderItem(product_id=uuid4(), quantity_kg=10, quality_grade="Standard", unit_price=5.0)],
            status=OrderStatus.DRAFT,
        )
        mock_order_repo.find_by_id.return_value = order
        mock_order_repo.update.return_value = order

        use_case = UpdateOrderStatusUseCase(mock_order_repo)
        result = await use_case.execute(
            UpdateOrderStatusInput(order_id=order.id, status="pending", user_id=user_id)
        )

        mock_order_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_invalid_transition_raises(self, mock_order_repo):
        user_id = uuid4()
        order = Order(
            id=uuid4(),
            user_id=user_id,
            items=[OrderItem(product_id=uuid4(), quantity_kg=10, quality_grade="Standard", unit_price=5.0)],
            status=OrderStatus.DELIVERED,
        )
        mock_order_repo.find_by_id.return_value = order

        use_case = UpdateOrderStatusUseCase(mock_order_repo)
        with pytest.raises(OrderNotModifiable):
            await use_case.execute(
                UpdateOrderStatusInput(order_id=order.id, status="cancelled", user_id=user_id)
            )

    @pytest.mark.asyncio
    async def test_wrong_user_raises(self, mock_order_repo):
        order = Order(
            id=uuid4(),
            user_id=uuid4(),
            items=[OrderItem(product_id=uuid4(), quantity_kg=10, quality_grade="Standard", unit_price=5.0)],
            status=OrderStatus.DRAFT,
        )
        mock_order_repo.find_by_id.return_value = order

        use_case = UpdateOrderStatusUseCase(mock_order_repo)
        with pytest.raises(InsufficientPermissions):
            await use_case.execute(
                UpdateOrderStatusInput(order_id=order.id, status="pending", user_id=uuid4())
            )
