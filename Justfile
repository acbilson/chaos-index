set dotenv-load
set shell := ["/opt/homebrew/bin/fish", "-c"]

# runs a local development Flask server
run:
	src/venv/bin/python src/main.py

# builds a production podman image
build:
  set COMMIT_ID (git rev-parse --short HEAD); \
  podman build \
  -t acbilson/index:latest \
  -t acbilson/index:$COMMIT_ID .

# builds a development podman image.
build-dev:
  podman build \
  --target dev \
  -t acbilson/index-dev:latest .

# starts a production podman image.
start:
  podman run --rm \
  --expose $EXPOSED_PORT -p $EXPOSED_PORT:$EXPOSED_PORT \
  -e "SITE=http://localhost:$EXPOSED_PORT" \
  -e "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" \
  -e "SESSION_SECRET=$SESSION_SECRET" \
  -e "DB_PATH=/mnt/db/data.db" \
  -e "SHARE_PATH=/mnt/share" \
  -v /Users/alexbilson/source/chaos-index/db:/mnt/db \
  -v /Users/alexbilson/source/chaos-index/share:/mnt/share \
  --name index \
  acbilson/index:latest

