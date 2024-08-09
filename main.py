from fastapi import FastAPI

from routers.category_router import category_router
from routers.shops_router import shops_router


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