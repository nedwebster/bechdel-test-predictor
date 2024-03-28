-- Cleans up old deleted Mlflow data in the PSQL database
DELETE FROM experiment_tags WHERE experiment_id=ANY(
    SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
);
DELETE FROM latest_metrics WHERE run_uuid=ANY(
    SELECT run_uuid FROM runs WHERE experiment_id=ANY(
        SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
    )
);
DELETE FROM metrics WHERE run_uuid=ANY(
    SELECT run_uuid FROM runs WHERE experiment_id=ANY(
        SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
    )
);
DELETE FROM tags WHERE run_uuid=ANY(
    SELECT run_uuid FROM runs WHERE experiment_id=ANY(
        SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
    )
);
DELETE FROM params WHERE run_uuid=ANY(
    SELECT run_uuid FROM runs where experiment_id=ANY(
        SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
));
DELETE FROM runs WHERE experiment_id=ANY(
    SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
);
DELETE FROM experiments where lifecycle_stage='deleted';