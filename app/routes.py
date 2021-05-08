from flask import request, render_template, Response, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import SavedImages
from app.helper import get_images, prev_url_checker, tags, file_format, no_file_name, error_type
from sqlalchemy import exc

@app.route('/')
def home():
    print('home')
    all_images = get_images()
    return render_template('index.html', images=all_images)

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
    if no_file_name(filename) is True:        # check if image file has a name
        return render_template('error.html', message="image has no file name")

    if file_format(filename) is False:       # check if the format of the image file is valid
        return render_template('error.html', message="acceptable formats are jpg, jpeg, png, and webp")

    try:
        # save to database 
        img = SavedImages(title=title, category=category, filename=filename)
        db.session.add(img)
        db.session.commit()
        # save image file to directory
        picture.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    except exc.SQLAlchemyError as e:
        error_message = error_type(e)
        return render_template('error.html', message=error_message)

    all_images = get_images()
    return render_template('index.html', images=all_images)

# category page
@app.route('/tags/<category>')
def category(category):
    if category not in tags: return render_template('error.html', message="invalid category")
    print('category:', category)
    all_images = get_images(category)
    return render_template('categories.html', images=all_images, category=category)

# favorites page
@app.route('/favorites')
def favorites():
    print('favorites')
    all_images = get_images(None, True)
    return render_template('categories.html', images=all_images, category='favorites')

# delete image
@app.route('/delete/<int:id>')
def delete(id):
    print(request.path)
    prev_url = request.referrer      # url of the page the request is coming from
    if prev_url is None: return render_template('error.html', message="invalid URL")  # attempt to delete item from the address bar is not permitted
    
    filename = SavedImages.query.filter_by(id=id).first().filename
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
    SavedImages.query.filter_by(id=id).delete()
    db.session.commit()

    print('deleted')

    prev_url = prev_url_checker(prev_url)       # helper function to check which page sent the request
                                            # home page, favorites page, or tags page  
                                          
    if prev_url == 'favorites': return redirect(url_for('favorites'))
    elif prev_url[0] == 'tags': return redirect(url_for('category', category=prev_url[1]))
    elif prev_url == 'home': return redirect(url_for('home'))

# favorite/unfavorite image
@app.route('/favorite/<int:id>')
def favorite(id):
    prev_url = request.referrer      # url of the page the request is coming from
    if prev_url is None: return render_template('error.html', message="invalid URL")  # attempt to favorite item from the address bar is not permitted

    image = SavedImages.query.filter_by(id=id).first()
    if image.favorite is False: image.favorite = True
    else: image.favorite = False
    db.session.commit()

    print('favorited')    

    prev_url = prev_url_checker(prev_url)       # helper function to check which page sent the request
                                            # home page, favorites page, or tags page  
                                          
    if prev_url == 'favorites': return redirect(url_for('favorites'))
    elif prev_url[0] == 'tags': return redirect(url_for('category', category=prev_url[1]))
    elif prev_url == 'home': return redirect(url_for('home'))

# error message if the url does not match any of the above
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="nothing found here"), 404