import datetime
import glob
import os

from flask import Flask, render_template

import atlas


app = Flask(__name__)


@app.route("/")
def atlas_status():
    values = atlas.get_messages("/var/iridium/300234063909200")[-1]
    last_image_filename = os.path.basename(
            glob.glob("/home/iridiumcam/StarDot/ATLAS_CAM/*.jpg")[-1])
    values["last_image_src"] = "http://iridiumcam.lidar.io/ATLAS_CAM/" + \
            last_image_filename
    return render_template("atlas_status.html", **values)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
