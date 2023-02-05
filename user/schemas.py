from pydantic import BaseModel


class AddUserWallet(BaseModel):
    public_address: str
    message: str
    signature: str
    coin: str
    user_id: int

    
class GetConnectedWallets(BaseModel):
    user_id: int
