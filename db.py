import databases
import ormar
import sqlalchemy

DATABASE_URL = 'postgresql://postgres:def73261M@localhost/vensus'

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)


class MainMeta(ormar.ModelMeta):
    metadata: sqlalchemy.MetaData = metadata
    database: databases.Database = database
    
