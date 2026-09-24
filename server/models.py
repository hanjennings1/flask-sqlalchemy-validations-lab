from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # ----- VALIDATORS -----
    # NAME: cannot be blank & must not already exist
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name cannot be left blank.")
        if db.session.query(Author).filter_by(name=name).first():
            raise ValueError("Author name already exists.")
        return name 

    # PHONE NUMBER: must be exactly 10 characters & digits-only
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # ----- VALIDATORS -----
    # TITLE: must contain "Won't Believe", "Secret", "Top", and/or "Guess"
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must contain: Won't Believe, Secret, Top, and/or Guess")
        return title

    # CONTENT: 250 characters minimum
    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError ("Post content must be at least 250 characters long.")
        return content

    # SUMMARY: 250 characters maximum
    @validates('summary')
    def validate_summary(self, key, summary):
        if not summary or len(summary) > 250:
            raise ValueError ("Post must have summary / Summary must be 250 characters or less.")
        return summary

    # CATEGORY: "Fiction" or "Non-Fiction" ONLY
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post's category must be either 'Fiction' or 'Non-Fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
