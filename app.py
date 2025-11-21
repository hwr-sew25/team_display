from flask import Flask, render_template

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)