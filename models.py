# backend/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(100))
    portfolio_website = db.Column(db.String(200))
    github = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    technologies = db.Column(db.Text)  # Stores technologies as a comma-separated string
    niche = db.Column(db.String(200))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'country': self.country,
            'portfolio_website': self.portfolio_website,
            'github': self.github,
            'linkedin': self.linkedin,
            'technologies': self.technologies,
            'niche': self.niche
        }
