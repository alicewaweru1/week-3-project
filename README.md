# Jumia Scraper

Run `jumia_scrape.py` to scrape phone listings from Jumia Kenya and save results to `jumia_phones.csv` and `jumia_phones.xlsx`.

If `EXCHANGE_RATE_API_KEY` is set, the script will also add a `Price (USD)` column. Without the key, it still saves the CSV and Excel files.

Set `EXCHANGE_RATE_API_KEY` in the environment or in `secrets.txt` as:

```
EXCHANGE_RATE_API_KEY=your_key
```
