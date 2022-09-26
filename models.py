from flask_sqlalchemy import SQLAlchemy


GENERIC_IMAGE ="https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"

db = SQLAlchemy()

class Pet (db.Model):
    __tablename__ = "pets"

    def __repr__(self):
        """show info about pet"""
        return f"<{self.id} {self.name} {self.age} {self.species}>"

    id      = db.Column (  db.Integer,
                            primary_key = True,
                            autoincrement = True  )
    name    = db.Column (   db.String(50),
                            nullable = False)
    species = db.Column (   db.String(30), nullable = False)
    photo_url = db.Column ( db.Text, 
                            nullable = True,
                            default = GENERIC_IMAGE)
    age     = db.Column (   db.Integer,
                            nullable = True)
    notes = db.Column (     db.Text,
                            nullable = True)
    available = db.Column ( db.Boolean, 
                            nullable = False,
                            default = True)


def connect_db(app):
    """Connects the database to Flask app"""
    db.app = app
    db.init_app(app)
