from flask import Flask, render_template, session, request, redirect, url_for
import roslibpy

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

client = roslibpy.Ros(host='10.20.128.225', port=9090)

def connect_ros():
    try:
        client.run()
        print("ROS connected successfully!")
    except Exception as e:
        print(f"Failed to connect to ROS: {e}")

connect_ros()

def publish_screen(screen_name: str):
    try:
        if not client.is_connected:
            connect_ros()

        screen_pub.publish(roslibpy.Message({'data': screen_name}))

    except Exception as e:
        print(f" Failed to publish screen: {e}")

# Verwendete Topics
screen_pub = roslibpy.Topic(client, '/current_screen', 'std_msgs/String')

def publish_screen(screen_name):
    screen_pub.publish(roslibpy.Message({'data': screen_name}))

def get_arrow_direction(side: str) -> str:
    side = side.lower()

    if side == "mittelgang":
        return "down"
    
    if side == "links":
        return "left"
    
    if side == "rechts":
        return "right"

    # fallback fehlt
    
    
def get_map(floor: str, wing: str) -> str:
    floor = floor.upper()      
    wing = wing.lower()        

    if wing == "ost":
        wing = "links"
    elif wing == "west":
        wing = "rechts"

    if floor == "EG":
        filename = f"EG_{wing}.svg" 
    else:   filename = f"{floor}OG_{wing}.svg"

    # fallback fehlt

    return f"images/karten/{filename}"


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

    # später Werte von Directions
    floor = "3"
    wing = "Ost"
    side = "Mittelgang"

    map_file = get_map(floor, wing)
    direction = get_arrow_direction(side)
    return render_template("karte.html", direction=direction, map_file=map_file, floor=floor, side=side)

@app.route("/set_language/<lang>")
def set_language(lang):
    session['lang'] = lang
    # zurück zur vorherigen Seite
    return redirect(request.referrer or url_for('index'))

 # ROS publish
 #   language_pub.publish(
  #      roslibpy.Message({'data': lang})
   # )

    #return redirect(request.referrer or url_for('index'))

@app.route("/karten_validierung")
def karten_validierung():
    session["active_screen"] = "karten_validierung"
    return render_template("karten_validierung.html")

@app.route("/kaffeeautomat")
def kaffeeautomat():
    session["active_screen"] = "kaffeeautomat"
    return render_template("kaffeeautomat.html")

@app.route("/muelleimer")
def muelleimer():
    session["active_screen"] = "muelleimer"
    return render_template("muelleimer.html")

@app.route("/bildungsangebote")
def bildungsangebote():
    session["active_screen"] = "bildungsangebote"
    return render_template("bildungsangebote.html")

@app.route("/karten_ausgabe")
def karten_ausgabe():
    session["active_screen"] = "karten_ausgabe"
    return render_template("karten_ausgabe.html")

@app.route("/snackautomat")
def snackautomat():
    session["active_screen"] = "snackautomat"
    return render_template("snackautomat.html")

@app.route("/spendenbox")
def spendenbox():
    session["active_screen"] = "spendenbox"
    return render_template("spendenbox.html")

@app.route("/geschichte_hwr")
def geschichte_hwr():
    session["active_screen"] = "geschichte_hwr"
    return render_template("geschichte_hwr.html")

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