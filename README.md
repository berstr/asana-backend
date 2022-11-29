

## Env Variables

    export NEW_RELIC_LICENSE_KEY=XXXX

    export NEW_RELIC_APP_NAME=asana

    export NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
    export NEW_RELIC_INFINITE_TRACING_TRACE_OBSERVER_HOST=<Trace Observer Host>
    export NEW_RELIC_APPLICATION_LOGGING_ENABLED=true
    export NEW_RELIC_APPLICATION_LOGGING_FORWARDING_ENABLED=true

    export ASANA_PERSONAL_TOKEN=XXXX
    export ASANA_USERNAME=XXX
    export ASANA_PORT=XXX
    
Optional - if you run front-end stand-alone (backend either via docker or CLI)

    export ASANA_BACKEND_CORS=true

## CLI

Manual start from command line:

newrelic-admin run-program python3 asana_rest.py

---------------------

## Docker

X.Y is the image tag

    docker build -t bstransky/asana:X.Y .

    docker run -d --name asana -e NEW_RELIC_LICENSE_KEY -e NEW_RELIC_DISTRIBUTED_TRACING_ENABLED -e NEW_RELIC_INFINITE_TRACING_TRACE_OBSERVER_HOST -e NEW_RELIC_APPLICATION_LOGGING_ENABLED -e NEW_RELIC_APPLICATION_LOGGING_FORWARDING_ENABLED -e NEW_RELIC_APP_NAME  -e ASANA_PERSONAL_TOKEN -e ASANA_PORT -e ASANA_USERNAME -v $(pwd)/logs:/logs -p37070:37070 bstransky/asana:X.Y
