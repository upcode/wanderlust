
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
import os.path
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask import send_from_directory
from werkzeug import secure_filename
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from flask.ext.jsonpify import jsonify
from datetime import datetime


# IMPORTED MODEL TABLES TO ROUTES
from model import User, State, User_State, Postcard, AdventureList, connect_to_db, db
app = Flask(__name__)

UPLOAD_FOLDER = '/uploads'



##############################################################################
app.config.from_object(__name__)
##############################################################################
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'RED PANDA'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

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


@app.route('/register-process', methods=['POST'])
def register_processed():
    """New user signup form"""

    print "Sign up route is working"

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    # query the DB for this user
    new_user = User(email=email, password=password)

    # check DB by email
    same_email_user = User.query.filter(User.email == email).first()
    # only users that registered or login will be redircted
    if same_email_user:
        flash("Email is already registered. Please signin to your account")
        return redirect("/")

    # check user by username --> contdion to check username authentic
    same_username = User.query.filter(User.email == email).first()
    if same_username:
        flash("please pick another username")
        return redirect("/")

    db.session.add(new_user)
    db.session.commit()

    # query db by email to to redirct user to passport page in thier user_session
    user = User.query.filter_by(email=email).first()

    flash("User %s added.You have successfully created an account! Welcome to Wanderlust" % email)
    session["user_id"] = user.user_id

    return redirect("/passport")


##############################################################################
                        # #  PASSPORT / PROFILE PAGE # #
##############################################################################

@app.route('/passport')
def passport():
    """wanderlist list where users can update their bucket
    list of places they want to visit"""

    user_id = session['user_id']
   # query to find users previous list items and loads when user logs into account page
    places = db.session.query(AdventureList.adventure_item).filter(AdventureList.user_id == user_id).all()

    # take users adventure list and loads their list when page loads
    new_place_list = []
    for item in places:
        new_place_list.append(item[0])

    print new_place_list

    return render_template('passport.html', places=new_place_list)

#################################################################
        # AJAX profile form on passport page

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
    user = db.session.query(User).filter_by(user_id=user_id).one()

    # ajax request inputs
    user.first_name = first
    user.last_name = last
    user.username = username
    user.city = city
    user.state = state
    user.quote = quote
    user.about = about

    db.session.commit()

    # profile_info_data = {"key": value}
    profile_info_data = {"first": first, "last": last, "username": username,
     "city": city, "state": state, "quote": quote, "about": about}

    # query DB for this user if the unser is none
    print "Profile been has been stored in DB"

    return jsonify(profile_info_data)

    # @app.route('/disply-profile-info', methods=['POST'])


##############################################################################
                            # # STATE MAP # #
##############################################################################

@app.route('/state_map')
def d3_state_map():

    # return render_template('testmap.html')
     return render_template('state_map.html')


@app.route('/state-map-ajax-add', methods=["POST"])
def state_map():
    """ state map where users can click on state and changes colors
    STATE_ID: 1 STATE_ABBRREVATION: AL STATE_NAME: Alabama
    """

    # AJAX CALL FOR USER STATE VISIT

    # get current user from session
    user_id = session["user_id"]
    print user_id

    # inputs from state map in console.log [feature.id] = state_id feature = state
    state_id = request.form['feature_id']
    print state_id


    state = db.session.query(State).filter_by(state_id=state_id).one()


    user_state_obj = User_State(state_id=state_id, user_id=user_id, visited_at=datetime.now())


    # TODO: make the object be added
    db.session.add(user_state_obj)
    db.session.commit()


    # TODO: query datbase for the information to go into this json

    user_state_json_data = {"state_id": state.state_id, "state_name": state.state_name, "visited_at": user_state_obj.visited_at}


    return jsonify(user_state_json_data)


