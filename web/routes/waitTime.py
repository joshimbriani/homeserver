from flask import Blueprint

waittime = Blueprint('waittime', __name__)

@waittime.route('/')
def show():
    return "wait time"