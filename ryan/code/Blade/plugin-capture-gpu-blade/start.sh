#!/bin/bash
# Run the Python script with the arguments passed to the container
exec python3 /app/app.py "$@"
