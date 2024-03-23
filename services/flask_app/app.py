import mlflow
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

from bechdel_test_predictor import BechdelAPI
from bechdel_test_predictor.error import MovieNotFoundError

from mlflow_utils import load_latest_model
from settings import MLFLOW_MODEL_NAME, MLFLOW_TRACKING_URI


load_dotenv(find_dotenv())
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

app = Flask(__name__)

model = load_latest_model(model_name=MLFLOW_MODEL_NAME)
client = BechdelAPI(model=model)


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
