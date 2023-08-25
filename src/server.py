#!/usr/bin/env python

import os
import time
from bottle import FileUpload, route, run, request, template

from parse_iof_xml import parse_iof_xml_result_list
from scoring import scored_class_result

LOG_DIR = os.path.join(os.path.dirname(__file__), "tmp", "uploads")


def save_uploaded_file(result_file: FileUpload):
    os.makedirs(LOG_DIR, exist_ok=True)
    now_ms = int(time.time() * 1000)
    file_name = f"{now_ms}_{result_file.filename}"
    result_file.save(os.path.join(LOG_DIR, file_name))


@route("/", method="GET")
def root():
    return template("index")


@route("/results", method="POST")
def upload():
    result_file: FileUpload = request.files.get("result_file")
    save_uploaded_file(result_file)
    result_list = parse_iof_xml_result_list(result_file.file)
    return template(
        "results",
        event_name=result_list["event"]["event_name"],
        class_results=[
            scored_class_result(class_result)
            for class_result in result_list["class_results"]
        ],
    )


if __name__ == "__main__":
    run(server="bjoern", host="0.0.0.0", port=80)
