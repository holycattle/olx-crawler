echo "Recreating db..."
rm olx_re_data/sql/olx_re_data.db
python scripts/setup_db.py
cd olx_re_data
scrapy crawl olx_housing -a max_page=$1 -o output.json
echo "Done!"
cd ..