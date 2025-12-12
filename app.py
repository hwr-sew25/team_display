from flask import Flask, render_template, session, request, redirect, url_for
import roslibpy

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

#client = roslibpy.Ros(host='10.20.128.225', port=9090)
#client.run()

#screen_pub = roslibpy.Topic(client, '/current_screen', 'std_msgs/String')

#def publish_screen(screen_name):
#    screen_pub.publish(roslibpy.Message({'data': screen_name}))


@app.route('/')
@app.route('/index')
def index():
    session["active_screen"] = "start"
    return render_template('index.html')

@app.route("/raumwahl")
def raumwahl():
    session["active_screen"] = "raumwahl"
    return render_template("raumwahl.html")

@app.route("/karte")
def karte():
    session["active_screen"] = "karte"
    return render_template("karte.html", direction="left")

@app.route("/set_language/<lang>")
def set_language(lang):
    session['lang'] = lang
    # zurück zur vorherigen Seite
    return redirect(request.referrer or url_for('index'))

@app.route("/error1")
def error_route():
    session["active_screen"] = "error1"
    return render_template("error_route.html")

@app.route("/error2")
def error_tec():
    session["active_screen"] = "error2"
    return render_template("error_tec.html")

if __name__ == "__main__":
    app.run(debug=True)