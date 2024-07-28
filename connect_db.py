from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///dbUniversity.db")
Session = sessionmaker(bind=engine)
session = Session()