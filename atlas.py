from collections import defaultdict
import datetime
import os

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


def get_messages(directory):
    # Because we get split messages from the ATLAS system, we slam together
    # all messages received in the same hour.
    paths = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if os.path.splitext(filename)[1] != ".sbd":
                continue
            dt = datetime.datetime.strptime(filename[0:13], "%y%m%d_%H%M%S")
            hour = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
            paths[hour].append(os.path.join(root, filename))
    messages = []
    for dt, path in sorted(paths.items(), key=lambda path: path[0]):
        payload = ""
        path.sort()
        for p in path:
            payload += sbd.message.MobileOriginatedMessage.read(p).payload
        if len(payload.split(",")) != len(PAYLOAD_NAMES):
            continue
        values = dict(zip(PAYLOAD_NAMES, payload.split(",")))
        values["last_heartbeat_datetime"] = dt
        starttime = values["scan_start_starttime"].split("/")
        values["scan_start_starttime"] = datetime.datetime.strptime(
                "{0:02d}/{1}/{2}".format(int(starttime[0]) + 1, starttime[1], starttime[2]),
                "%m/%d/%y %H:%M:%S")
        for key, value in values.iteritems():
            try:
                values[key] = float(value)
            except (ValueError, TypeError):
                pass
        messages.append(values)
    return messages


if __name__ == "__main__":
    import csv
    import sys
    messages = get_messages("/var/iridium/300234063909200")
    fieldnames = ["last_heartbeat_datetime"] + PAYLOAD_NAMES
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for message in messages:
        writer.writerow(message)
