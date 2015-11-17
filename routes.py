
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask import send_from_directory
from werkzeug import secure_filename
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from flask.ext.jsonpify import jsonify
from sqlalchemy import update
# import config_file for external api

# IMPORTED MODEL TABLES TO ROUTES
from model import User, State_Landmark, World_100_City, World_100_Wonder
from model import D3_World_Map, D3_State_Map, Postcard, AdventureList, connect_to_db, db
# IMPORTED MODEL RELATIONSHIP TABLES TO ROUTES

# from model import UserState, UserStateLandmark, UserCountry, UserTopWorldCity UserWorldWonder
# from model import Postcard, UserPostcard, connect_to_db, db

# this is the path to the upload directory
UPLOAD_FOLDER = 'uploads/'
# upload extensions that are allowed
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
app = Flask(__name__)
SECRET_KEY = "not actually a secret"
app.config.from_object(__name__)

app.secret_key = 'RED PANDA'

app.config['UPLOAD_FOLDER'] = 'uploads'

# For a given file, return whether it's an allowed type or not

@app.route('/index')
def index():
    """ testing page"""
    # return render_template('index.html')
    # return render_template('timeline.html')
    # return render_template('teststatemap.html')
    # return render_template('testmap.html')
    # return render_template('amjavascriptmap.html')

##############################################################################
# INDEX PAGE



@app.route('/')
def wanderlust():
    """Homepage."""
    return render_template("wanderlust.html")
#     # return render_template('google.html')


##############################################################################
                            # # LOGIN # #
##############################################################################
# Route ("/login", methods=["POST"]) process login form
# WHERE REQUEST GOES TO FORM HTML FROM action=/login needs to match route route("/login")

# FORM PROCESSING LOGIN

# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("wanderlust.html")

@app.route('/login-process', methods=['POST'])
def process_login():
    """Log user into site, find user in the DB and their
    their user id in the session then if they
     are logged in redirect them to map page"""

     # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    print "form password"
    print password

# check to see if this person exisit and then asign them variable user
    user = User.query.filter_by(email=email).first()
    print "\n \n \n ", user



    if not user:
        flash("No such user")
        return redirect("/")

    elif user.password != password:
        flash("Incorrect password")
        return redirect("/")
    else:
        session["user_id"] = user.user_id

    flash("Logged in")
    # return redirect('/user_id/%s' % user.user_id)
    return redirect('/passport')


# LOG OUT ROUTE

@app.route("/logout")
def process_logout():
    """Log user out by removing user_id from session"""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

##############################################################################
                            # # REGISTER # #
##############################################################################


# WHERE SIGNUP FORM IS PROCESSED
@app.route('/register-process', methods=['POST'])
def register_processed():
    """New user signup form"""

    print "Sign up route is working"

    # Get form variables

    email = request.form["email"]
    # username = request.form["username"]
    password = request.form["password"]

    # query the DB for this user
    # new_user = User(email=email, username=username, password=password)
    new_user = User(email=email, password=password)


    # CHECK BY EMAIL
    # is email in database, returns the user obj
    # if email NOT in database, returns None
    same_email_user = User.query.filter(User.email == email).first()

    if same_email_user:
        flash("Email is already registered. Please signin to your account")
        return redirect("/login")
        # if this is None, (meaning email is not in db) -- this doesn't run.
        # if email is in the databse, this will run.
        # redirct to login flash message please sign this email is registered

    # CHECK BY USERNAME
    same_username = User.query.filter(User.email == email).first()
    if same_username:
        flash("please pick another username")
        return redirect("/login")
        # if have same username register with another username <-- flash
        # redirect login --> form

    db.session.add(new_user)
    db.session.commit()

    # NEED TO STORE USER IN SESSION.
        # need to get the user_id from database
    user = User.query.filter_by(email=email).first()

    flash("User %s added.You have successfully created an account! Welcome to Wanderlust" % email)
    session["user_id"] = user.user_id

    return redirect("/passport")


##############################################################################
                        # #  PASSPORT / PROFILE PAGE # #
##############################################################################

@app.route('/passport')
def passport():
    """wanderlist list where users can update their bucket list of places they want to visit"""
    # query db for users session and under user look for users adventure list with all of their places and pass places into adventure list in passport page
    user_id = session['user_id']
    # this query finds what user has in DB and pulls it out and hopefully jinja
    places = db.session.query(AdventureList.adventure_item).filter(AdventureList.user_id == user_id).all()

    # first_name = db.sessionquery(User.first).filter(User_id==userid).first()
    #if there'sno first name, does it return None?  Error?
    # if None, can you pass None to jinja?

    new_place_list = []
    for item in places:
        new_place_list.append(item[0])

    print new_place_list
    # places = places_query.adventure_item
    # print places

    # print type(places.adventure_item)
    # google_place_key=google_place_key, TODO ADD EXTERNAL FILE FOR API KEYS

    return render_template('passport.html', places=new_place_list)

#################################################################


