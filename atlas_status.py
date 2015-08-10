import datetime
import glob
import os

from flask import Flask, render_template
import sbd

PAYLOAD_NAMES = [
        "_power_on",
        "scan_params_temperature",
        "scan_params_pressure",
        "scan_params_humidity",
        "scan_params_meas_prog",
        "scan_params_phi_start",
        "scan_params_phi_stop",
        "scan_params_phi_step",
        "scan_params_theta_start",
        "scan_params_theta_stop",
        "scan_params_theta_step",
        "scan_start_starttime",
        "scan_stop_stoptime",
        "scan_stop_num_points",
        "scan_stop_range_min",
        "scan_stop_range_max",
        "scan_stop_file_size",
        "scan_stop_amplitude_min",
        "scan_stop_amplitude_max",
        "scan_stop_roll",
        "scan_stop_pitch",
        "scan_stop_latitude",
        "scan_stop_longitude",
        "scan_skip_skiptime",
        "scan_skip_reason_code",
        "scan_skip_reason_description",
        "tempmount",
        "solar1",
        "wind1",
        "wind2",
        "solar2",
        "efoy1",
        "efoy2",
        "b1",
        "b2",
        "b3",
        "b4",
        "soc1",
        "ccl1",
        "dcl1",
        "soc2",
        "ccl2",
        "dcl2",
        "soc3",
        "ccl3",
        "dcl3",
        "soc4",
        "ccl4",
        "dcl4",
        ]

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

    last_image_filename = glob.glob("/home/iridiumcam/StarDot/ATLAS_CAM/*.jpg")[-1]

    payload = ""
    for path in paths:
        payload += sbd.message.MobileOriginatedMessage.read(path).payload
    values = dict(zip(PAYLOAD_NAMES, payload.split(",")))
    for key, value in values.iteritems():
        try:
            values[key] = float(value)
        except ValueError:
            pass
    starttime = values["scan_start_starttime"].split("/")
    values["scan_start_starttime"] = datetime.datetime.strptime(
            "{:02d}/{}/{}".format(int(starttime[0]) + 1, starttime[1], starttime[2]),
            "%m/%d/%y %H:%M:%S")

    values["last_heartbeat_datetime"] = active_hour
    values["last_image_src"] = "http://iridiumcam.lidar.io/ATLAS_CAM/" + last_image_filename

    return render_template("atlas_status.html", **values)


if __name__ == "__main__":
    app.run(debug=True)
