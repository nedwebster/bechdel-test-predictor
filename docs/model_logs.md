# Model Logs
The model predictions are logged to the PSQL database under the `model_logs` table. To view them, follow the steps below:

First launch the psql database in docker.
```bash
docker compose run -d postgres-db
```

The above command will paste a container id to the terminal. Paste that container id into the command below
```bash
docker exec -it 'paste-container-id' sh
```

Now that you're inside the psql docker container, you can launch the psql shell
```bash
psql -U postgres
```

Finally, you can browse the logs by running
```sql
select * from model_logs;
```