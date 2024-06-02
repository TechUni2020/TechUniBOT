from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import String
from sqlalchemy.dialects.mysql import TEXT, BIGINT

Base = declarative_base()

class JoinApplicationTable(Base):
    __tablename__ = "join_application"

    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(String(255), nullable=False, unique=True)
    mail_address = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    thread_id = Column(BIGINT, nullable=False, unique=True)

    @classmethod
    def from_application(cls, application, thread_id):
        return cls(
            form_id=application.id,
            mail_address=application.mail_address,
            name=application.name,
            thread_id=thread_id
        )