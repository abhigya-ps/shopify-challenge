from flask import request, render_template, Response, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import SavedImages

def getImages(category=None, favorites=False):

    if favorites is True:          # return favorited images
        if not SavedImages.query.filter_by(favorite=True): allImages = []
        else: allImages = SavedImages.query.filter_by(favorite=True)

    elif category is None:        # no category mentioned -> show all images
        if not SavedImages.query.all(): allImages = []
        else: allImages = SavedImages.query.all()

    else:                       # shows images of given category
        if not SavedImages.query.filter_by(category=category): allImages = []
        else: allImages = SavedImages.query.filter_by(category=category)
        
    for image in allImages:     # path for images inside uploads folder
        image.filename = 'uploads/' + image.filename

    return allImages
    

@app.route('/')
def home():
    print('home')
    allImages = getImages()
    return render_template('index.html', images=allImages)

# upload image
app.config['UPLOAD_PATH'] = 'app/static/uploads'
@app.route('/', methods=['POST'])
def upload():
    print('upload')
    title = request.form['title']
    category = request.form['category']
    picture = request.files['picture']

    if not picture:
        return 'No picture uploaded', 400

    filename = secure_filename(picture.filename)
    print(filename)
    # save image file to directory
    picture.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    # save to database
    img = SavedImages(title=title, category=category, filename=filename)
    db.session.add(img)
    db.session.commit()

    allImages = getImages()
    return render_template('index.html', images=allImages)

# delete image
@app.route('/delete/<int:id>')
def delete(id):
    filename = SavedImages.query.filter_by(id=id).first().filename
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
    SavedImages.query.filter_by(id=id).delete()
    db.session.commit()

    print('deleted')
    prev_url = request.referrer
    if len(prev_url) > 22:  
        if prev_url[22:] == 'favorites':        # check if delete request is coming from a favorite page
            return redirect(url_for('favorites'))
        else:                       # check if delete request is coming from a category page
            tag = prev_url[27:]
            return redirect(url_for('category', category=tag))
    else:                         # delete request is coming from home page
        return redirect(url_for('home'))

# favorite/unfavorite image
@app.route('/favorite/<int:id>')
def favorite(id):
    image = SavedImages.query.filter_by(id=id).first()
    if image.favorite is False: image.favorite = True
    else: image.favorite = False
    db.session.commit()

    print('favorited')
    prev_url = request.referrer
    if len(prev_url) > 22:      # check if favorite request is coming from a category page
        tag = prev_url[27:]
        return redirect(url_for('category', category=tag))
    else:                       # favorite request is coming from home page
        return redirect(url_for('home'))

# favorites page
@app.route('/favorites')
def favorites():
    print('favorites')
    allImages = getImages(None, True)
    return render_template('categories.html', images=allImages, category='favorites')

# category page
@app.route('/tags/<category>')
def category(category):
    print('category:', category)
    allImages = getImages(category)
    return render_template('categories.html', images=allImages, category=category)