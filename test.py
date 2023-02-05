from fastapi import APIRouter

from db import User, Wallet
from schemas import User, Wallet

router = APIRouter()


@router.get('/')
async def root():
    return {'message': 'Hello world!'}


@router.get('/user', response_model=User)
async def create_user():
    pass