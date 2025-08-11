from database.database import engine, Base
from database.models import Trade, Signal, Balance, BacktestResult

def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":

    init_database()
