# Image Repository with Python/Flask

image repository that lets a user upload meanigful photos from his or her life with a label indicating what that photo signifies

## Features
- Categorize images with tags
- Delete images
- Favorite/unfavorite images

## Database
- SQLite database - stores id, title for the image, category, and filename of the image
- Image files stored locally within the *static/uploads* folder

## Exception handling
- Image must have a title ex. *John's Birthday April 2021*
- Image must belong to a category/tag ex. *friends & family*
- Image files must have a name and a valid format ex. *birthday-john.jpg*
- Each image must have a unique title
- Each image must have a unique filename

## Testing
- Unit tests based on responses to certain URL requests

## Homepage demo
<img src="images/homepage-demo.JPG" />

## Instructions
- Clone repository and navigate to repository <br>
<code>$ git clone https://github.com/abhigya-ps/shopify-challenge </code> <br>
<code>$ cd shopify-challenge </code> <br><br>
- Create virtual environment and activate it <br>
<code>$ virtualenv venv </code> <br>
<code>$ source venv/scripts/activate </code> <br><br>
- Install packages in the requirements file <br>
<code>$ pip install -r requirements.txt </code> <br><br>
- Initialize database to store image information
  - Start python shell <br>
  <code>$ python -i</code> <br>
  - Create database <br>
  <code>>>> from app import db </code> <br>
  <code>>>> db.create_all() </code> <br>
  <code>>>> exit() </code> <br>
  This creates *images.db* SQLite database inside the *app* folder <br><br>
- Run the flask application <br>
<code>$ python run.py </code> <br><br>
- Visit [localhost:5000](http://localhost:5000/) in a web browser. You are now in the homepage! <br><br>
- Start uploading your favorite images!
