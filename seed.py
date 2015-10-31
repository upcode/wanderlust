from model import State
from model import User
from model import Landmark
from model import connect_to_db, db
from routes import app

# helper function, comment out print to disable debugging
def debug(msg):
    print msg

###############################################################################
# STATES


def load_states():
    # open csv file (us_states)
    us_states_file = open("data/us_states.csv")
    #read each line
    for line in us_states_file:
        # split on ","   --> list
        line_list = line.split(",")
        # each item in list -->  remove whitespace .strip()
        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()

        code, state, capital = line_list[0], line_list[1], line_list[2]
        print "CODE: %s, STATE: %s, CAPITAL: %s" % (code, state, capital)
        # # make State(....) object
        state = State(state_code=code, name=state, capital=capital)

        # add to session
        db.session.add(state)
    # commit session
    db.session.commit()

    debug "Ya! Success!"


###############################################################################
#USERS

def load_users():
    """opeing csv file and parsing data to enter into database"""
    # open csv file (users)
    user_file = open("data/users.csv")
    #read each line
    #i = 0
    for line in user_file:
        #i += 1
        # split on "| "   --> list
        line_list = line.strip().split("|")
        #print "THE LENGTH IS", len(line_list)
        #print "i is", i
        #print "the line is", line
        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()
        user_id, first_name, last_name, email, username, password, state = line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5], line_list[6]
        print "USER_ID: %s, FIRST_NAME: %s, LAST_NAME: %s, EMAIL: %s, USERNAME: %s,PASSWORD: %s, STATE: %s" % (user_id, first_name, last_name, email, username, password, state)
        # make State(....) object
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email, username=username, password=password, state=state)

        # TODO: handle empty lines at the end

        # add to session and store users from CSV file
        db.session.add(user)
    # commit session commits transaction
    db.session.commit()

    print "Ya! Load Users Table is Success!"

###############################################################################
#LANDMARKS


def load_landmarks():
    """opening csv file and parsing data to enter into database"""
    # open csv file (state_landmarks)
    state_landmark_file = open("data/state_landmarks.csv")
    for line in state_landmark_file:
        line_list = line.split("|")

        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()


        state_name, name = line_list[0], line_list[1]

        # remove any extra "State" at end of state_name
        if (state_name[-5:] == "State") or (state_name[-5:] == "state"):
            state_name = state_name[0:-6]

        print "STATE: %s, NAME: %s" % (state_name, name)

        # for each state, get the state_code
        if state_name == "Washington D.C.":
            state_code = "DC"
        else:
            tup = db.session.query(State.state_code).filter(State.name==state_name).one()
            state_code = tup[0]

        # make State(....) object
        landmark = Landmark(state_code=state_code, name=name)

        # add to session
        db.session.add(landmark)
    # commit session
    db.session.commit()

    print "Ya! Load Landmark Table is Success!"


###############################################################################
                            # HELPER FUNCTION #
###############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_states()

    # Import different types of data
    #load_users()

    # Import different types of data
    load_landmarks()
