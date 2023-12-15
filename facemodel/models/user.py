#!/usr/bin/env python3
"""Template for the User Class"""
from facemodel import db
from flask_login import UserMixin
from facemodel.models.base import BaseModel


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    image_id = db.Column(db.String(255), nullable=False, unique=True, default=None)

    def __init__(self, email, first_name, last_name, image_id=None):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.image_id = image_id


    def __repr__(self):
        return f'<User {self.username}>'

    def format(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_id': self.image_id
        }