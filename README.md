# quotesByAuthor
A simple web scraper for goodreads.com that returns a list of quotes by your favorite authors and saves it to a json file.

To use, simply open getQuotes.py, edit the list of authors to your liking, and then run the script.

## Required Packages
pip install requests
pip install beautifulsoup4
pip install Levenshtein
pip install langdetect

## Examples
to get quotes from Shakespeare and JK Rowling that are less than 175 characters:

import quotesByAuthor

getAllQuotes(["Shakespeare", "JK Rowling"], 175) // saves all the quotes to a json file

getRandomQuote() // displays a random quote from the json file
