# Clearing the PSQL Database
The PSQL database manages the storage for mlflow. To delete an mlflow run, experiment, or model, it is not enough to simply delete it from the UI or via the CLI. Instead, the backend storage must also be cleared manually. Not doing this causes problems if, for example, an experiment is deleted in the mlflow UI and then a new experiment with the same name is created. This will error, because some state from the old experiment still exists in storage, even if it is not visible from within the mlflow UI. Below are the steps needed to clear the PSQL storage that is used in this app.

First launch the psql database in docker.
```bash
docker compose run -d postgres-db
```

The above command will paste a container id to the terminal. Paste that container id into the command below
```bash
docker exec -it 'paste-container-id'
```

Now that you're inside the psql docker container, you can launch the psql shell
```bash
psql -U postgres
```

Then copy the sql code from the `helpers/clean_up_mlflow.sql` file in this repository, and paste it into the terminal. This code will clear the psql database of all mlflow files.

Exit the psql shell by running `\q`, and then exit the docker container with `exit`.

Finally, stop the PSQL container by running:
```shell
docker stop 'past-container-id'
```