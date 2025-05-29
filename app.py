from flask import Flask, render_template, request
from waitress import serve
import json
import fnmatch
import os

app = Flask(__name__)

with open("data/dwyl_5l_set.json") as f:
    WORDS = set(json.load(f))

def match_pattern(pattern, words):
    pattern = pattern.lower()
    return [w for w in words if fnmatch.fnmatch(w, pattern) and len(w) == 5]

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    matches_no_repeat = []
    matches_with_repeat = []
    input_data = {"pattern": "", "blacklist": "", "yellow": ""}

    if request.method == "POST":
        pattern = request.form.get("pattern", "").lower()
        blacklist = set(request.form.get("blacklist", "").lower())
        yellow = set(request.form.get("yellow", "").lower())

        input_data = {
            "pattern": pattern,
            "blacklist": "".join(blacklist),
            "yellow": "".join(yellow),
        }

        matches = match_pattern(pattern, WORDS)

        if blacklist:
            matches = [w for w in matches if not any(c in blacklist for c in w)]

        if yellow:
            matches = [w for w in matches if yellow.issubset(set(w))]

        matches_no_repeat = [w for w in matches if len(set(w)) == len(w)]
        matches_with_repeat = [w for w in matches if len(set(w)) != len(w)]

    return render_template(
        "index.html",
        input_data=input_data,
        matches=matches,
        matches_no_repeat=matches_no_repeat,
        matches_with_repeat=matches_with_repeat,
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)

