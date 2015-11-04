""" Models and Database fucntions for Wanderlust app"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    password = db.Column(db.String(128), nullable=False, unique=True)
    state = db.Column(db.String(64), nullable=False)
    user_image = db.Column(db.Unicode(128))

    # @hybrid_property
    # def password(self):
    #     return self._password

    # @password.setter
    # def _set_password(self, plaintext):
    #     self._password = bcrypt.generate_password_hash(plaintext)

#############################################################################
        #### RELATIONSHIP TABLE FOR USER AND STATE ####
        ## records users states they have visited  ###
##############################################################################
#Associative Users and States


# class UserState(db.Model):
#     """Relationship table for users and states: where users states will be recorded"""
#     #creating table name
#     __tablename__ = "user_states"

#     # defining what table will look like in DB
#     user_state_id = db.Column(db.Integer, autoincrement=True, nullable=True, primary_key=True)
#     user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
#     state_id = db.Column(db.String(2), db.ForeignKey('states.state_id'), nullable=False)
#     state_capital_name = db.Column(db.ForeignKey('states.state_capital_name'), nullable=False)
#     visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)
#     state_id = db.Column(db.String(2), db.ForeignKey('states.state_id'), nullable=False)

#    #Define the relationship to user table
#     user = db.relationship("User", backref=db.backref("userstatecapitals", order_by=user_id))

#     #Define the relationship to state table
#     state = db.relationship("State", backref=db.backref("userstatecapitals", order_by=state_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<UserState user_state_id=%s user_id=%s state_id=%s state_capital_name=%s>" % (self.user_state_id, self.user_id, self.state_id, state_capital_name)


# ### records number of states users has visited ###
# ##############################################################################

# class UserStateLandmark(db.Model):
#     """users and landmark relationship table"""

#     __tablename__ = "user_state_landmarks"

#     user_landmark_id = db.Column(db.Integer, autoincrement=True, nullable=True, primary_key=True)
#     user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
#     state_landmark_id = db.Column(db.ForeignKey('landmarks.state_landmark_id'), nullable=False)
#     visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

#    #Define the relationship to user table
#     users = db.relationship("User", backref=db.backref("user_landmarks", order_by=user_id))

#     #Define the relationship to state table
#     states = db.relationship("State", backref=db.backref("user_landmarks", order_by=state_landmark_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<UserStateLandmark user_landmark_id=%s user_id=%s state_landmark_id=%s visited_at=%s>" % (self.user_landmark_id, self.user_id, self.landmark_id, self.visited_at)



#         ## records number of countries users has visited ###
# # ##############################################################################
# # many to many realtionships

# class UserCountry(db.Model):
#     """users and country relationship table"""
#     __tablename__ = "user_countries"

#     user_country_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
#     user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
#     country_id = db.Column(db.String(64), db.ForeignKey('countries.country_id'), nullable=False)
#     visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

#    #Define the relationship to user table
#     users = db.relationship("User", backref=db.backref("user_countries", order_by=user_id))

#     #Define the relationship to state table
#     countries = db.relationship("Country", backref=db.backref("user_countries", order_by=country_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<UserCountry user_country_id=%s user_id=%s country_id=%s>" % (self.user_country_id, self.user_id, self.country_id)

#         ### records number of wold cities users has visited ###
#  ##############################################################################


# class UserWorld100City(db.Model):
#     """users and states relationship table"""
#     __tablename__ = "user_world_cities"

#     user_world_top_city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
#     top_world_city_id = db.Column(db.ForeignKey('top_world_cities.top_world_city_id'), nullable=False)
#     visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

#    #Define the relationship to user table
#     uers = db.relationship("User", backref=db.backref("user_world_cities", order_by=user_id))

#     #Define the relationship to state table
#     top_cities = db.relationship("TopWorldCity", backref=db.backref("user_world_cities", order_by=top_world_city_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<UserTopWorldCity user_world_top_id=%s user_id=%s>" % (self.user_world_top_id, self.user_id,)



#         ### records number of world wonders users has visited ###
# ##############################################################################


# class UserWorld100Wonder(db.Model):
#     """users and world wonders relationship table"""
#     __tablename__ = "user_world_wonders"

#     user_wonder_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
#     world_wonder_id = db.Column(db.ForeignKey("world_wonders.world_wonder_id"), nullable=True)
#     visited_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

#    #Define the relationship to user table
#     user = db.relationship("User", backref=db.backref("user_world_wonders", order_by=user_id))

#     #Define the relationship to state table
#     wonders = db.relationship("UserWorldWonder", backref=db.backref("user_world_wonders", order_by=world_wonder_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<UsersWorldWonder user_wonders_id=%s user_id=%s wonder_name=%s>" % (self.user_wonder_id, self.user_id, self.wonder_id)


#                 ### records users states they have visited  ###
# ##############################################################################

# class UserPostcard(db.Model):
#     """user upload their picture and send it to social media"""

#     __tablename__ = "user_postcards"

#     user_postcard_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.ForeignKey('postcards.user_id'))
#     postcard_id = db.Column(db.Integer, db.ForeignKey('postcards.postcard_id'))

#     #Define the relationship to user
#     user = db.relationship("UserPostcard", backref=db.backref("user", order_by=userpostcard.user_id))
#     #Define the relationship to user table
#     postcard = db.relationship("Postcard", backref=db.backref("user_postcards.postcard_id", order_by=postcards.postcard_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Postcard user_postcard_id=%s user_id=%s postcard_id>" % (self.user_postcard_id, self.user_id, postcard_id,)

##############################################################################
                ##### MODEL FOR POSTCARD TABLE ####
##############################################################################
# postcard table


class Postcard(db.Model):
    """user upload their picture and send it to social media"""

    __tablename__ = "postcards"

    postcard_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'))
    image_title = db.Column(db.Unicode(64))
    postcard_image = db.Column(db.Unicode(128))
    description = db.Column(db.Text)
    Address = db.Column(db.String(64))
    state_stamp_image = db.Column(db.Unicode(128))
    world_stamp_image = db.Column(db.Unicode(128))
    google_map_pins = db.Column(db.Integer, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Postcard postcard_id=%s user_id=%s created_at=%s>" % (self.postcard_id, self.user_id)


##############################################################################
                ##### MODEL FOR STATES TABLE ####
##############################################################################


class State(db.Model):
    """States abbrevation, state name and Capital name Table"""

    __tablename__ = "states"

    state_id = db.Column(db.String(2), nullable=True, primary_key=True)
    state_name = db.Column(db.String(64), nullable=True)
    state_capital_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<State state_id=%s state_name=%s state_capital_name=%s>" % (self.state_id, self.state_name, state_capital_name)


##############################################################################
                ##### MODEL FOR STATE Landmark TABLE ####
##############################################################################
#Landmark


class StateLandmark(db.Model):
    """Landmark Table"""
    __tablename__ = "state_landmarks"

    state_landmark_id = db.Column(db.Integer, nullable=True, primary_key=True)
    state_id = db.Column(db.String(2), db.ForeignKey('states.state_id'), nullable=False)
    state_landmark_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<StateLandmark state_landmark_id=%s state_id=%s state_landmark_name=%s>" % (self.landmark_id, self.state_id, self.state_landmark_name)


##############################################################################
                ##### MODEL FOR COUNTRY TABLE ####
##############################################################################


class Country(db.Model):
    """Country and Capitals Table"""

    __tablename__ = "countries"

    country_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    country_name = db.Column(db.String(64), nullable=False)
    country_capital_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Country country_id=%s country_name=%s, country_capital_name=%s >" % (self.country_id, self.country_name, self.country_capital_name)

#############################################################################
                ##### MODEL FOR  WORLD 100 CITITES TABLE ####
##############################################################################


class World100City(db.Model):
    """Top 100 Cities in the World"""

    __tablename__ = "world_cities"

    world_city_id = db.Column(db.Integer, autoincrement=True, nullable=True, primary_key=True)
    world_city_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<World100City world_citites_id=%s world_cities_name=%s>" % (self.world_city_id,
                                                    self.world_city_name)

#############################################################################
                ##### MODEL FOR 100 WONDERS OF THE WORLD ####
##############################################################################
# 100 Wonders of the world


class World100Wonder(db.Model):
    """100 wonders of the world"""

    __tablename__ = "world_wonders"

    world_wonder_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    world_wonder_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<World100Wonder world_wonder_id=%s world_wonder_name=%s>" % (self.world_wonder_id, self.world_wonder_name)


##### HELPER FUNCTIONS ####
##############################################################################


def connect_to_db(app):
    """Connect the database to our Flask App"""
    # Configure to use our POSTGRES database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgressql:///localhost/wdatabasedb'

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
