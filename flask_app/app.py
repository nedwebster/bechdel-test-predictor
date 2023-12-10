from dotenv import load_dotenv
from flask import Flask, render_template, request

from bechdel_test_predictor import BechdelTestClient


load_dotenv()
app = Flask(__name__)

client = BechdelTestClient()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        prediction = client.get_bechdel_prediction(title=title)

        return render_template("index.html", prediction=prediction["prediction"], summary=prediction["summary"])

    return render_template("index.html")