@app.route('/state-map-ajax-remove', methods=['POST'])
def removeStateVisit():
    """delete function for removing state visit"""

    user_id = session["user_id"]
    print user_id

    state_id = request.form.get('feature_id')
    state = db.session.query(State).filter_by(state_id=state_id).one()

    user_state_obj = db.session.query(User_State).filter(User_State.user_id == user_id, User_State.state_id == state_id).first()
    print user_state_obj

    user_state_json_data = "error"

    if user_state_obj:

        db.session.delete(user_state_obj)
        db.session.commit()

        user_state_json_data = {"state_id": state_id, "state_name": state.state_name, "visited_at": user_state_obj.visited_at}


    return jsonify(user_state_json_data)


###############################################################################
@app.route('/request-user-state-map-ajax-load', methods=['POST'])
def get_users_states():

    user_id = session['user_id']

    #query user in DB for this session
    user_states_visits = db.session.query(User_State).filter_by(user_id=user_id).all()
    # querying users states in User_States Table
    user_state_json_data = db.session.query(User_State).filter_by(state_id=state_id, state_name=state_name, user_id=user_id)
    if request.method == 'POST':
        user_states_data = json.loads(request.form.get('data'))

    # convert python object to json
    user_state_json_data = json.dumps(obj)
    print 'json: %s' % user_state_json_data
    # convert json to python object
    user_state_json_data = json.loads(user_state_json_data)

    return render_template('state_map.html', json=user_states_data )


##############################################################################
                            # # BUCKET LIST # #
##############################################################################

             # AJAX adventure list on passportpage

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


@app.route('/passport-dashboard')
def dashboard():

    address = request.form.get["Street address"]
    city = request.form.get["City"]
    state = request.form.get["State"]
    zipcode = request.form.get["zip code"]
    country = request.form.get["country"]
    des = request.form.get["description"]

    user_id = session["user_id"]

##############################################################################
                 # # GOOGLE FORM API PLACE ADDRESS FORM # #
##############################################################################

#AJAX google addresss from on passport page

@app.route('/google-postcard-ajax', methods=['POST'])
def google_postcard_form_ajax():
    """ google address form that prepopulates address"""

    user_id = session["user_id"]

    # input from ajax call from HTML form
    street_number = request.form.get('street_number')
    route_address = request.form.get('route')
    city = request.form.get('locality')
    postal_code = request.form.get('postal_code')
    state = request.form.get("state")
    country = request.form.get('country')
    message = request.form.get('message', None)

    print "google-postcard-ajax", street_number, route_address, city, postal_code, state, country, message

    # commit form information to Database
    db.session.commit()

    postcard_data = {"street_number": street_number, "route": route_address, "city": city, "state": state, "country": country, "message": message}

    return jsonify(postcard_data)

##############################################################################
                 # # IMAGE UPLAOD FORM ROUTE # #
##############################################################################

# UPLOAD IMAGE

# @app.route('/ajax_upload')
# def pic():
#     """List the uploads."""
#     # uploads = Upload.query.all()
#     # return render_template('list.html', uploads=uploads)
#     render_template('/pic.html')

#     return

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     """Upload a new file."""
#     if request.method == 'POST':
#         save(request.files['upload'])
#         return redirect(url_for('passport'))
#     return render_template('upload.html')


# @app.route('/delete/<int:id>', methods=['POST'])
# def remove(id):
#     """Delete an uploaded file."""
#     upload = Upload.query.get_or_404(id)
#     delete(upload)
#     return redirect(url_for('index'))



# @app.route('/postcard-upload-ajax', methods=['GET', 'POST'])
# def postcard():

#     def allowed_file(filename):
#         return '.' in filename and \
#         filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#     if request.method == 'POST':
#         file = request.files['passport'] # should be passport
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('/passport',
#                                     filename=filename))

#     return render_template('passport.html')






##############################################################################
                            # # WORLD MAP # #
##############################################################################
@app.route('/world_map')
def world_map():
    """d3 state map where users can click on country and changes colors"""

    return render_template("world_map.html")

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
