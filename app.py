from flask import Flask, render_template, session, request, redirect, url_for
import roslibpy

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

client = roslibpy.Ros(host='localhost', port=9090)

def connect_ros():
    try:
        client.run()
        print("ROS connected successfully!")
    except Exception as e:
        print(f"Failed to connect to ROS: {e}")

connect_ros()

# Verwendete Topics
screen_pub = roslibpy.Topic(client, '/current_screen', 'std_msgs/String')
language_pub = roslibpy.Topic(client, '/language', 'std_msgs/String')
start_pub = roslibpy.Topic(client, '/display/start_druecken', 'std_msgs/Bool')
stop_pub = roslibpy.Topic(client, '/display/stop_druecken', 'std_msgs/Bool')

def publish_screen(screen_name: str):
    try:
        if not client.is_connected:
            connect_ros()

        screen_pub.publish(roslibpy.Message({'data': screen_name}))

    except Exception as e:
        print(f" Failed to publish screen: {e}")

def publish_language(lang: str):
    try:
        if not client.is_connected:
            connect_ros()

        language_pub.publish(roslibpy.Message({'data': lang}))

        print(f"Published language: {lang}")

    except Exception as e:
        print(f"Failed to publish language: {e}")

def publish_start():
    try:
        if not client.is_connected:
            connect_ros()
        msg = roslibpy.Message({'data': True})
        start_pub.publish(msg)
        print("Published START = True")
    except Exception as e:
        print(f"Failed to publish start:", e)


def publish_stop():
    try:
        if not client.is_connected:
            connect_ros()
        msg = roslibpy.Message({'data': True})
        stop_pub.publish(msg)
        print("Published STOP = True")
    except Exception as e:
        print(f"Failed to publish stop:", e)

#def publish_screen(screen_name):
#    screen_pub.publish(roslibpy.Message({'data': screen_name}))

#def publish_language(laguage):
#    screen_pub.publish(roslibpy.Message({'data': language}))

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
    publish_screen("start")
    return render_template('index.html')

@app.route("/raumwahl")
def raumwahl():
    publish_screen("raumwahl")
    publish_start(True)
    return render_template("raumwahl.html")

@app.route("/karte")
def karte():
    publish_screen("karte")

    # später Werte von Directions
    floor = "3"
    wing = "Ost"
    side = "Mittelgang"
    room = " 1.29"

    map_file = get_map(floor, wing)
    direction = get_arrow_direction(side)
    return render_template("karte.html", direction=direction, map_file=map_file, floor=floor, side=side, room=room)

@app.route("/set_language/<lang>")
def set_language(lang):
    session['lang'] = lang
    publish_language(lang)
    return redirect(request.referrer or url_for('index'))

@app.route("/karten_validierung")
def karten_validierung():
    publish_screen("karten_validierung")
    return render_template("karten_validierung.html")

@app.route("/kaffeeautomat")
def kaffeeautomat():
    publish_screen("kaffeeautomat")
    return render_template("kaffeeautomat.html")

@app.route("/muelleimer")
def muelleimer():
    publish_screen("muelleimer")
    return render_template("muelleimer.html")

@app.route("/bildungsangebote")
def bildungsangebote():
    publish_screen("bildungsangebote")
    return render_template("bildungsangebote.html")

@app.route("/karten_ausgabe")
def karten_ausgabe():
    publish_screen("karten_ausgabe")
    return render_template("karten_ausgabe.html")

@app.route("/snackautomat")
def snackautomat():
    publish_screen("snackautomat")
    return render_template("snackautomat.html")

@app.route("/spendenbox")
def spendenbox():
    publish_screen("spendenbox")
    return render_template("spendenbox.html")

@app.route("/geschichte_hwr")
def geschichte_hwr():
    publish_screen("geschichte_hwr")
    return render_template("geschichte_hwr.html")

# status = error (von directions)
@app.route("/error1")
def error_route():
    publish_screen("error1")
    return render_template("error_route.html")

@app.route("/error2")
def error_tec():
    publish_screen("error2")
    return render_template("error_tec.html")

if __name__ == "__main__":
    app.run(debug=True)