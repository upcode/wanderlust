""" Models and Database fucntions for Wanderlust app"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()
##############################################################################


##############################################################################
                ##### MODEL FOR USER TABLE ####
##############################################################################


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(64), nullable=False)


    #authenticated= db.Column(db.Boolean, default=False)

# def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = bcrypt.generate_password_hash(password)

#     def is_authenticated(self):
#         return True

#     def is_active(self):
#         return True

#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         return unicode(self.id)

#     def __repr__(self):
#         return '<name - {}>'.format(self.name)

##############################################################################
                ##### MODEL FOR STATES TABLE ####
##############################################################################


class State(db.Model):
    """States Selection"""

    __tablename__ = "states"

    state_code = db.Column(db.String(2), nullable=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    capital = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User state_code=%s state_name=%s>" % (self.state_code, self.name)

##############################################################################
        ##### RELATIONSHIP TABLE FOR USER AND STATE ####
        ### track number of states users has visited ###
##############################################################################


class UserState(db.Model):
    """users and states relationship table"""
    __tablename__ = "user_states"

    user_state_id = db.Column(db.Integer, nullable=True, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    state_code = db.Column(db.String(2), db.ForeignKey('states.state_code'), nullable=False)
    visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

   # #Define the relationship to user table
   #  user = db.relationship("User", backref=db.backref("userstates", order_by=user_id))

   #  #Define the relationship to state table
   #  state = db.relationship("State", backref=db.backref("userstates", order_by=state_code))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Userstates id=%s user_id=%s state_code=%s>" % (self.id, self.user_id, self.state_code)

##############################################################################
                ##### MODEL FOR Landmark TABLE ####
##############################################################################


class Landmark(db.Model):
    """users get badages for any location historical or landmark"""
    __tablename__ = "landmarks"

    landmark_id = db.Column(db.Integer, nullable=True, primary_key=True)
    state_code = db.Column(db.String(2), db.ForeignKey('states.state_code'), nullable=False)
    name = db.Column(db.String(64), nullable=True)

    #Define the relationship to state table
    # state = db.relationship("State", backref=db.backref("userstates", order_by=state_code))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Userstates id=%s user_id=%s state_code=%s>" % (self.id, self.user_id, self.state_code)

##############################################################################
        ##### RELATIONSHIP TABLE FOR USER AND LANDMARKS ####
        ### track number of states users has visited ###
##############################################################################


class UserLandmark(db.Model):
    """users and states relationship table"""
    __tablename__ = "user_landmarks"

    user_landmark_id = db.Column(db.Integer, nullable=True, primary_key=True)

    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    state_code = db.Column(db.String(2), db.ForeignKey('states.state_code'), nullable=False)
    landmark_id = db.Column(db.ForeignKey('landmarks.landmark_id'), nullable=False)

    visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

   #Define the relationship to user table
    user = db.relationship("User", backref=db.backref("userstates", order_by=user_id))

    #Define the relationship to state table
    state = db.relationship("State", backref=db.backref("userstates", order_by=state_code))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Userstates id=%s user_id=%s state_code=%s>" % (self.id, self.user_id, self.state_code)

##############################################################################
##############################################################################

# class RegistrationFrom(Form):
#     username = TextField('Username', [validartors.Length(min=4, max=25)])
#     eamil = TextField('email Address'[validartors.Length(min=6, max=35)])
#     password = PasswordField('New Password',[
#         validartors.Required()
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])])
# confirm = PasswordField('Repear Password')
# accept_tos = BooleansField('I accept the TOS', [validartors.Required()])

##############################################################################
                ##### MODEL FOR POSTCARD TABLE ####
##############################################################################


# class Postcard(db.Model):
#     """user upload their picture and send it to social media"""

#     __tablename__ = "postcards"

#     postcard_id = db.Column(db.Integer, primary_key=True)
#     userstate_id = db.Column(db.Integer, db.ForeignKey("userstates.id"))
#     created_at = db.Column(db.DateTime, default=datetime.now, nullable=True)
#     location = db.Column(db.String(64))
#     description = db.Column(db.Text)

#     #Define the relationship to user
#     userstate = db.relationship("UserStates", backref=db.backref("postcards", order_by=postcard_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Postcard postcard_id=%s user_id=%s state_code=%s>" % (self.postcard_id, self.user_id, self.state_visit_id, self.score)

##############################################################################
                ##### MODEL FOR COUNTRY TABLE ####
##############################################################################

# class Country(db.model):
#     """States Selection"""

#     __tablename__ = "countires"

#     country_id = db.Column(db.String(2), nullable=True, primary_key=True)
#     name = db.Column(db.String(64), nullable=True)

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         return "<User country_id=%s name=%s>" % (self.country_id,
#                                                     self.name)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask App"""
    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # Prepare SQLAlchemy for connection
    db.app = app
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Makes the connection
    db.init_app(app)


if __name__ == "__main__":
# As a convenience, if we run this module interactively, it will leave
# you in a state of being able to work with the database directly.

    from routes import app
    connect_to_db(app)
    print "Connected to DB."
