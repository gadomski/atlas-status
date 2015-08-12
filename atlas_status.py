import datetime
import glob
import os
import StringIO

from flask import Flask, render_template, make_response

import atlas

app = Flask(__name__)
app.config["MESSAGE_DIRECTORY"] = "/var/iridium/300234063909200"
app.config["IMAGE_DIRECTORY"] = "/home/iridiumcam/StarDot/ATLAS_CAM"


@app.route("/")
def atlas_status():
    values = atlas.get_messages(app.config["MESSAGE_DIRECTORY"])[-1]
    image_glob = os.path.join(app.config["IMAGE_DIRECTORY"], "*.jpg")
    last_image_filename = os.path.basename(sorted(glob.glob(image_glob))[-1])
    values["last_image_src"] = "http://iridiumcam.lidar.io/ATLAS_CAM/" + \
            last_image_filename
    values["last_image_datetime"] = datetime.datetime.strptime(
            os.path.splitext(last_image_filename)[0],
            "ATLAS_CAM_%Y%m%d_%H%M%S")
    return render_template("atlas_status.html", **values)


@app.route("/data.csv")
def atlas_data():
    output = StringIO.StringIO()
    atlas.write_data(app.config["MESSAGE_DIRECTORY"], output)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-type"] = "text/csv"
    return response


if __name__ == "__main__":
    app.config["IMAGE_DIRECTORY"] = "/Users/gadomski/Pictures/ATLAS_CAM"
    app.run(debug=True, host="0.0.0.0")
