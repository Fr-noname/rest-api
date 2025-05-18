from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey('users.id'), nullable=False)
    job = Column(String, nullable=False)
    work_size = Column(Integer, nullable=False)
    collaborators = Column(String, nullable=True)
    start_date = Column(String, default=datetime.utcnow, nullable=False)
    end_date = Column(String, nullable=True)
    is_finished = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Job> {self.job}'