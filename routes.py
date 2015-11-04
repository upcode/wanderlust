
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
from flask import Flask, render_template, redirect, url_for, request
from model import User, connect_to_db, db
from model import State, connect_to_db, db
from model import StateLandmark, connect_to_db, db
from model import Country, connect_to_db, db
from model import World100City, connect_to_db, db
from model import World100Wonder, connect_to_db, db
#from d3worldnamefunction import country_dictionary

# from . import app, db
# from .forms import EmailPasswordForm
# from .util import ts, send_email
# from .models import User
# from flask.ext.login import login_user

# from . import app
# from .forms import UsernamePasswordForm

# from model import UserState, connect_to_db, db
# from model import UserStateLandmark, connect_to_db, db
# from model import UserCountry, connect_to_db, db
# from model import UserTopWorldCity, connect_to_db, db
# from model import UserWorldWonder, connect_to_db, db
# from model import Postcard, connect_to_db, db
# from model import UserPostcard, connect_to_db, db


#from flask_debugtoolbar import DebugToolbarExtension
#from us import states
app = Flask(__name__)
#GoogleMaps(app)
app.secret_key = "green"

##############################################################################


                    ####  SERVER RUNNING ROUTE ####
##############################################################################

@app.route('/')
def server():
    """prints server is running and returns hello world if page loads correctly"""
    print "SERVER IS RUNNING"
    return 'HELLO WORLD!'


                    ####  LANDING PAGE ROUTE ####
##############################################################################

@app.route('/landing_page')
def landing_page():
        """landing page where users can select to login or sign up"""

        return render_template('landing_page.html')


                    ####  LANDING MODAL LOGIN/LOGOUT ####
##############################################################################

@app.route('/landing_page')
def sign_in_modal():
        """landing page where users can select to login or sign up"""

        return render_template('landing_page.html')

# LOGIN IN PAGE
@app.route('/landing_page/login', methods=['GET', 'POST'])




                    ####  STATE MAP ROUTE ####
##############################################################################

@app.route('/d3_state_map')
def state_map():
    """print hello world making sure sever is running"""



    return render_template("d3_state_map.html",)


@app.route('/state_mapcolor')
def state_map():
    """print hello world making sure sever is running"""



    return render_template("state_mapcolor.html",)



                        ####  WORLD MAP ROUTE  ####
##############################################################################


@app.route('/d3_world_map')
def world_map():
    """print hello world making sure sever is running"""


# def country_dictionary():
#     """returns dictionary of coutry name and id into jsonify file"""
#     country = country_dictionary()

#     country = jsonfiy(country)
#     return render_template("d3_world_map.html", country=country)

##############################################################################


@app.route('/d3_world_map2')
def world_map2():
    """print hello world making sure sever is running"""
    return render_template("d3_world_map2.html")



####  GOOGLE MAP POSTCARD ROUTE  ####
##############################################################################


@app.route('/map')
def Postcard():
    """google map with drop pins where users can enter places they been"""
    print "map is working!!!! NAILED IT!!!!"
    return render_template('google_map.html')

# PASSPORT/ USER ACCOUNT /DASHBOARD
##############################################################################
# this page is for when a user searches for form and looks for cap, state, country, wonders, cities
# it stores in DB that they went to the location and also updates in the view table section
# Started user profrofile page need to combine this route with that page.

@app.route('/passport')
def passport_dashboard():
    """Show list of states, when user clicks on the state
     D3 map color will change from grey to color of users choice
     indicating they have visited that state"""

    # states in table name State is my class querying all us states and returning
    # states with name
    print "apples"
    states = State.query.all()
    print states
    return render_template("passport.html", states_in_html=states)
    #TODO RENDER landmark to this page
    landmarks = Landmark.query.all()
    return render_template("passport.html", states_in_html=states, landmarks_in_html=landmarks)


##############################################################################
@app.route('/passport')
def list():
    """Show list of states, when user clicks on the state
     D3 map color will change from grey to color of users choice
     indicating they have visited that state"""

    # states in table name State is my class querying all us states and returning
    # states with name
    print "apples"
    states = State.query.all()
    print states
    return render_template("passport.html", states_in_html=states)
    #TODO RENDER landmark to this page
    landmarks = Landmark.query.all()
    return render_template("passport.html", states_in_html=states, landmarks_in_html=landmarks)


# HELPER FUNCTIONS
##############################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run()
