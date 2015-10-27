from flask import Flask
#from us import states
app = Flask(__name__)


@app.route('/')
def hello_world():
    """print hello world making sure sever is running"""
    print "homepage is work"
    return 'Hello World!'

# @app.route('/map')
# def state():
#     return render_temaplate("map.html")


##############################################################################


if __name__ == '__main__':
    app.run()