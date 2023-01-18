# ensures a venv exists and, if not, creates it
venv:
	if [ -d src/venv ]; then echo 'pass'; else python3 -m venv src/venv; fi

# clears database and other artifacts
clean:
	rm -f db/data.db

# runs init script
init: venv clean
	src/venv/bin/python3 src/init.py --path db/data.db

# runs scraper script
scrape: venv
	src/venv/bin/python3 src/scrape.py --path db/data.db

# runs parser script
parse: venv
	src/venv/bin/python3 src/parse.py --path db/data.db

# runs index script
index: venv
	src/venv/bin/python3 src/index.py --path db/data.db
