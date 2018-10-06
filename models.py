from fpl_website import db
from sqlalchemy.dialects.postgresql import JSON

#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
class Result(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    element_type = db.Column(db.String(), index=True)
    singular_name = db.Column(db.String())
    singular_name_short = db.Column(db.String())

    def __init__(self, element_type, singular_name, singular_name_short):
        self.element_type = element_type
        self.singular_name = singular_name
        self.singular_name_short = singular_name_short

    def __repr__(self):
        return '<Name {}>'.format(self.singular_name)