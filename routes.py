
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
from flask import Flask, render_template, redirect, url_for, request
from model import User, connect_to_db, db
from model import State, connect_to_db, db
from model import State_Landmark, connect_to_db, db
from model import Country, connect_to_db, db
from model import World_100_City, connect_to_db, db
from model import World_100_Wonder, connect_to_db, db
from model import D3_World_Map, D3_State_Map, connect_to_db, db
from model import Postcard, connect_to_db, db

#from d3worldnamefunction import country_dictionary


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
app.secret_key = "RED PANDA"


def debug():
    """ return message in the console if data loaded successfully"""

    msg = "route is working"

    print msg
##############################################################################


                    ####  SERVER RUNNING ROUTE ####
##############################################################################

@app.route('/')
def server():
    """prints server is running and returns hello world if page loads correctly"""
    print "SERVER IS RUNNING"
    return 'HELLO WORLD!'
    debug()


                    ####  LANDING PAGE ROUTE ####
##############################################################################

@app.route('/landing_page')
def landing_page():
        """landing page where users can select to login or sign up"""

        return render_template('landing_page.html')
        debug()


                    ####  LANDING MODAL LOGIN/LOGOUT ####
##############################################################################


                    ####  STATE MAP ROUTE ####
##############################################################################

@app.route('/d3_state_map')
def state_map():
    """print hello world making sure sever is running"""

    return render_template("d3_state_map.html")



                        ####  WORLD MAP ROUTE  ####
##############################################################################


@app.route('/d3_world_map')
def world_map():
    """print hello world making sure sever is running"""

    return render_template("d3_world_map.html")



# def country_dictionary():
#     """returns dictionary of coutry name and id into jsonify file"""
#     country = country_dictionary()
#     country = jsonfiy(country)
#         return render_template("d3_world_map.html", country=country)

##############################################################################



####  GOOGLE MAP POSTCARD ROUTE  ####
##############################################################################


# @app.route('/postcard')
# def Postcard():
#     """google map with drop pins where users can enter places they been"""
#     print "map is working!!!! NAILED IT!!!!"
#     return render_template('google_map.html')

# PASSPORT/ USER ACCOUNT /DASHBOARD
##############################################################################
# this page is for when a user searches for form and looks for cap, state, country, wonders, cities
# it stores in DB that they went to the location and also updates in the view table section
# Started user profrofile page need to combine this route with that page.

# @app.route('/passport')
# def passport_dashboard():
#     """Show list of states, when user clicks on the state
#      D3 map color will change from grey to color of users choice
#      indicating they have visited that state"""

#     # states in table name State is my class querying all us states and returning
#     # states with name
#     print "apples"
#     states = State.query.all()
#     print states
#     return render_template("passport.html", states_in_html=states)
#     #TODO RENDER landmark to this page
#     landmarks = Landmark.query.all()
#     return render_template("passport.html", states_in_html=states, landmarks_in_html=landmarks)


##############################################################################
# @app.route('/passport')
# def list():
#     """Show list of states, when user clicks on the state
#      D3 map color will change from grey to color of users choice
#      indicating they have visited that state"""

#     # states in table name State is my class querying all us states and returning
#     # states with name
#     print "apples"
#     states = State.query.all()
#     print states
#     return render_template("passport.html", states_in_html=states)

#     #TODO RENDER landmark to this page
#     landmarks = Landmark.query.all()

#     return render_template("passport.html", states_in_html=states, landmarks_in_html=landmarks)


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
