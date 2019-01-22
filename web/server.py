from flask import Flask, render_template
import os
#from homeserver.web.routes.waitTime import waittime

app = Flask(__name__)
#app.register_blueprint(waittime, url_prefix='/api/waittime')

@app.route("/", defaults={'u_path': ''})
@app.route('/<path:u_path>')
def hello(u_path):
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)