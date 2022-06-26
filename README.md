# ranobesDownloader

Downloads a ranobes story to an html file, it can then be converted by calibre.

## Requirements

`Python3`

`pip install beautifulsoup4`

`pip install selenium`

`pip install chromedriver_py`

If you're not using MacOS, modify the line

`CHROMIUM_PATH = "/Applications/Chromium.app/Contents/MacOS/Chromium"`

to your Chromium executable. Google Chrome works as well.

## Usage

`python3 scraper.py URL` where URL is the URL of the first chapter.
