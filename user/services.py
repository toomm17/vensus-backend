import random
import uuid
from typing import Union

from jose import jwt
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_utils.curried import to_hex

from fastapi import Request

from . import schemas
from .models import User, Wallet


# Get user
async def get_token_from_headers(request: Request) -> str:
    auth_header_str = request.headers.get('authorization')
    token = auth_header_str.replace('Bearer ', '')
    return token


async def decode_access_token(token: str) -> dict:
    return jwt.decode(token, 'test', algorithms='HS256')


async def get_user_wallets(public_address: str, coin: str) -> Union[User | None]:
    wallet = await Wallet.objects.get_or_none(public_address=public_address, coin=coin)
    if wallet:
        user = await User.objects.select_related('wallets').filter(wallets__user_id=wallet.user_id).all()
        return user[0].wallets
    return None


async def get_user(message: str) -> User:
    nonce = await get_nonce(message)
    user = await User.objects.get(nonce=nonce)
    return user


# Create user
async def format_sign_message(message: str):
    message_to_hex = to_hex(text=message)
    message_hash = encode_defunct(hexstr=message_to_hex)
    return message_hash


async def get_nonce(message: str) -> int:
    nonce = message.split('nonce: ')[-1]
    print(nonce)
    return int(nonce)


async def generate_access_token(wallet: Wallet) -> str:
    return jwt.encode(
        {'wallet': wallet.public_address, 'coin': wallet.coin},
        'test',
        algorithm='HS256'
    )


async def verify_signature(signature: str, message: str, wallet: str) -> bool:
    # Maybe add this to pydantic validation
    message_hash = await format_sign_message(message)
    signer_address = w3.eth.account.recover_message(message_hash, signature=signature)
    if signer_address.lower() != wallet:
        return False
    return True


async def _generate_nonce():
    return random.randint(100000, 999999)


async def create_user(nonce: int) -> User:
    user = await User.objects.create(nonce=nonce)
    return user


async def create_login_message() -> str:
    nonce = await _generate_nonce()
    user = await create_user(nonce)
    message = f'Authorize your wallet to play!\n\nYour nonce: {nonce}'
    return message


async def create_wallet(user_data: schemas.CreateUser, user_id: int) -> Union[Wallet | None]:
    signature, message, wallet = user_data.signature, user_data.message, user_data.wallet
    signature_is_verify = await verify_signature(signature, message, wallet)
    if signature_is_verify:
        wallet = await Wallet.objects.create(
            public_address=wallet, signature=signature, coin=user_data.coin, user_id=user_id
        )
        return wallet

    return None




