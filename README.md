# quotesByAuthor
A simple web scraper for goodreads.com that returns a list of quotes by your favorite authors and saves it to a json file.

## Examples
to get quotes from Shakespeare and JK Rowling that are less than 175 characters:

import quotesByAuthor

getAllQuotes(["Shakespeare", "JK Rowling"], 175)
