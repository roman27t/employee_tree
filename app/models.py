import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm, ForeignKey, UniqueConstraint
from sqlalchemy_utils import LtreeType
from sqlalchemy import Index
from sqlalchemy import func
from sqlalchemy.orm import relationship, remote, foreign

metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)


class PositionModel(Base):
    __tablename__ = 'position'

    pk = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False, unique=True)
    detail = sa.Column(sa.String(255), nullable=False, default='')

    @property
    def serialized(self) -> dict:
        return {
            'pk': self.pk,
            'name': self.name,
            'detail': self.detail,
        }


class StaffModel(Base):
    __tablename__ = 'staff'

    pk = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    hiring_date = sa.Column(sa.DateTime(), default=dt.datetime.now)
    last_name = sa.Column(sa.String(50), nullable=False)
    first_name = sa.Column(sa.String(50), nullable=False)
    middle_name = sa.Column(sa.String(50), nullable=False, default='')
    birthdate = sa.Column(sa.Date(), nullable=False)
    wage_rate = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    path = sa.Column(LtreeType, nullable=False)
    position_id = sa.Column(sa.Integer, ForeignKey('position.pk'))

    position = relationship('PositionModel')

    # parent = relationship(
    #     'Node',
    #     primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
    #     backref='children',
    #     viewonly=True
    # )
    __table_args__ = (
        UniqueConstraint('last_name', 'birthdate', 'position_id', name='unique_compound_key'),
        # Index('ix_nodes_path', path, postgresql_using='gist'),
    )

    @property
    def serialized(self) -> dict:
        return {
            'pk': self.pk,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'path': str(self.path),
            'position_id': self.position_id,
            'wage_rate': float(self.wage_rate),
        }
