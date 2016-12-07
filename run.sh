#!/bin/bash
echo "Starting scraper"
scrapy runspider mycinema.py -t json --nolog -o - > "movies.json"
echo "Scrape complete, checking movies with imdb"
python3 checkimdb.py movies.json
