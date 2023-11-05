from sqlalchemy import create_engine

from db.models import Base
from db.config import *

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
