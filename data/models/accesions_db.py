import sqlalchemy

from data.db_session import SqlAlchemyBase, create_session, global_init


class Accession(SqlAlchemyBase):
    __tablename__ = 'Accessions'

    Id = sqlalchemy.Column(sqlalchemy.Integer, default=0, primary_key=True)
    Date = sqlalchemy.Column(sqlalchemy.String, default=0)


def add_accession(_id, date):
    global_init('db/dsbot.db')
    accession = Accession()
    accession.Id = _id
    accession.Date = date
    db_session = create_session()
    db_session.add(accession)
    db_session.commit()
    return
