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

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author must have a name.")

        # Check if another author with the same name already exists
        existing = Author.query.filter_by(name=value).first()
        if existing:
            raise ValueError(f"Author with name '{value}' already exists.")
        
        return value

    @validates('phone_number')
    def validate_phone_number(slef, key, value):
        if not value.isdigit() or len(value) !=10:
            raise ValueError("Phone number must be exactly 10 digits.") 
        return value           

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

    # Add validators
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Post must have a title.")

        clickbait_phrases = [
            "Won't Believe", "Secret", "Top", "Guess"
        ]

        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait.")
        
        return value

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Summary must be at most 250 characters.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return value  


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
