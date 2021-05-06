from flask import request, render_template, Response, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import SavedImages
from app.helper import getImages, prevUrlChecker

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

    prevUrl = request.referrer
    prevUrl = prevUrlChecker(prevUrl)       # helper function to check which page sent the request
                                            # home page, favorites page, or tags page  
                                          
    if prevUrl == 'favorites': return redirect(url_for('favorites'))
    elif prevUrl[0] == 'tags': return redirect(url_for('category', category=prevUrl[1]))
    elif prevUrl == 'home': return redirect(url_for('home'))

# favorite/unfavorite image
@app.route('/favorite/<int:id>')
def favorite(id):
    image = SavedImages.query.filter_by(id=id).first()
    if image.favorite is False: image.favorite = True
    else: image.favorite = False
    db.session.commit()

    print('favorited')

    prevUrl = request.referrer
    prevUrl = prevUrlChecker(prevUrl)       # helper function to check which page sent the request
                                            # home page, favorites page, or tags page  
                                          
    if prevUrl == 'favorites': return redirect(url_for('favorites'))
    elif prevUrl[0] == 'tags': return redirect(url_for('category', category=prevUrl[1]))
    elif prevUrl == 'home': return redirect(url_for('home'))

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404