from app import db
from flask import jsonify

class Img(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String())
    description = db.Column(db.String())
    created_at = db.Column(db.String())

    def __init__(self, path, description, created_at):
        self.path = path
        self.description = description
        self.created_at = created_at

    def serialize(self):
        # return jsonify(
        #     id=self.id,
        #     path=self.path,
        #     description=self.description,
        #     created_at=self.created_at
        # )
        return {
            'id': self.id,
            'path': self.path,
            'description': self.description,
            'created_at': self.created_at
        }