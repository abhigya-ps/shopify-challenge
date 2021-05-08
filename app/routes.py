from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import SavedImages
from app.helper import tags, prev_url_checker, file_format, no_file_name, error_type, get_images
from sqlalchemy import exc

# home page
@app.route('/')
def home():
    all_images = get_images()
    return render_template('index.html', images=all_images)

# upload image
app.config['UPLOAD_PATH'] = 'app/static/uploads'
@app.route('/', methods=['POST'])
def upload():
    title = request.form['title']
    category = request.form['category']
    picture = request.files['picture']

    if not picture:
        return render_template('error.html', message="no picture uploaded"), 400

    filename = secure_filename(picture.filename)
    if no_file_name(filename) is True:        # check if image file has a name
        return render_template('error.html', message="image has no file name"), 400

    if file_format(filename) is False:       # check if the format of the image file is valid
        return render_template('error.html', message="acceptable formats are jpg, jpeg, png, and webp"), 400

    try:
        # save to database 
        img = SavedImages(title=title, category=category, filename=filename)
        db.session.add(img)
        db.session.commit()
        
        # save image file to directory
        picture.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        
    except exc.SQLAlchemyError as e:    # catch error while writing to database
        error_message = error_type(e)
        return render_template('error.html', message=error_message), 400

    all_images = get_images()
    return render_template('index.html', images=all_images)

# category page
@app.route('/tags/<category>')
def category(category):
    if category not in tags: return render_template('error.html', message="invalid category"), 400
    all_images = get_images(category)
    return render_template('categories.html', images=all_images, category=category)

# favorites page
@app.route('/favorites')
def favorites():
    all_images = get_images(category=None, favorites=True)
    return render_template('categories.html', images=all_images, category='favorites')

# delete image
@app.route('/delete/<int:id>')
def delete(id):
    prev_url = request.referrer      # url of the page the request is coming from

    # attempt to delete item from the address bar is not permitted
    if prev_url is None: return render_template('error.html', message="invalid URL"), 403
    
    filename = SavedImages.query.filter_by(id=id).first().filename
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename)) # delete image file from static/uploads folder
    SavedImages.query.filter_by(id=id).delete()     # delete record from database
    db.session.commit()

    # helper function to check which page sent the request -> home page, favorites page, or tags page 
    prev_url = prev_url_checker(prev_url)
                                          
    if prev_url == 'favorites': return redirect(url_for('favorites'))
    elif prev_url[0] == 'tags': return redirect(url_for('category', category=prev_url[1]))
    elif prev_url == 'home': return redirect(url_for('home'))

# favorite/unfavorite image
@app.route('/favorite/<int:id>')
def favorite(id):
    prev_url = request.referrer      # url of the page the request is coming from

    # attempt to favorite item from the address bar is not permitted
    if prev_url is None: return render_template('error.html', message="invalid URL"), 403

    image = SavedImages.query.filter_by(id=id).first()
    # favorite or unfavorite image based on present state
    if image.favorite is False: image.favorite = True
    else: image.favorite = False
    db.session.commit()

    # helper function to check which page sent the request -> home page, favorites page, or tags page 
    prev_url = prev_url_checker(prev_url)
                                          
    if prev_url == 'favorites': return redirect(url_for('favorites'))
    elif prev_url[0] == 'tags': return redirect(url_for('category', category=prev_url[1]))
    elif prev_url == 'home': return redirect(url_for('home'))

# error message if the url does not match any of the above routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="nothing found here"), 404