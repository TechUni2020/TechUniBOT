from techuni.techuni_object import JoinApplication
from techuni.techuni_database.schema import JoinApplicationTable

class DatabaseSession:
    def __init__(self, session):
        self.database_session = session

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

    def get_application(self, application: JoinApplication):
        return self.database_session.query(JoinApplicationTable).filter_by(form_id=application.id).first()

    def get_application_by_thread(self, thread_id: int):
        return self.database_session.query(JoinApplicationTable).filter_by(thread_id=thread_id).first()

    def commit(self):
        self.database_session.commit()

    def close(self):
        self.database_session.close()