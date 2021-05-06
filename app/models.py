from app import db

class SavedImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    category = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, unique=True, nullable=False)
    favorite = db.Column(db.Boolean, default=False, nullable=False)