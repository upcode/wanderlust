
##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask import send_from_directory
from werkzeug import secure_filename
from flask_debugtoolbar import DebugToolbarExtension

# IMPORTED MODEL TABLES TO ROUTES
from model import User, State, State_Landmark, Country, World_100_City, World_100_Wonder
from model import D3_World_Map, D3_State_Map, Postcard, AdventureList, connect_to_db, db
# IMPORTED MODEL RELATIONSHIP TABLES TO ROUTES

# from model import UserState, UserStateLandmark, UserCountry, UserTopWorldCity UserWorldWonder
# from model import Postcard, UserPostcard, connect_to_db, db

# FILE UPLOADER EXTENSION
UPLOAD_FOLDER = 'postcarduploads/' # filepath where photos are stored
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.secret_key = 'RED PANDA'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##############################################################################

@app.route('/test', methods=["POST"])
def test():
    user_id = request.form["user_id"]
    postcard_id = request.form["postcard_id"]
    created_at = request.form["created_at"]
    user_image = request.form["user_image"]
    return json.dumps({'status': 'OK', 'user_id': user_id, "postcard_id": postcard_id, "created_at": created_at,
     "user_image": user_image})


##############################################################################
# TESTING AJAX
@app.route('/adventure')
def list():
        return render_template("profilepage.html")


@app.route('/adventurelist', methods=['POST'])
def process_list():

    user_id = session["user_id"]
    adventure_list = request.form('adventureList')
    print "adventurelist", adventure_list

    new_list_item = AdventureList(user_id=user_id, adventure_list=adventure_list)

    db.session.add(new_list_item)
    db.session.commit()
    return "New adventure has been stored in DB"
    # return render_template("list.html")


##############################################################################
# UPLOAD POSTCARD ROUTE

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

    return render_template('profilepage.html')

@app.route('/uploads/<filename>')
def uploaded_postcard(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

##############################################################################
# INDEX PAGE

@app.route('/')
def index():
    """Homepage."""
    return render_template('helloworld.html')



# Route ("/login", methods=["POST"]) process login form
# WHERE REQUEST GOES TO FORM HTML FROM action=/login needs to match route route("/login")

# FORM PROCESSING LOGIN

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("wanderlust.html")

@app.route('/login', methods=['POST'])
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

    print user.password


    if not user:
        flash("No such user")
        return redirect("/login")

    elif user.password != password:
        flash("Incorrect password")
        return redirect("/login")
    else:
        session["user_id"] = user.user_id

    flash("Logged in")
    # return redirect('/user_id/%s' % user.user_id)
    return redirect('/profilepage')


# LOG OUT ROUTE

@app.route("/logout")
def process_logout():
    """Log user out by removing user_id from session"""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/login")



##############################################################################


@app.route('/register', methods=['GET'])
def register_form():
    """ show from for user sign up"""

    return render_template('wanderlust.html')

# WHERE SIGNUP FORM IS PROCESSED
@app.route('/register', methods=['POST'])
def register_processed():
    """New user signup form"""

    print "Sign up route is working"

    # Get form variables

    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    # query the DB for this user
    new_user = User(email=email, username=username, password=password)
    user = User.query.filter(User.email == email).first()
    user = User.query.filter(User.username == username).first()
    user = User.query.filter(User.password == password).first()

    # white is varaibles, oranage is DB feildnames

    user = User.query.filter_by(email=email).first()

    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username=username).first()

    flash("User %s added.You have successfully created an account! Welcome to Wanderlust" % email)
    session["username"] = user.username
    db.session.add(new_user)
    db.session.commit()
    return redirect("/d3_state_map")







@app.route("/logout")
def logout():
    """Log user out by removing user_id from session"""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/login")


                    ####  STATE MAP ROUTE ####
##############################################################################

@app.route('/d3_state_map')
def state_map():
    """print hello world making sure sever is running"""

    # get id from ajax request

    # instance from db

    # if it doesnt exist, make it

    # if it does, delete it



# @app.route('/d3_state_map')
# def process_userState_visit():
    # d3statemap_id = request.form['d3statemap_id']
    # user_id =  request.form['user_id'];
    # state_code = request.form['password'];
    # state_name = request.form['state_id']
    # visited_at = request.form["visit_at"];
    # return json.dumps({'status':'OK', 'd3statemap_id': d3statemap_iduser_id, ':user_id': user_id, 'state_code':state_code, 'state_name':state_name,'visited_at':visited_at});


    return render_template("d3_state_map.html")










                        ####  WORLD MAP ROUTE  ####
##############################################################################


@app.route('/d3_world_map')
def world_map():
    """print hello world making sure sever is running"""

    return render_template("d3_world_map.html")







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
