from flask import request, render_template, Response, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import SavedImages
from app.helper import getImages, prevUrlChecker, tags, fileFormat, noFileName, errorType
from sqlalchemy import exc
import traceback

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

    if noFileName(filename) is True:        # check if image file has a name
        return render_template('error.html', message="image has no file name")

    if fileFormat(filename) is False:       # check if the format of the image file is valid
        return render_template('error.html', message="acceptable formats are jpg, jpeg, png, and webp")

    try:
        # save to database 
        img = SavedImages(title=title, category=category, filename=filename)
        db.session.add(img)
        db.session.commit()
        # save image file to directory
        picture.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    except exc.SQLAlchemyError as e:
        errorMessage = errorType(e)
        return render_template('error.html', message=errorMessage)

    allImages = getImages()
    return render_template('index.html', images=allImages)

# category page
@app.route('/tags/<category>')
def category(category):
    if category not in tags: return render_template('error.html', message="invalid category")
    print('category:', category)
    allImages = getImages(category)
    return render_template('categories.html', images=allImages, category=category)

# favorites page
@app.route('/favorites')
def favorites():
    print('favorites')
    allImages = getImages(None, True)
    return render_template('categories.html', images=allImages, category='favorites')

# delete image
@app.route('/delete/<int:id>')
def delete(id):
    print(request.path)
    prevUrl = request.referrer      # url of the page the request is coming from
    if prevUrl is None: return render_template('error.html', message="invalid URL")  # attempt to delete item from the address bar is not permitted
    
    filename = SavedImages.query.filter_by(id=id).first().filename
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
    SavedImages.query.filter_by(id=id).delete()
    db.session.commit()

    print('deleted')

    prevUrl = prevUrlChecker(prevUrl)       # helper function to check which page sent the request
                                            # home page, favorites page, or tags page  
                                          
    if prevUrl == 'favorites': return redirect(url_for('favorites'))
    elif prevUrl[0] == 'tags': return redirect(url_for('category', category=prevUrl[1]))
    elif prevUrl == 'home': return redirect(url_for('home'))

# favorite/unfavorite image
@app.route('/favorite/<int:id>')
def favorite(id):
    prevUrl = request.referrer      # url of the page the request is coming from
    if prevUrl is None: return render_template('error.html', message="invalid URL")  # attempt to favorite item from the address bar is not permitted

    image = SavedImages.query.filter_by(id=id).first()
    if image.favorite is False: image.favorite = True
    else: image.favorite = False
    db.session.commit()

    print('favorited')    

    prevUrl = prevUrlChecker(prevUrl)       # helper function to check which page sent the request
                                            # home page, favorites page, or tags page  
                                          
    if prevUrl == 'favorites': return redirect(url_for('favorites'))
    elif prevUrl[0] == 'tags': return redirect(url_for('category', category=prevUrl[1]))
    elif prevUrl == 'home': return redirect(url_for('home'))

# error message if the url does not match any of the above
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="nothing found here"), 404