from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.users import User
from schemas.user_schema import UserSchema

users_router = APIRouter(
    tags=['Users']
)


@users_router.post('/create')
async def create_user(user_info: UserSchema,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        new_user = User(**user_info.dict())
        session.add(new_user)
        await session.commit()
        return {'status': 200, 'new_user': new_user}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

