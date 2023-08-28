#!/usr/bin/env python

import os
import time
from bottle import FileUpload, route, run, request, template

from parse_iof_xml import parse_iof_xml_result_list
from scoring import COMPETITION_CLASSES, UNFINISHED_STATUSES, score_result, scored_class_result
from storage import read_event_result_list, save_event_result_list, series_for_event

LOG_DIR = os.path.join(os.path.dirname(__file__), "tmp", "uploads")


def save_uploaded_file(result_file: FileUpload):
    os.makedirs(LOG_DIR, exist_ok=True)
    now_ms = int(time.time() * 1000)
    file_name = f"{now_ms}_{result_file.filename}"
    result_file.save(os.path.join(LOG_DIR, file_name))


def make_class_result_tables(current_event_result, previous_event_results):
    tables = {}
    for class_name in ["D14", "H14", "D12", "H12", "D10", "H10"]:
        class_rows = {}
        total_score = {}
        for event_result in previous_event_results + [current_event_result]:
            if not event_result:
                continue
            class_results = event_result["class_results"][class_name]
            for person_id, result in class_results["results"].items():
                score = score_result(result)
                if score:
                    total_score.setdefault(person_id, []).append(score)
                    class_rows[person_id] = {
                        "name": result["person_name"],
                        "team": result["team"],
                        "unfinished": result["status"] in UNFINISHED_STATUSES,
                    }
        for person_id, result in current_event_result["class_results"][class_name][
            "results"
        ].items():
            class_rows[person_id]["current_score"] = score_result(result)
        for person_id, point_list in total_score.items():
            sorted_points = sorted(point_list, reverse=True)
            class_rows[person_id]["total_score"] = sum(sorted_points[:3])
            class_rows[person_id]["num_competitions"] = len(sorted_points)
            class_rows[person_id]["fourth_score"] = int(
                len(sorted_points) > 3 and sorted_points[3]
            )
            class_rows[person_id]["fifth_score"] = int(
                len(sorted_points) > 4 and sorted_points[4]
            )
        tables[class_name] = sorted(
            class_rows.values(),
            key=lambda x: (
                x["total_score"],
                x["num_competitions"],
                x["fourth_score"],
                x["fifth_score"],
            ),
            reverse=True,
        )
    return tables


@route("/", method="GET")
def root():
    return template("index")


@route("/results", method="POST")
def upload():
    result_file: FileUpload = request.files.get("result_file")
    save_uploaded_file(result_file)
    result_list = parse_iof_xml_result_list(result_file.file)
    save_event_result_list(result_list)
    other_event_ids = series_for_event(result_list["event"]["event_id"])
    other_event_results = [
        read_event_result_list(event_id)
        for event_id in other_event_ids
        if event_id != result_list["event"]["event_id"]
    ]
    return template(
        "results",
        event_name=result_list["event"]["event_name"],
        result_tables=make_class_result_tables(result_list, other_event_results),
    )


if __name__ == "__main__":
    run(server="cheroot", host="0.0.0.0", port=8080)
