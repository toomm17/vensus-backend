import uuid
from typing import Union

from jose import jwt
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_utils.curried import to_hex

from . import models
from . import schemas


async def create_user() -> Union[models.User | str]:
    user_uuid = uuid.uuid4()
    str_user_uuid = uuid.UUID(str(user_uuid))
    user, created = await models.User.objects.get_or_create(uuid=str_user_uuid)
    if created:
       return user
    return 'Have uuid'


async def format_sign_message(message: str):
    message_to_hex = to_hex(text=message)
    message_hash = encode_defunct(hexstr=message_to_hex)
    return message_hash


async def verify_signature(signature: str, message: str, wallet: str) -> bool:
    # Maybe add this to pydantic validation
    message_hash = await format_sign_message(message)
    signer_address = w3.eth.account.recover_message(message_hash, signature=signature)
    if signer_address.lower() != wallet:
        return False
    return True


async def get_nonce(message: str) -> int:
    nonce = message.split('nonce: ')[-1]
    print(nonce)
    return int(nonce)


async def add_user_wallet(wallet_data: schemas.AddUserWallet) -> Union[models.Wallet | None]:
    signature_is_verify = await verify_signature(
        wallet_data.signature, wallet_data.message, wallet_data.public_address
    )
    if signature_is_verify:
        wallet = await models.Wallet.objects.create(
            user_id=wallet_data.user_id, signature=wallet_data.signature, message=wallet_data.message,
            public_address=wallet_data.public_address, coin=wallet_data.coin,
        )
        return wallet
    return None


async def get_wallet(public_address: str, coin: str) -> models.Wallet:
    wallet = await models.Wallet.objects.get_or_none(public_address=public_address, coin=coin)
    return wallet


async def generate_jwt_user(user_id: int):
    return jwt.encode({'user_id': user_id}, 'backend_test', algorithm='HS256')


async def get_connected_wallets(user_id: int):
    wallets = await models.Wallet.objects.all(user_id=user_id)
    print(wallets)
    return wallets
