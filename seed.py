from model import connect_to_db, db
from model import State
from model import Country
from routes import app

#  relationships

#  from model import UserState, UserStateLandmark, UserCountry, UserTopWorldCity, UserWorldWonder
# helper function, comment out print to disable debugging


def debug():
    """ return message in the console if data loaded successfully"""

    msg = "wanderlust db is seeded"

    print msg



# ###############################################################################
# #D3 STATE

def load_states():
    # open csv file (us_states)
    d3states_file = open("data/d3state_data.csv")
    #read each line
    for line in d3states_file:
        # split on ","   --> list
        line_list = line.split("|")
        # each item in list -->  remove whitespace .strip()
        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()

        state_id, state_abbrevation, state_name = line_list[0], line_list[1], line_list[2]
        print "STATE_ID: %s STATE_ABBRREVATION: %s STATE_NAME: %s" % (state_id, state_abbrevation, state_name)
        # # make State(....) object
        state = State(state_abbrevation=state_abbrevation, state_id=state_id, state_name=state_name)

        # add to session
        db.session.add(state)
        # commit session
    db.session.commit()

    debug()


###############################################################################

# ###############################################################################
# #D3 COUNTRIES


def load_countries():
    # open csv file (us_states)
    d3file = open("data/d3countryseed.csv")

    #read each line
    for line in d3file:
        # split on ","   --> list
        line_list = line.split("|")
        # each item in list -->  remove whitespace .strip()
        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()

        country_id, country_name = line_list[0], line_list[1]
        print "COUNTRY_ID: %s, COUNTRY_NAME: %s" % (country_id, country_name)
        # # make State(....) object
        country = Country(country_id=country_id, country_name=country_name)

        # add to session
        db.session.add(country)
        # commit session
    db.session.commit()

    debug()


###############################################################################
                            # HELPER FUNCTION #
###############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_states()
    load_countries()
