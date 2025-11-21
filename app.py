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

@app.route("/set_language/<lang>")
def set_language(lang):
    session['lang'] = lang
    # zurück zur vorherigen Seite
    return redirect(request.referrer or url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)