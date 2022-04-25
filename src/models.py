from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    mass = db.Column(db.Float, unique=False, nullable=True)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
        }

class Planetas(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), primary_key=False)
    rotation = db.Column(db.Integer, primary_key=False)
    population = db.Column(db.Integer, primary_key=False)
    residents = db.Column(db.String(180), primary_key=False)

    def serialize(self):
        return {
            "pid":self.pid,
            "name": self.name,
            "rotation": self.rotation,
            "population": self.population,
            "residents": self.residents,
        }

class Favpeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid_people = db.Column(db.Integer, db.ForeignKey('people.uid'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    people = db.relationship('People')
    user = db.relationship('User')

    def serialize(self):
        return {
            "uid_people": self.uid_people,
            "id_user": self.id_user,
            "id": self.id
        }
class Favplanetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid_planetas = db.Column(db.Integer, db.ForeignKey('planetas.pid'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    Planetas = db.relationship('Planetas')
    user = db.relationship('User')

    def serialize(self):
        return {
            "id": self.id,
            "pid_planetas": self.pid_planetas,
            "id_user": self.id_user,
        }