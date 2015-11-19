
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
from datetime import datetime

# IMPORTED MODEL TABLES TO ROUTES
from model import User, State, User_State, Postcard, AdventureList, connect_to_db, db
# IMPORTED MODEL RELATIONSHIP TABLES TO ROUTES
# from model import UserState, UserStateLandmark, UserCountry, UserTopWorldCity UserWorldWonder
# from model import Postcard, UserPostcard, connect_to_db, db

##############################################################################
app = Flask(__name__)
app.secret_key = 'RED PANDA'
app.config.from_object(__name__)



##############################################################################
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
app.config['UPLOAD_FOLDER'] = 'uploads'
##############################################################################

# INDEX PAGE

@app.route('/index')
def index():
    """ Index page where I test few functions
     and make sure routes are connected """
    return render_template('flipcard.html')
    # return render_template('index.html')
    # return render_template('timeline.html')
    # return render_template('teststatemap.html')
    # return render_template('testmap.html')
    # return render_template('amjavascriptmap.html')
    # return render_template('mocpostcard.html')



##############################################################################
                            # # LOGIN # #
##############################################################################


@app.route('/', methods=['GET'])
def wanderlust():
    """Show login form."""

    return render_template("wanderlust.html")

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
        return redirect("/")
        # if this is None, (meaning email is not in db) -- this doesn't run.
        # if email is in the databse, this will run.
        # redirct to login flash message please sign this email is registered

    # CHECK BY USERNAME
    same_username = User.query.filter(User.email == email).first()
    if same_username:
        flash("please pick another username")
        return redirect("/")
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

@app.route('/state_map')
def d3_state_map():

    # return render_template('testmap.html')
     return render_template('state_map.html')

# AJAX CALL FOR ADDING STATE VISIT TO DB

@app.route('/state-map-ajax-add', methods=["POST"])
def state_map():
    """ state map where users can click on state and changes colors"""
    # data is presented in DB
    # DB: STATE_ID: 1 STATE_ABBRREVATION: AL STATE_NAME: Alabama

# AJAX CALL FOR USER STATE VISIT

    # get current user from session
    user_id = session["user_id"]
    print user_id

    # inputs from state map in console.log [feature.id] = state_id feature = state
    state_id = request.form.get('feature_id')
    print state_id

    # print route and state_id, user_id
    print 'state-map-ajax-add', state_id, user_id

    # querying DB for user_session
    # current_user == instance in User Model querying DB feild for user_id grab one if user_id == user_id
    states_visited = db.session.query(User_State).filter_by(user_id=user_id).all()
    # querying DB for state_id from user_session from Ajax post call filter DB by state_id and get one
    state = db.session.query(State).filter_by(state_id=state_id).one()
    print "cupcakes", state.state_name

    user_state = User_State(state_id=state_id, user_id=user_id, visted_at=datetime.now())

    return "success!"
    # # CONDITONS:
    #     # if user == to user_id in DB and state_id not in DB add state_id as a visit
    # if current_user == user_id:
    #     if state_id != state_id:

    #         # query DB for state_name
    #         state_name = db.session.query(State).filter_by(state_name=state_name).one()

    #     flash("Congrulations on another state visit. %s has been added to your Dashboard" % state_name)
    #     print(state_name)

    #     # add user state visit to DB if user hasnt visited state
    # db.session.add(state_id)
    # db.seesion.commit

    # #TODO: add count to by DB in HMTL hidden feild as count start at 0 and then increment each one


    # # querying DB for user's state visit count. Updating user_state_count --> DB
    # update_state_count = State.state_count + 1
    # db.session.query(State).filter(D3_State_Map.state_id==state_id).update({D3_State_Map.state_count:update_state_count})
    #     # updating count to DB
    # db.seesion.commit()

    # # return json data which has key values
    # # removed this "state_color":state_color
    # # yellow is vaibles i assigned and white is DB model variables
    # user_state_map_info_data = {"state_id": state_id, "visited_at": visited_at, "update_state_count":state_count}
    # ###make a dictionary, where the key is "first", value is first etc
    # return jsonify(user_state_map_info_data)


# AJAX CALL FOR ADDING STATE VISIT TO DB

@app.route('/state-map-ajax-remove')
def removeStateVisit():
    """delete function for removing state visit"""
    user_id = session["user_id"]
    print user_id

    print 'state-map-ajax-remove', state_id, user_id

    current_user = db.session.query(D3_State_Map).filter_by(user_id=int(user_id)).first()
    state_visit = db.session.query(D3_State_Map).filter_by(state_id=int(state_id)).one()
    state_name = db.session.query(D3_State_Map).filter_by(state_name=state_name).one()
    visited_at = db.session.query(D3_state_Map).filter_by(visit_at=visit_at).one()
    print current_user, state_visit, state_name, visit_at

    if current_user == user_id:
        if state_id == state_id:
            flash("State already been visited on %s" % visited_at)

        else:
            # if user clicks yes remove visit from DB
            if state_id == state_id:
                flash("State has visit has been removed")
                return(state_id)


    db.session.delete(state_id)
    db.session.commit()

    # querying DB for user's state visit count. Deleting user_state_count --> DB
    delete_state_count = D3_State_Map.state_count + 1
    db.session.query(D3_State_Map).filter(D3_State_Map.state_id==state_id).update({D3_State_Map.state_count:delete_state_count})
        # updating count to DB
    db.session.commit()

    # return json data which has key values
    # removed this "state_color":state_color
    # yellow is vaibles i assigned and white is DB model variables
    user_state_map_info_data = {"state_id": state_id, "visited_at": visited_at, "update_state_count":state_count}
        # make a dictionary, where the key is "first", value is first etc
    return jsonify(user_state_map_info_data)


# AJAX CALL FOR LOAD USERS SESSION OF STATE MAP



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
