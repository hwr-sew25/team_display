from flask import Flask, render_template, session, request, redirect, url_for
import roslibpy
import requests     
import time  
from threading import Thread


app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

latest_directions = None

client = roslibpy.Ros(host='localhost', port=9090)

DIRECTIONS_API = "http://10.20.228.19:5001"


def connect_ros():
    try:
        client.run()
        print("ROS connected successfully!")
    except Exception as e:
        print(f"Failed to connect to ROS: {e}")

connect_ros()
client.node_name = "/display_ui_node"

# Verwendete Topics
screen_pub = roslibpy.Topic(client, '/current_screen', 'std_msgs/String')
language_pub = roslibpy.Topic(client, '/language', 'std_msgs/String')
start_pub = roslibpy.Topic(client, '/start_druecken', 'std_msgs/Bool')
stop_pub = roslibpy.Topic(client, '/stop_druecken', 'std_msgs/Bool')
#poi_pub = roslibpy.Topic(client, '/poi', 'std_msgs/String')

def directions_listener():
    global latest_directions

    while True:
        try:
            response = requests.get(f"{DIRECTIONS_API}/api/display/steps")

            if response.status_code == 200:
                data = response.json()

                if data.get("room_id"):
                    print("\nNeue Wegbeschreibung erhalten!")
                    print(f"Raum: {data['room_id']}")
                    print(f"Wing: {data['wing']}")
                    print(f"Floor: {data['floor']}")
                    print(f"Side: {data['side']}")
                    print(f"Steps: {data['steps']}")
                    print(f"Additional Info: {data['additional_info']}")
                    print(f"Timestamp: {data['timestamp']}")

                    latest_directions = data 

        except Exception as e:
            print(f"Fehler im Directions Listener: {e}")

        time.sleep(1)

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

#def publish_poi(poi: str):
#    try:
#        if not client.is_connected:
#            connect_ros()

#        language_pub.publish(roslibpy.Message({'data': poi}))

#        print(f"Published language: {poi}")

#    except Exception as e:
#        print(f"Failed to publish language: {e}")

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
    
    
def get_map(floor: str, wing: int) -> str:
    floor = floor.upper()              

    if wing == 1:
        wing = "links"
    elif wing == 2:
        wing = "rechts"

    if floor == "EG":
        filename = f"EG_{wing}.svg" 
    else:   filename = f"{floor}OG_{wing}.svg"

    return f"images/karten/{filename}"


@app.route('/')
@app.route('/index')
def index():
    publish_screen("start")
    return render_template('index.html')

@app.route("/raumwahl")
def raumwahl():
    publish_screen("raumwahl")
    publish_start()
    return render_template("raumwahl.html")

@app.route("/karte")
def karte():
    publish_screen("karte")

    global latest_directions

    floor = latest_directions["floor"]
    wing = latest_directions["wing"]
    side = latest_directions["side"]
    room = latest_directions["room_id"]
    steps = latest_directions["steps"]

    map_file = get_map(floor, wing)
    direction = get_arrow_direction(side)

    return render_template(
        "karte.html",
        direction=direction,
        map_file=map_file,
        floor=floor,
        side=side,
        room=room,
        steps=steps
    )

@app.route("/set_language/<lang>")
def set_language(lang):
    session['lang'] = lang
    publish_language(lang)
    return redirect(request.referrer or url_for('index'))

@app.route("/stop", methods=["POST"])
def stop_action():
    publish_stop()
    return redirect(url_for("index"))

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
    listener_thread = Thread(target=directions_listener, daemon=True)
    listener_thread.start()

    app.run(debug=True)
