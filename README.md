# csc-glue

Glue component for Construction site controller

The recommended way to use this is via the provided Docker image. Just run: `docker run -it --rm DOCKER-IMAGE-NAME`

Environment variables:
- `GLUE_CSC_ENDPOINT_CONFIG` – SPARQL Update / Select endpoint for the config graph
- `GLUE_CSC_ENDPOINT_WORKERS` – SPARQL Update / Select endpoint for the workers graph
- `GLUE_LTSE_POSTGREST_ENDPOINT` – PostgREST endpoint for the LTSE
- `GLUE_POLL_INTERVAL` – Interval in seconds between polling the LTSE
- `GLUE_MQTT_HOST` – MQTT broker host
- `GLUE_MQTT_PORT` – MQTT broker port
