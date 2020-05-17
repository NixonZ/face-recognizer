import flask from flask
import time
app = flask(__name__)

@app.route('time')
def get_current_time():
    return {'time':time.time()}