from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .config import *

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
