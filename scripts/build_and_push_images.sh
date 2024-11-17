docker build services/mlflow_server/. -t nedwebster/mlflow_server
docker push nedwebster/mlflow_server

docker build . -t nedwebster/bechdel_flask_app -f services/flask_app/Dockerfile
docker push nedwebster/bechdel_flask_app

docker build . -t nedwebster/bechdel_python_tasks -f services/python_tasks/Dockerfile
docker push nedwebster/bechdel_python_tasks
