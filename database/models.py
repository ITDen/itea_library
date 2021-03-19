from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class Reader(UserMixin, db.Model):
    __tablename__ = 'readers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    books = db.relationship('Book', backref='reader', lazy='dynamic', cascade="save-update")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return f'{self.surname} {self.name}'

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer())
    add_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey(f'readers.id'), nullable=True)

    def __repr__(self):
        return f'{self.title}, {self.author}, {self.year}'
