from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy     
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SavedImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    print('home')
    if not SavedImages.query.all():
        print(12)
        return render_template('index.html')
        
    allImages = SavedImages.query.all()
    print(allImages[0].filename)
    for image in allImages:
        image.filename = 'uploads/' + image.filename
    # imgNames = ['uploads/' + img.name for img in allImages]
    return render_template('index.html', allImages=allImages)

# upload image
app.config['UPLOAD_PATH'] = 'static/uploads'
@app.route('/upload', methods=['POST'])
def upload():
    print('upload')
    title = request.form['title']
    category = request.form['category']
    picture = request.files['picture']

    if not picture:
        return 'No picture uploaded', 400

    filename = secure_filename(picture.filename)
    mimetype = picture.mimetype
    
    # save image file to directory
    picture.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    # save to database
    img = SavedImages(title=title, category=category, img=picture.read(), filename=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return render_template('index.html')
    return 'Image has been uploaded!', 200

# delete image
@app.route('/delete/<int:id>')
def delete(id):
    filename = SavedImages.query.filter_by(id=id).first().filename
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
    SavedImages.query.filter_by(id=id).delete()
    db.session.commit()
    return 'Deleted'

# display single image
@app.route('/<int:id>')
def display(id):
    img = SavedImages.query.filter_by(id=id).first()
    if not img:
        return 'Image not found!', 404
    
    return Response(img.img, mimetype=img.mimetype)

if __name__ == "__main__":
    app.run(port=5000, debug=True)