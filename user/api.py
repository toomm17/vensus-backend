from fastapi import APIRouter, Request

from . import schemas
from . import new_service

user_router = APIRouter(prefix='/user')


@user_router.get('/create/token')
async def create_user_token():
    # In frontend headers add jwt for only fronted api request
    user = await new_service.create_user()  # Check instance maybe string
    token = await new_service.generate_jwt_user(user.id)
    return {'token': token}


@user_router.get('/get/{public_address}/{coin}')
async def get_wallets(public_address: str, coin: str):
    wallet = await new_service.get_wallet(public_address, coin)
    return {'wallet': wallet}


@user_router.post('/add/user/wallet')
async def add_wallet(wallet_data: schemas.AddUserWallet):
    new_wallet = await new_service.add_user_wallet(wallet_data)
    return {'wallet_added': new_wallet}


@user_router.post('/get/connected/wallets')
async def get_connected_wallets(user_data: schemas.GetConnectedWallets):
    wallets = await new_service.get_connected_wallets(user_data.user_id)
    return {'wallets': wallets}