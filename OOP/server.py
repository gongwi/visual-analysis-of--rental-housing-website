from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/area")
def area():
    return render_template("area.html")


@app.route("/square")
def square():
    return render_template("square.html")


@app.route("/type")
def house_type():
    return render_template("type.html")


@app.route("/direction")
def direction():
    return render_template("direction.html")


@app.route("/transportation")
def transportation():
    return render_template("transportation.html")


@app.route("/elevator")
def elevator():
    return render_template("elevator.html")


if __name__ == "__main__":
    app.run()
