from model import State, User, Country, World100Wonder, World100City, StateLandmark
# relationships
#from model import UserState, UserStateLandmark, UserCountry, UserTopWorldCity, UserWorldWonder
from model import connect_to_db, db
from routes import app

# helper function, comment out print to disable debugging


def debug(msg):
    #debug = True
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

        state_id, state_name, state_capital_name = line_list[0], line_list[1], line_list[2]
        print "STATE_ID: %s, STATE_NAME: %s, STATE_CAPITAL_NAME: %s" % (state_id, state_name, state_capital_name)
        # # make State(....) object
        state = State(state_id=state_id, state_name=state_name, state_capital_name=state_capital_name)

        # add to session
        db.session.add(state)
    # commit session
    db.session.commit()

    #debug "Ya! Success!"

    print "STATE: SUCCESS DATA UPLOAD"


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
        print "USER_ID: %s, FIRST_NAME: %s, LAST_NAME: %s, EMAIL: %s, USERNAME: %s, PASSWORD: %s, STATE: %s" % (user_id, first_name, last_name, email, username, password, state)
        # make State(....) object
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email, username=username, password=password, state=state)

        # TODO: handle empty lines at the end

        # add to session and store users from CSV file
        db.session.add(user)
    # commit session commits transaction
    db.session.commit()

    #debug "Ya! Success!"
    print "USERS: SUCCESS DATA UPLOAD"


###############################################################################
#LANDMARKS


def load_statelandmarks():
    """opening csv file and parsing data to enter into database"""
    # open csv file (state_landmarks)
    state_landmark_file = open("data/us_state_landmarks.csv")
    for line in state_landmark_file:
        line_list = line.split("|")

        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()

        state_name, state_landmark_name = line_list[0], line_list[1]
        # remove any extra "State" at end of state_name
        if (state_name[-5:] == "State") or (state_name[-5:] == "state"):
            state_name = state_name[0:-6]

        print "STATE_NAME: %s, STATE_LANDMARK_NAME: %s" % (state_name, state_landmark_name)

        # for each state, get the state_code
        if state_name == "Washington D.C.":
            state_id = "DC"
        else:
            tup = db.session.query(State.state_id).filter(State.state_name == state_name).one()
            state_id = tup[0]

        # make State(....) object
        landmark = StateLandmark(state_id=state_id, state_landmark_name=state_landmark_name)

        # add to session
        db.session.add(landmark)
    # commit session
    db.session.commit()

    print "LANDMARK: SUCCESS DATA UPLOAD"

###############################################################################
#CONTURIES


def load_countires():
    """opeing csv file and parsing data to enter into database"""
    # open csv file (users)
    country_file = open("data/countries.csv")
    #read each line
    #i = 0
    for line in country_file:
        #i += 1
        # split on "| "   --> list
        line_list = line.strip().split("|")
        #print "THE LENGTH IS", len(line_list)
        #print "i is", i
        #print "the line is", line
        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()
        country_name, country_capital_name = line_list[0], line_list[1]
        print "COUNTRY_NAME: %s, COUNTRY_CAPITAL_NAME: %s" % (country_name, country_capital_name)
        # make country(....) object
        country = Country(country_name=country_name, country_capital_name=country_capital_name)

        # add to session and store users from CSV file
        db.session.add(country)
    # commit session commits transaction
    db.session.commit()

    #debug "Ya! Success!"
    print "COUNTRIES: SUCCESS DATA UPLOAD"


###############################################################################
#WORLD CITY


def load_world100city():
    """opeing csv file and parsing data to enter into database"""
    # open csv file (users)
    #city_list = []
    top_city_file = open("data/world_100_cities.csv")
    for line in top_city_file:
        city_list = line.split()
        #city_list = city_list.strip()
        #city_list.append(line)
        for i in range(len(city_list)):
            city_list[i] = city_list[i].strip()
            city_name = city_list[0]
        print "CITY_NAME: %s" % (city_name)
    city = World100City(city_name=city_name)

    # add to session and store users from CSV file
    db.session.add(city)
    # commit session commits transaction
    db.session.commit()

    print "WORLD100CITY: SUCCESS DATA UPLOAD"
###############################################################################
#WONDERS


def load_world100wonders():
    """opeing csv file and parsing data to enter into database"""
    # open csv file (users)
    #city_list = []
    wonder_file = open("data/world_100_wonders.csv")
    for line in wonder_file:
        wonder_list = line.split()
        #wonder_list = wonder_list.strip()
        #city_list.append(line)
        for i in range(len(wonder_list)):
            wonder_list[i] = wonder_list[i].strip()
            world_wonder_name = wonder_list[0]
        print "WONDER_NAME: %s" % (world_wonder_name)
    wonder = World100Wonder(world_wonder_name=world_wonder_name)

    db.session.add(wonder)
    # commit session commits transaction
    db.session.commit()

print "WORLD100WONDERS: SUCCESS DATA UPLOAD"


###############################################################################
                            # HELPER FUNCTION #
###############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    #load_states()  # DONE
    load_users()
    #load_statelandmarks()  # DONE
    #load_countires()  # DONE
    #load_world100wonders()  # DONE
    #load_world100city()  # DONE
