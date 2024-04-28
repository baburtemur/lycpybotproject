import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase, create_session, global_init
from sqlalchemy.dialects.mysql import insert


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    Id = sqlalchemy.Column(sqlalchemy.Integer, default=0, primary_key=True)
    Warnings = sqlalchemy.Column(sqlalchemy.Integer, default=0)


def add_user(_id: int):
    global_init('db/dsbot.db')
    user = User()
    user.Id = _id
    db_session = create_session()
    if not db_session.query(User).get(user.Id):
        user.Warnings = 1
        status = 1
        db_session.add(user)
    else:
        user = db_session.query(User).get(user.Id)
        user.Warnings += 1
        status = user.Warnings
        db_session.query(User).filter(User.Id == _id).update(
            {User.Warnings: sqlalchemy.sql.expression.func.replace(User.Warnings, user.Warnings - 1, user.Warnings)})
    db_session.commit()
    return status
