from sqlalchemy import String, create_engine, Column, select
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class NPMData(Base):
    __tablename__ = "data"
    npm = Column(String, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return f"{self.npm} - {self.name}"


engine = create_engine("sqlite:///sqlite.db", echo=True, future=True)

Base.metadata.create_all(engine)


def add_data(npm, name):
    with Session(engine) as sess:
        try:
            data = NPMData(npm=npm, name=name)
            sess.merge(data)
            sess.commit()
            return True
        except Exception:
            raise Exception("DB Error")
    return False


def get_data(npm):
    with Session(engine) as sess:
        query = select(NPMData).where(NPMData.npm.__eq__(npm))
        return sess.scalar(query)
    return None
