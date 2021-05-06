from app.models import SavedImages

tags = ['home', 'work', 'school', 'art', 'music', 'food', 'travel', 'friends&family', 'others']
imageFormats = ['jpg', 'jpeg', 'png', 'webp']

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

def prevUrlChecker(urlStr):
    
    urlList = urlStr.split('/')  # split url into list spearated by '/'
    print(urlList)

    # "http://127.0.0.1:5000/tags/food/"  ->  ['http:', '', '127.0.0.1:5000', 'tags', 'food', '']

    if 'favorites' in urlList:      # check to see if the previous url is from the favorites page
        return 'favorites'
        
    elif 'tags' in urlList:         # check to see if the previous url is from a category/tags page
        return 'tags', urlList[4]   # and return the category of the page too

    else:                           # last case -> the url is from the home page
        return 'home' 

def fileFormat(filename):       
    if filename.split('.')[-1].lower() not in imageFormats:     # check file format with acceptable formats
        return False
    else:
        return True

def noFileName(filename):       
    if len(filename.split('.')) == 1:       # check if image file has only format and no name
        return True
    else:
        return False

def errorType(e):           # error -> either title already used or image already exists (determined by filename)
    if str(e).count('title') == 2: return "use a different title for your image"
    elif str(e).count('filename') == 2: return "image already exists"