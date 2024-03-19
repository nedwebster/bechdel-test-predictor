from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

from bechdel_test_predictor import BechdelAPI
from bechdel_test_predictor.error import MovieNotFoundError


load_dotenv(find_dotenv())
app = Flask(__name__)

client = BechdelAPI()


@app.route("/", methods=["GET", "POST"])
def get_prediction():
    if request.method == "POST":
        title = request.form["title"]
        try:
            prediction = client.get_bechdel_prediction(title=title)
            return render_template("index.html", prediction=prediction["prediction"], summary=prediction["summary"])
        except MovieNotFoundError as e:
            return render_template("error.html", error=str(e))
    return render_template("index.html")
