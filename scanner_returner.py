from flask import Flask, render_template
from datetime import datetime
from edit_firebase import *
import socket

firebase_init()

app = Flask(__name__)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return str(IP)


ip = get_ip()

print(ip)


def check_event_exist(event):
    event_list = read("")
    print(event_list.keys())
    if event in event_list.keys():
        return True
    else:
        return False


def authenticate_hash(event, hash):
    response = read(f"/{event}/{hash}")
    print(f"raw response: {response}")

    if response != None:
        response["person_exist"] = True
        current_time = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        if response["count"] == False:
            save(f"/{event}/{hash}/count", True)
            save(f"/{event}/{hash}/time", current_time)
            response["time"] = current_time

    else:
        response = {"person_exist": False}

    print(f"return response: {response}")
    return response


@app.route("/scan/<event>")
def scan(event):
    if check_event_exist(event):
        return render_template("scan.html", event=event, ip=ip)
    else:
        return "No such event -_-"
    # replace javascript code with event name (in api fetch)


@app.get("/<event>/<hash>")
def read_user(event, hash):
    return authenticate_hash(event, hash)


app.run(host=ip, port=443, ssl_context="adhoc")
