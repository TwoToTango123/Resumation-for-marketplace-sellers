from db.database import engine, Base
from db.models import Review, Response
def init():
    Base.metadata.create_all(engine)
    print("Таблицы созданы")

if __name__ == "__main__":
    init()