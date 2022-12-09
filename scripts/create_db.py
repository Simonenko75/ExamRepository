from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""create table sensors_values (
        id integer not null primary key,
        value float not null,
        created_at varchar(256)
        );""")

    session.execute("""create table sensors_names (
            id integer not null primary key,
            name_sensor varchar(256),
            user_id integer references sensors_values
            );""")

    session.close()

if __name__ == "__main__":
    main()