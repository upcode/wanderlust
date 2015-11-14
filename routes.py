
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask import send_from_directory
from werkzeug import secure_filename
from flask_debugtoolbar import DebugToolbarExtension

# IMPORTED MODEL TABLES TO ROUTES
from model import User, State_Landmark, World_100_City, World_100_Wonder
from model import D3_World_Map, D3_State_Map, Postcard, AdventureList, connect_to_db, db
# IMPORTED MODEL RELATIONSHIP TABLES TO ROUTES

# from model import UserState, UserStateLandmark, UserCountry, UserTopWorldCity UserWorldWonder
# from model import Postcard, UserPostcard, connect_to_db, db

# FILE UPLOADER EXTENSION
UPLOAD_FOLDER = 'postcarduploads/'  # filepath where photos are stored
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.secret_key = 'RED PANDA'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##############################################################################
# INDEX PAGE

@app.route('/')
def index():
    """Homepage."""
    return render_template("wanderlust.html")
    # return render_template('google.html')


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
    username = request.form["username"]
    password = request.form["password"]

    # query the DB for this user
    new_user = User(email=email, username=username, password=password)

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
    same_username = User.query.filter(User.username == username).first()
    if same_username:
        flash("please pick another username")
        return redirect("/login")
        # if have same username register with another username <-- flash
        # redirect login --> form

    db.session.add(new_user)
    db.session.commit()

    # NEED TO STORE USER IN SESSION.
        # need to get the user_id from database
    user = User.query.filter_by(username=username).first()

    flash("User %s added.You have successfully created an account! Welcome to Wanderlust" % email)
    session["user_id"] = user.user_id

    return redirect("/passport")


##############################################################################
                        # #  PASSPORT / PROFILE PAGE # #
##############################################################################
@app.route('/passport')
def passport():
    """User profile page"""
    # query db for users session and under user look for users adventure list with all of their places and pass places into adventure list in passport page
    user_id = session['user_id']
    # this query finds what user has in DB and pulls it out and hopefully jinja
    places = db.session.query(AdventureList.adventure_item).filter(AdventureList.user_id == user_id).all()

    new_place_list = []
    for item in places:
        new_place_list.append(item[0])

    print new_place_list
    # places = places_query.adventure_item
    # print places

    # print type(places.adventure_item)

    return render_template('passport.html', places=new_place_list)

##############################################################################


@app.route('/passport', methods=['POST'])
def passport_profile():
    # user_id is dictionary

    user_id = session['user_id']

    username = request.form["username"]
    quote = request.form["quote"]
    state = request.form["state"]
    aboutme = request.forn["about"]
    user_image = request.form["user_image"]
    # query DB for this user's info

    current_user_info = User(user_id=user_id, username=username,
                           state=state, aboutme=aboutme, user_image=user_image, quote=quote)
    #check user in DB, return user obj
    # if username not in DB returns none
    same_user_id = User.query.filter(User.email == email).first()
    if not same_user_id:
        flash("Please register or sign into your own account")
        return redirct("/login")
    same_username = User.query.filter(User.username == username).first()

    if same_username:
        flash("please pick another username")

    if user == None:
        flash('User %s not found.' % username)

        return redirect("/passport")

    else:
        # ORANNGE DB MODAL NAMES # WHITE ABOVE NAMES
        return render_template('passport.html',
                           username=username,
                           state=state, aboutme=aboutme, user_image=user_image)


        db.session.add(current_user_info)
        db.session.commit()


    user = User.query.filter_by(username=username).first()



    return redirect("/passport")

    flash("your profile page is updated")
    # query the DB for this user



@app.route('/postcard/<user_id>', methods=['GET', 'POST'])
def postcard():

    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        file = request.files['postcard']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('passport.html')

@app.route('/uploads/<filename>')
def uploaded_postcard(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#################################################################
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


@app.route('/profile', methods=['POST'])
def profile():
    user_id = session["user_id"]
    user_username = request.form['username']
    user_quote = request.form['quote']
    user_state = request.form['state']
    user_about = request.form['about']
    user_image = request.form['image']
    print "passport-profile", user_username, user_quote, user_state, user_about, user_image


    new_user_profile = User(user_id=user_id, username=user_username, quote=user_quote, state=user_state, aboutme=user_about, user_image=user_image)
    db.session.add(new_list_item)
    db.session.commit()

    return "WINNER!"



    # return render_template("list.html")
##############################################################################
                            # # STATE MAP # #
##############################################################################


@app.route('/state_map')
def state_map():
    """d3 state map where users can click on state and changes colors"""

    return render_template("state_map.html")

    # get id from ajax request

    # instance from db

    # if it doesnt exist, make it

    # if it does, delete it

    # add user from profile session
    user_id = session["user_id"]
    new_state_visit = request.form['d.id']
    print 'state_map', new_state_visit



    new_state_visit = D3_State_Map(user_id=user_id, d3statemap_id=new_state_visit)

    db.session.add(  new_state_visit)
    db.session.commit()
    return "New state has been stored in DB"







    print


# new_visit = User(user_id=user_id, d3statemap_id=state_id)

# user_id= request.form['user_id']
# state_id = request.form['d.id']


# check to see if user has visited state by searching user_id and state_id
# add conditions if user visited state add to db
# if user been to state send message already visited

@app.route('/test', methods=['POST'])
def test():
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
