import datetime
import os

from flask import Flask, render_template
import sbd

app = Flask(__name__)


@app.route("/")
def atlas_status():
    # Because we get split messages from the ATLAS system, we slam together
    # all messages received in the same hour.
    paths = []
    active_hour = datetime.datetime.min
    for root, dirs, files in os.walk("/var/iridium/300234063909200"):
        for filename in files:
            if os.path.splitext(filename)[1] != ".sbd":
                continue
            dt = datetime.datetime.strptime(filename[0:13], "%y%m%d_%H%M%S")
            if (dt - active_hour).seconds > 60 * 60:
                active_hour = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
                paths = [os.path.join(root, filename)]
            else:
                paths.append(os.path.join(root, filename))
    payload = ""
    for path in paths:
        payload += sbd.message.MobileOriginatedMessage.read(path).payload
    print payload
    return render_template("atlas_status.html",
            last_heartbeat_datetime=active_hour)


if __name__ == "__main__":
    app.run(debug=True)
