from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/raumwahl")
def raumwahl():
    return render_template("raumwahl.html")

@app.route("/karte")
def karte():
    return render_template("karte.html", direction="left")

@app.route("/set_language/<lang>")
def set_language(lang):
    session['lang'] = lang
    # zurück zur vorherigen Seite
    return redirect(request.referrer or url_for('index'))

@app.route("/error1")
def error_route():
    return render_template("error_route.html")

@app.route("/error2")
def error_tec():
    return render_template("error_tec.html")

if __name__ == "__main__":
    app.run(debug=True)