from .. import db
import datetime

class Historico_clicks(db.Model):

    __tablename__ = 'historico_clicks'

    id = db.Column(db.Integer, primary_key=True)
    id_proyecto = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

    @classmethod
    def insert(self, **kwargs):
        session = db.session
        try:
            new_record = self(**kwargs)
            session.add(new_record)
            session.commit()
            return new_record
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def update(self, record_id, **kwargs):
        session = db.session
        try:
            query = db.update(self).where(self.id == record_id).values(**kwargs)
            session.execute(query)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def delete(self, record_id):
        session = db.session
        try:
            record = session.query(self).get(record_id)
            if record:
                session.delete(record)
                session.commit()
            else:
                raise ValueError("Record not found")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def to_dict(self):
        return {
            'id': self.id,
            'id_proyecto': self.id_proyecto,
            'fecha': self.fecha.isoformat()
        }
