from sqlalchemy.orm import sessionmaker
from techuni.object import JoinApplication
from techuni.database.schema import JoinApplicationTable


class DatabaseSessionManager:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def __enter__(self):
        self.database_session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.database_session.rollback()
        self.database_session.close()

    def add_application(self, application: JoinApplication, thread_id: int):
        data = JoinApplicationTable.from_application(application, thread_id)
        self.database_session.add(data)
        self.commit()

    def delete_application(self, application: JoinApplication):
        data = self.get_application(application)
        self.database_session.delete(data)
        self.commit()

    def delete_application_by_thread(self, thread_id: int):
        data = self.get_application_by_thread(thread_id)
        self.database_session.delete(data)
        self.commit()

    def get_application(self, application: JoinApplication) -> JoinApplicationTable:
        return self.database_session.query(JoinApplicationTable).filter_by(form_id=application.id).one()

    def get_application_by_thread(self, thread_id: int) -> JoinApplicationTable:
        return self.database_session.query(JoinApplicationTable).filter_by(thread_id=thread_id).one()

    def commit(self):
        self.database_session.commit()

    def close(self):
        self.database_session.close()
