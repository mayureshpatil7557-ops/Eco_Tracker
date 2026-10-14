import math
import os
import subprocess
import threading
import webbrowser

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Emission factors (typical values, approximate)
TRANSPORT_EF = {  # kg CO2e per passenger-km
    "walking": 0.0,
    "train": 0.041,
    "bus": 0.089,
    "motorcycle": 0.103,
    "car": 0.171,
}
GRID_EF = 0.82  # kg CO2e per kWh, approximate grid average
DIET_EF = {  # kg CO2e per person per day
    "plant": 2.9,
    "vegetarian": 3.8,
    "mixed": 5.6,
    "meat": 7.2,
}
BENCHMARKS = [  # tonnes CO2e per person per year, approximate whole-life averages
    {"name": "World average", "t": 4.7},
    {"name": "1.5 °C pathway by 2030", "t": 2.3},
    {"name": "India average", "t": 2.0},
]
TREE_KG_PER_YEAR = 21

DEFAULTS = {
    "transport": "bus",
    "distance": "10",
    "passengers": "1",
    "electricity": "5",
    "household_size": "3",
    "diet": "mixed",
}


def parse_form(data):
    """Validate the submitted form. Returns (values, error)."""
    form = {key: data.get(key, default).strip() for key, default in DEFAULTS.items()}

    if form["transport"] not in TRANSPORT_EF:
        return form, "Please choose a primary transport."
    if form["diet"] not in DIET_EF:
        return form, "Please choose your typical diet."

    try:
        distance = float(form["distance"])
        electricity = float(form["electricity"])
        household = int(float(form["household_size"]))
        passengers = int(float(form["passengers"] or 1))
    except ValueError:
        return form, "Please enter valid numbers."

    if not 0 <= distance <= 150:
        return form, "Daily distance must be between 0 and 150 km."
    if not 0 <= electricity <= 50:
        return form, "Daily electricity use must be between 0 and 50 kWh."
    if not 1 <= household <= 10:
        return form, "Household size must be between 1 and 10 people."
    if form["transport"] == "car" and not 1 <= passengers <= 8:
        return form, "People sharing the car must be between 1 and 8."

    return {
        "transport": form["transport"],
        "diet": form["diet"],
        "distance": distance,
        "electricity": electricity,
        "household": household,
        "passengers": passengers if form["transport"] == "car" else 1,
    }, None


def calculate(v):
    transport = TRANSPORT_EF[v["transport"]] * v["distance"] / v["passengers"]
    electricity = v["electricity"] / v["household"] * GRID_EF
    food = DIET_EF[v["diet"]]
    day = transport + electricity + food
    return {
        "transport": transport,
        "electricity": electricity,
        "food": food,
        "day": day,
        "year": day * 365 / 1000,
    }


def build_tips(v, c):
    tips = []
    eff = TRANSPORT_EF[v["transport"]] / v["passengers"]

    if v["transport"] in ("car", "motorcycle"):
        saved = (eff - TRANSPORT_EF["train"]) * v["distance"] * 156
        if saved > 5:
            tips.append({
                "title": "Take the metro or train three days a week",
                "text": "Rail emits about a quarter of what a petrol car does per passenger-kilometre.",
                "saving": saved,
            })
    if v["transport"] == "car" and v["passengers"] < 4 and v["distance"] > 0:
        base = TRANSPORT_EF["car"] * v["distance"] * 365
        tips.append({
            "title": "Add one more person to your car",
            "text": "Carpooling splits the same tailpipe emissions between more people.",
            "saving": base / v["passengers"] - base / (v["passengers"] + 1),
        })
    if v["transport"] == "bus" and v["distance"] > 0:
        saved = (TRANSPORT_EF["bus"] - TRANSPORT_EF["train"]) * v["distance"] * 365
        if saved > 5:
            tips.append({
                "title": "Switch to an electric train where you can",
                "text": "Rail is the lowest-emission way to cover long daily distances.",
                "saving": saved,
            })
    if c["electricity"] > 0.3:
        tips.append({
            "title": "Cut household electricity by 20%",
            "text": "LED lighting, a 5-star AC and switching appliances fully off all add up.",
            "saving": c["electricity"] * 0.2 * 365,
        })
    if v["diet"] == "meat":
        tips.append({
            "title": "Move to a mixed diet",
            "text": "Swap red meat for chicken, eggs or pulses a few days a week.",
            "saving": (DIET_EF["meat"] - DIET_EF["mixed"]) * 365,
        })
    if v["diet"] == "mixed":
        tips.append({
            "title": "Go vegetarian a few days a week",
            "text": "Dal, rajma, paneer and seasonal vegetables have a much smaller footprint than meat.",
            "saving": (DIET_EF["mixed"] - DIET_EF["vegetarian"]) * 365 * 0.5,
        })
    if v["diet"] == "vegetarian":
        tips.append({
            "title": "Lean on plant protein more often",
            "text": "Replacing dairy-heavy meals with pulses and grains trims food emissions further.",
            "saving": (DIET_EF["vegetarian"] - DIET_EF["plant"]) * 365 * 0.5,
        })

    tips.sort(key=lambda t: t["saving"], reverse=True)
    tips = tips[:3]
    fillers = [
        {"title": "Buy local and seasonal food",
         "text": "Less transport and storage means fewer emissions on every plate.", "saving": 0},
        {"title": "Keep doing what you are doing",
         "text": "Your habits are already well below average. Share them with friends and family.", "saving": 0},
    ]
    while len(tips) < 3:
        tips.append(fillers[len(tips) - 1 if len(tips) else 0])
    return tips[:3]


def build_donut(c):
    """Arc lengths for the SVG donut (circle r=78)."""
    circumference = 2 * math.pi * 78
    total = c["day"] or 1
    arcs, start = [], 0.0
    for key in ("transport", "electricity", "food"):
        share = c[key] / total
        arcs.append({
            "key": key,
            "share": share,
            "dash": max(0.0, share * circumference - 2),
            "offset": -start * circumference,
            "circumference": circumference,
        })
        start += share
    return arcs


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/lifestyle")
def lifestyle():
    return render_template("lifestyle.html", form=DEFAULTS, error=None)


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "GET":
        return redirect(url_for("lifestyle"))

    values, error = parse_form(request.form)
    if error:
        return render_template("lifestyle.html", form={**DEFAULTS, **request.form.to_dict()}, error=error), 400

    c = calculate(values)
    donut = build_donut(c)

    bench = BENCHMARKS + [{"name": "Your estimate", "t": c["year"], "you": True}]
    bench.sort(key=lambda b: b["t"], reverse=True)
    top = max(b["t"] for b in bench) or 1
    for b in bench:
        b["width"] = b["t"] / top * 100

    return render_template(
        "results.html",
        c=c,
        donut=donut,
        bench=bench,
        tips=build_tips(values, c),
        trees=round(c["year"] * 1000 / TREE_KG_PER_YEAR),
    )


URL = "http://127.0.0.1:5000"


def open_in_chrome():
    """Open the site in Google Chrome (falls back to the default browser)."""
    print(" * Opening Chrome at " + URL, flush=True)
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if os.path.exists(path):
            subprocess.Popen([path, URL])
            return
    try:
        # Works when Chrome is registered with Windows (the usual case)
        subprocess.Popen(["cmd", "/c", "start", "", "chrome", URL])
    except OSError:
        webbrowser.open(URL)


if __name__ == "__main__":
    # In debug mode Flask starts twice; only open the browser from the first process.
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(2.0, open_in_chrome).start()
    app.run(debug=True)