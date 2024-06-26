from flask import Flask, render_template, request

from bechdel_test_predictor import BechdelAPI
from bechdel_test_predictor.error import MovieNotFoundError
from bechdel_test_predictor.mlflow import MlflowModel, load_latest_model


app = Flask(__name__)
model = load_latest_model(model_name=MlflowModel.name)
client = BechdelAPI(model=model)


@app.route("/", methods=["GET", "POST"])
def get_prediction():
    if request.method == "POST":
        title = request.form["title"]
        try:
            prediction = client.get_bechdel_prediction(title=title)
            return render_template(
                "index.html",
                title=prediction["title"],
                prediction=prediction["prediction"],
                summary=prediction["summary"],
            )
        except MovieNotFoundError as e:
            return render_template("error.html", error=str(e))
    return render_template("index.html")
