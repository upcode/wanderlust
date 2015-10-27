""" Models and Database fucntions for Wanderlust app"""
from flask_sqlachemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()
##############################################################################
# Model for Users table


class User(db.model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(10), nullable=True)
    #authenticated= db.Column(db.Boolean, default=False)

    # def is_active(self):
    #     """True, asll users are active"""
    #     return True
    # def get_id(self):
    #     """Return the email address to satisfy Falsk-Login's requirements."""
    #     return self.email

    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated

    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False


    # def __repr__(self):
    #     """Provide helpful representation when printed."""
    #     return "<User user_id=%s email=%s password=%s username=%s>" % (self.user_id, self.email, self.password, self.username, self.age, self.home_location)

# Model for States Table


class State(db.model):
    """States Selection"""
    __tablename__ = "states"

    state_id = db.Column(db.String(2), nullable=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    abb = db.Column(db.String(2), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User state_id=%s state_name=%s state_visit_date=%s>" % (self.state_id, self.state_name, self.state_visit_date)

# Model for User and State Relationship Table to track number of states users has visited
class UserStates(db.model):
    """users and states relationship table"""
    __tablename__ = "userstates"


    id = db.Column(db.Integer, nullable=True, primary_key=True)
    user_id = db.Column(db.ForeignKey('states.state_id'), nullable=False)
    state_id = db.Column(db.String(2), db.ForeignKey('states.state_id'), nullable=False)
    visited_at = db.Column(db.DateTime, nullable=False)

   #Define the relationship to user
    user = db.relationship("User",
                            backref=db.backref("userstates", order_by=user_id))
    #Define the relationship to state
    state = db.relationship("State",
                            backref=db.backref("userstates", order_by=state_id))
    def __repr__(self):
        """Provide helpful representation when printed."""

    return "<Userstates id=%s user_id=%s state_id=%s>" % (self.id, self.user_id, self.state_id)


# Model for Postcard Table


class Postcard(db.model):
    """user upload their picture and send it to social media"""

    __tablename__ = "postcards"

    postcard_id = db.Column(db.Integer, primary_key=True)
    userstate_id = db.Column()

    #Define the relationship to user
    userstate = db.relationship("UserStates",
                            backref=db.backref("postcards", order_by=postcard_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Postcard postcard_id=%s user_id=%s state_id=%s state_visit_date=%s>" % (self.postcard_id, self.user_id, self.state_visit_id, self.score)





##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask App"""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.app = app
    db.init_app(app)

    if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

        from server import app
        connect_to_db(app)
        print "Connected to DB."