
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
from flask import Flask, render_template, redirect, url_for, request, flash, session
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
# TESTING PAGE


@app.route('/login', methods=["GET"])
def login():
        """show login form"""

        # displaying the log in form from the GET request
        return render_template('login.html')

@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site"""
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Incorrect email")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    print user

    session["user_id"] = user.user_id

    flash("Logged in.")
    return redirect("/d3_state_map")

@app.route("/logout")
def logout():
    """Log user out"""

    del session["user_id"]
    flash("Logged out")
    return redirect("/landingpage")

# SIGN UP
##############################################################################
# SIGN UP A NEW USER

@app.route('/login', methods=['GET'])
def signup():
    """ show from for user sign up"""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def signup_processed():
    """New user login information"""

    # Get form variables from FORM in POST request
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')

    new_user = User.query.filter_by(email=email, password=password, username=username).first()

    print new_user

    db.session.add(new_user)
    db.session.commit()

    print new_user

    flash("Thanks for joining wanderlust")
    return redirect('/d3_state_map')







##############################################################################

# @app.route('/landingpage', methods=["GET"])
# def show_login_form():
#         """show login form"""

#         # displaying the log in form from the GET request
#         return render_template('landingpage.html')

# @app.route("/landingpage", methods=["POST"])
# def process_login_form():
#     """Log user into site"""
#     email = request.form['email']
#     password = request.form['password']

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("Incorrect email")
#         return redirect('/landing_page')

#     if user.password != password:
#         flash("Incorrect password.")
#         return redirect("/landingpage")

#     print user

#     session["user_id"] = user.user_id

#     flash("Logged in.")
#     return redirect("/d3_state_map")

# @app.route("/logout")
# def process_logout():
#     """Log user out"""

#     del session["user_id"]
#     flash("Logged out")
#     return redirect("/landingpage")



                    ####  LANDING PAGE ROUTE ####
##############################################################################

# @app.route('/landing_page')
# def landing_page():
#         """landing page where users can select to login or sign up"""

#         return render_template('landing_page.html')

# # ajax request from the html page
# pass varibles to be dictionary
# return from DB using ajax --> to the routes

# Return route below
    # signupUser --> python method
    # /signUpUser.json
    # using jquery Ajax to post from data to python flask

# @app.route('/signUpUser.json', methods=['POST'])
# def signUpUser():
#     """creating a new user"""

# #QUERY MODAL TO MATCH AJAX request
#     username = request.form.get('username')
#     password = request.form.get('password')
#     email = request.form.get('email')
#     new_user = User.query.filter_by(username=username, email=email, password=password).first()
# # If USER matches username, password, and email matches

#     if new_user:
#         return "Ok"
#     else:
#         return "sign up"



# @app.route('/signUp')
# def signUp():
#     """creating a new user"""
#     return render_template('register.html')




# @app.route('/signUpUser', methods=['POST'])
# def signUpUser():
#     user =  request.form['username'];
#     password = request.form['password'];
#     new_user = User.query.filter_by(username=username, password=password).first()

#     return json.dumps({'status':'OK','user':user,'pass':password});

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
