from src.integrations.cars import CarsKafkaProducer
from src.integrations.orders import OrdersClient
from src.integrations.users import UsersClient, UsersKafkaProducer


async def get_users_client() -> UsersClient:
    return UsersClient()


async def get_users_kafka() -> UsersKafkaProducer:
    return UsersKafkaProducer()


async def get_cars_kafka() -> CarsKafkaProducer:
    return CarsKafkaProducer()


async def get_orders_client() -> OrdersClient:
    return OrdersClient()
