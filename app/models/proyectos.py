from .. import db

class Proyectos(db.Model):

    __tablename__ = 'proyectos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    titulo = db.Column(db.String(128), nullable=False)
    path = db.Column(db.String(256), nullable=True)
    portada = db.Column(db.String(256), nullable=True)

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