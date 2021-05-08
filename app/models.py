from app import db

# creates table titled 'saved_images' with columns for 
# id no. for the upload, title of the image, category the image belongs to,
# file name of the image, and whether or not the image is favorited by the user
class SavedImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    category = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, unique=True, nullable=False)
    favorite = db.Column(db.Boolean, default=False, nullable=False)