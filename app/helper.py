# helper functions that assist view functions in routes.py in sending responses based on requests from the user

from app.models import SavedImages

tags = ['home', 'work', 'school', 'art', 'music', 'food', 'travel', 'friends&family', 'others']
image_formats = ['jpg', 'jpeg', 'png', 'webp', 'jfif']

def prev_url_checker(url_str):
    
    url_list = url_str.split('/')  # split url into list separated by '/'

    # ex. "http://127.0.0.1:5000/tags/food/"  ->  ['http:', '', '127.0.0.1:5000', 'tags', 'food', '']

    if 'favorites' in url_list:      # check to see if the previous url is from the favorites page
        return 'favorites'
        
    elif 'tags' in url_list:         # check to see if the previous url is from one of the category/tags page
        return 'tags', url_list[4]   # and return the category of the page too

    else:                           # last case -> the url is from the home page
        return 'home' 

def file_format(filename):       
    if filename.split('.')[-1].lower() not in image_formats:     # check if file format is an acceptable format
        return False
    else:
        return True

def no_file_name(filename):   
    if len(filename.split('.')) == 1 or filename.split('.')[0] == '':       # check if image file has only format and no name
        return True
    else:
        return False

def error_type(e):           # error -> either title already used or image already exists (determined by filename)
    print('error:', e)
    if str(e).count('title') == 2: return "use a different title for your image"
    elif str(e).count('filename') == 2: return "image already exists"
    else: return "something went wrong with the upload"

def get_images(category=None, favorites=False):

    all_images = []
    if favorites is True:          # return favorited images
        if not SavedImages.query.filter_by(favorite=True): all_images = []
        else: all_images = SavedImages.query.filter_by(favorite=True)

    elif category is None:        # no category mentioned -> show all images
        if not SavedImages.query.all(): all_images = []
        else: all_images = SavedImages.query.all()

    else:                       # shows images of given category
        if not SavedImages.query.filter_by(category=category): all_images = []
        else: all_images = SavedImages.query.filter_by(category=category)
        
    for image in all_images:     # path for images inside uploads folder
        image.filename = 'uploads/' + image.filename

    return all_images