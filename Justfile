set dotenv-load
set shell := ["/opt/homebrew/bin/fish", "-c"]

# runs a local development Flask server
run:
	src/venv/bin/python src/main.py

# runs the build index script locally
run_build_index:
	src/venv/bin/python src/build_index.py

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
  -e "DB_PATH=/mnt/index/db" \
  -e "SHARE_PATH=/mnt/index/share" \
  -v /Users/alexbilson/source/chaos-index/db:/mnt/index/db \
  -v /Users/alexbilson/source/chaos-index/share:/mnt/index/share \
  --name index \
  acbilson/index:latest

# runs the build index script inside the container
build_index:
  podman run --rm \
  --expose $EXPOSED_PORT -p $EXPOSED_PORT:$EXPOSED_PORT \
  -e "SITE=http://localhost:$EXPOSED_PORT" \
  -e "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" \
  -e "SESSION_SECRET=$SESSION_SECRET" \
  -e "DB_PATH=/mnt/index/db" \
  -e "SHARE_PATH=/mnt/index/share" \
  -v /Users/alexbilson/source/chaos-index/db:/mnt/index/db \
  -v /Users/alexbilson/source/chaos-index/share:/mnt/index/share \
  -v /Users/alexbilson/source/chaos-index/logs:/mnt/index/logs \
  --name index \
  acbilson/index:latest \
  python build_index.py