@app.route('/profile', methods=['POST'])
def profile():
    """ RETURN user profile information"""

    user_id = session["user_id"]
    # from HTML form getting inputs from ajax call
    first = request.form.get('first', None)
    last = request.form.get('last', None)
    username = request.form.get('username', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    quote = request.form.get('quote', None)
    about = request.form.get('about', None)

    print "profile", first, last, city, state, quote, about
    # query db for current user
    # GET the object you want to edit
    # my instance of user class query db to pull out user and its attributes
    user = db.session.query(User).filter_by(user_id=user_id).one()
    #instance is binded to User model attribute and assing it to ajax form

    user.first_name = first
    user.last_name = last
    user.username = username
    user.city = city
    user.state = state
    user.quote = quote
    user.about = about

    db.session.commit()

    # profile_info_data = {"key": value}
    profile_info_data = {"first": first, "last": last, "username": username, "city": city, "state": state, "quote": quote, "about": about}

    # query DB for this user if the unser is none
    print "Profile been has been stored in DB"

    ###make a dictionary, where the key is "first", value is first etc
    return jsonify(profile_info_data)

    # @app.route('/disply-profile-info', methods=['POST'])


@app.route('/adventurelist', methods=['POST'])
def process_list():

    user_id = session["user_id"]
    new_item = request.form['place']
    print "adventurelist", new_item

    new_list_item = AdventureList(user_id=user_id, adventure_item=new_item)

    db.session.add(new_list_item)
    db.session.commit()
    return "New adventure has been stored in DB"


@app.route('/disply-user-adventure-list', methods=['POST'])


@app.route('/passport-dashboard')  # form sumission from passport page
def dashboard():

    address = request.form.get["Street address"]
    city = request.form.get["City"]
    state = request.form.get["State"]
    zipcode = request.form.get["zip code"]
    country = request.form.get["country"]
    des = request.form.get["description"]

    user_id = session["user_id"]

##############################################################################
#AJAX Call for GOOGLE POSTCARD FORM


@app.route('/google-postcard-ajax', methods=['POST'])
def google_postcard_form_ajax():
    """ google address form that prepopulates address"""

    # adding user sessipon
    user_id = session["user_id"]
    # FROM HTML from all variables
    # from HTML form getting inputs from ajax call
    street_number = request.form.get('street_number')
    route_address = request.form.get('route')
    city = request.form.get('locality')
    postal_code = request.form.get('postal_code')
    state = request.form.get("state")
    country = request.form.get('country')
    message = request.form.get('message', None)

    print "google-postcard-ajax", street_number, route_address, city, postal_code, state, country, message

    # commit form information to Database
    db.session. commit()

    postcard_data = {"street_number": street_number, "route": route_address, "city": city, "state": state, "country": country, "message": message}
     # query DB for this user if the unser is been has been stored in DB"

    ###make a dictionary, where the key is "first", value is first etc
    return jsonify(postcard_data)



##############################################################################
# UPLOAD IMAGE

@app.route('/postcard-upload-ajax', methods=['GET', 'POST'])
def postcard():

    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        file = request.files['passport'] # should be passport
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('/passport',
                                    filename=filename))

    return render_template('passport.html')


@app.route('/uploads/<filename>')
def uploaded_postcard(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


##############################################################################
                            # # STATE MAP # #
##############################################################################

@app.route('/state-map')
def state():

    # return render_template('testmap.html')
     return render_template('teststatemap.html')


@app.route('/state-map-ajax')
def state_map():
    """d3 state map where users can click on state and changes colors"""

    # AJAX CALL FOR USER STATE VISIT

    # get current user from session
    user_id = session["user_id"]

    # inputs from d3 state map from click function and consle logging
    state_id = request.form.get('d.id') # id from d3 map
    # state_color = request.form.get('state_color') # color of state

    # print route and state_id, color, date state was visited and user_id
    print 'state-map-ajax', state_id, user_id

    # query for db for user
    # user is my instance, User is my class table look for the feild user_id in db and grab one if user_id == user_id
    user = db.session.query(User).filter_by(user_id=int(user_id)).one()
    user.state_id = state_id
    # user.state_color = state_color
    user.state_name = state_name
    user.visited_at = visited_at

    db.session.commit()
    # return json data which has key adn values
    # removed this "state_color":state_color
    user_state_map_info_data = {"state_id":state_id,"visited_at": visited_at}

    # query DB for this user if the unser is none
    print "state visit has been stored in DB"

    ###make a dictionary, where the key is "first", value is first etc
    return jsonify(user_state_map_info_data)








@app.route('/test', methods=['POST'])
def ajaxtest():
    value = request.form.get('key')
    print value
    print "PING!"
    return "THIS IS COMING BACK FROM THE SERVER"



#########

# var laod_state_map = d3.laod_state_map('load', 'statechange');


##############################################################################
                            # # WORLD MAP # #
##############################################################################
@app.route('/world_map')
def world_map():
    """d3 state map where users can click on country and changes colors"""

    return render_template("world_map.html")



##############################################################################
                        # #  POSTCARDS # #
##############################################################################

##############################################################################

# HELPER FUNCTIONS
##############################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run()
