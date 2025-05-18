import sqlalchemy as sa
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.util.preloaded import orm

from data.db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    chief_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    members = orm.relationship("User", back_populates='department')
    email = sa.Column(sa.String, nullable=True, unique=True, index=True)
    chief = relationship('User')

    def __repr__(self):
        return f'<Department> {self.id} {self.title} {self.email}'



