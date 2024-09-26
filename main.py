from fastapi import FastAPI

from routers.category_router import category_router
from routers.orders_router import orders_router
from routers.shops_router import shops_router
from routers.users_router import users_router

app = FastAPI()


app.include_router(
    shops_router,
    prefix='/shops',
    tags=['Shops']
)

app.include_router(
    category_router,
    prefix='/categories',
    tags=['Categories']
)

app.include_router(
    orders_router,
    prefix='/orders',
    tags=['Orders']
)

app.include_router(
    users_router,
    prefix='/users',
    tags=['Users']
)
