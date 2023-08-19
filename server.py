import os
from pprint import pprint
import time
from bottle import FileUpload, redirect, route, run, request, template
from score_file import scores_for_file

LOG_DIR = os.path.join(os.path.dirname(__file__), "tmp", "uploads")


def save_uploaded_file(result_file: FileUpload):
    os.makedirs(LOG_DIR, exist_ok=True)
    now_ms = int(time.time() * 1000)
    file_name = f"{now_ms}_{result_file.filename}"
    result_file.save(os.path.join(LOG_DIR, file_name))


@route("/", method="GET")
def root():
    return """
<form action="results" method="post" enctype="multipart/form-data">
  Resultat-fil i IOF XML-format: <input type="file" name="result_file" />
  <input type="submit" value="Ladda upp" />
</form>
"""


@route("/results", method="POST")
def upload():
    result_file: FileUpload = request.files.get("result_file")
    save_uploaded_file(result_file)
    return template("results", scores=scores_for_file(result_file.file))


if __name__ == "__main__":
    run()
