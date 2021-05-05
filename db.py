from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# initialize database and create tables
def db_init():
    db.init_app(app)

    # creates the table if the database does not already exist
    with app.app_context():
        db.create_all()