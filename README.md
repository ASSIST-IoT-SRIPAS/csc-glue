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

## License

This code is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

Copyright 2025 Systems Research Institute, Polish Academy of Sciences

This work is part of the [ASSIST-IoT project](https://assist-iot.eu/) that has received funding from the EU’s Horizon 2020 research and innovation programme under grant agreement No 957258.
