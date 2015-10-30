
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
from flask import Flask, render_template, redirect, url_for, request
from model import State, connect_to_db, db
from model import Landmark
#from flask_debugtoolbar import DebugToolbarExtension
#from us import states
app = Flask(__name__)
#GoogleMaps(app)
app.secret_key = "LDK"

##############################################################################


##############################################################################

@app.route('/')
def hello_world():
    """print hello world making sure sever is running"""
    print "homepage is work"
    return 'Hello World!'
##############################################################################


@app.route('/landing_page')
def landing_page():
        """landing page where users can select to login or sign up"""
        return render_template('landing_page.html')

##############################################################################


# @app.route("/login")
# def login_form():
#     username = request.form.get("username")
#     pwd = request.form.get("pwd")
#     return render_template("login.html", username=username, pwd=pwd)


##############################################################################

# @app.route("/register")
# def login_form():
#     username = request.form.get("username")
#     pwd = request.form.get("pwd")
#     return render_template("login.html", username=username, pwd=pwd)

@app.route('/map')
def google_map():
    """google map"""
    print "map is working!!!! NAILED IT!!!!"
    return render_template('google_map.html')


@app.route('/states')
def state_list():

    """Show list of states"""

    # states in table name State is my class querying all us states and returning
    # states with name
    print "apples"
    states = State.query.all()
    print states
    return render_template("states.html", states_in_html=states)
#TODO RENDER landmark to this page
    landmarks = Landmark.query.all()
    return render_template("states.html", states_in_html=states, landmarks_in_html=landmarks)

# @app.route('/postcard', methods=["GET", "POST"])
# def postcard():
#     """postcard page where users can search for location"""

#     return render_template("postcard.html", location=location, city=location_city, state=location_state, country=location_country, lat=location_lat, lag=location_lng)


##############################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run()
