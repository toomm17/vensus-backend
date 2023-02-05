import ormar

from db import MainMeta


# TODO 
# Maybe create Enum types for game in BetHistory, coin in all tables, 
# ttype in Transaction, check how can do it with javascript post request
# Something like str choice

class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    uuid: str = ormar.UUID(uuid_format='string')
    username: str = ormar.String(max_length=25, unique=True, nullable=True)
    total_deposit: float = ormar.Float(nullable=True)
    total_withdraw: float = ormar.Float(nullable=True)


class Wallet(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.ForeignKey(User)
    public_address: str = ormar.String(max_length=255)
    message: str = ormar.String(max_length=255, unique=True)
    coin: str = ormar.String(max_length=10)
    signature: str = ormar.String(max_length=255, nullable=True)
    balance: float = ormar.Float(default=0)

    
class Transaction(ormar.Model):
    class Meta(MainMeta):
        pass
    
    # Only for withdrawal and replenishment info
    
    # Maybe add trx hash
    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.ForeignKey(User)
    ttype: str = ormar.String(max_length=13)  # Transaction type
    coin: str = ormar.String(max_length=3)
    tsum: float = ormar.Float()  # Transaction sum


class BetHistory(ormar.Model):
    class Meta(MainMeta):
        pass
    
    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.ForeignKey(User)
    game: str = ormar.String(max_length=8)
    bet: float = ormar.Float()
    coefficient: float = ormar.Float()
    result: float = ormar.Float()
    

