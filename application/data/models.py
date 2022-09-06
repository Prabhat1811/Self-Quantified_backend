from .database import db
from flask_login import login_manager
from flask_security import UserMixin, RoleMixin
from sqlalchemy.sql import func

roles_users = db.Table('roles_users', 
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    )

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)
    description = db.Column(db.String)
    tracker_type = db.Column(db.String)
    settings = db.Column(db.String)

class TrackerLog(db.Model):
    __tablename__ = 'tracker_log'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'))
    timestamp = db.Column(db.DateTime, server_default=func.now())
    value = db.Column(db.Integer)
    note = db.Column(db.String)