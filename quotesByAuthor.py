import requests
from bs4 import BeautifulSoup, NavigableString
import math, json
import random
import Levenshtein
from langdetect import detect 

json_file_name = "quoteBank.json"

def findAuthorID(author):
    try:
        author = author.replace(" ", "+")
        page = requests.get("https://www.goodreads.com/search?utf8=%E2%9C%93&q=" + author + "&search_type=books&search%5Bfield%5D=author")
        soup = BeautifulSoup(page.text, 'html.parser')
        idLink = soup.find(class_="authorName",href=True)["href"]
        start = idLink.find("show/")
        end = idLink.find("?from")
        authorID = idLink[start+5:end]

        #experimental: trying to find out if the authorID is correct
        nameStart = authorID.find(".")
        authorName = authorID[nameStart+1:].replace("_"," ")
        lDistance = Levenshtein.distance(author,authorName)
        differenceScore = lDistance-len(authorName)+len(author) #bigger is worse

    except:
        print("failed to find author")
        pass
    print("found " + author +" @ " + authorID)
    print("(experimental) difference score = " + str(differenceScore))
    return authorID

def getQuotesByAuthor(author, maxChars, pagesToScrape = None, language = "en"):
    all_quotes = []
    authorID = findAuthorID(author)

    try:
        page = requests.get("https://www.goodreads.com/author/quotes/" + authorID)
        soup = BeautifulSoup(page.text, 'html.parser')
        pages = soup.find(class_="smallText").text
        of = pages.find("of ")
        showing = pages.find("Showing ")
        num_shown = pages[showing+10:of-1]
        total_num = pages[of+3:]
        total_num = total_num.replace(",", "").replace("\n", "")
        num_shown = int(num_shown)
        total_num = int(total_num)

        if pagesToScrape is not None:
            if(pagesToScrape > 1 and pagesToScrape <= total_num):
                pages = pagesToScrape
            elif(pagesToScrape < 1):
                pages = 1
            else:
                pages = math.ceil(total_num/num_shown)
        else:           
            pages = math.ceil(total_num/num_shown)   

    except:
        pages = 1

    print("looking through", pages, "pages") 

    #get author's name
    page = requests.get("https://www.goodreads.com/author/quotes/" + authorID)
    soup = BeautifulSoup(page.text, 'html.parser')
    h1 = soup.find("h1")
    officialName = h1.find_all("a")[1].text
    print("Author's Official Name: " + officialName)

    for i in range(1, pages+1, 1):
        try:
            page = requests.get("https://www.goodreads.com/author/quotes/" + authorID + "?page=" + str(i))
            soup = BeautifulSoup(page.text, 'html.parser')
            print("scraping page", i, " of ", pages)
        except:
            print("could not connect to goodreads")
            break    

        try:
            quote = soup.find(class_="quotes")
            quote_list = quote.find_all(class_="quoteDetails")
        except:
            pass

        for quote in quote_list:
            meta_data = []
        # Get quote's text
            try:
                outer = quote.find(class_="quoteText")
                inner_text = " ".join(outer.strings)   
                midIndex = inner_text.find("―")
                final_quote = " ".join(inner_text[:midIndex].split()).strip()
            except:
                pass 
            if(len(final_quote) < maxChars and len(final_quote) != 0):
                try: 
                    if(detect(final_quote) == language):
                        meta_data.append(final_quote)
                    else:
                        continue
                except:
                    continue
            else:
                continue
                
            #get quote's author
            try:
                meta_data.append(officialName)

            except:
                meta_data.append(None)
            #get quote's tags
            try: 
                title = quote.find(class_="authorOrTitle")
                title = title.nextSibling.nextSibling.text
                title = title.replace("\n", "")
                meta_data.append(title.strip())
            except:
                meta_data.append(None)

            # Get quote's tags
            try:
                tags = quote.find(class_="greyText smallText left").text
                tags = [x.strip() for x in tags.split(',')]
                tags = tags[1:]
                meta_data.append(tags)
            except:
                meta_data.append(None)
            
            # Get number of likes
            try:
                likes = quote.find(class_="right").text
                likes = likes.replace("likes", "")
                likes = int(likes)
                meta_data.append(likes)
            except:
                meta_data.append(None)

            all_quotes.append(meta_data)
    
    return all_quotes

def getAllQuotes(authorsList, maxChars, pagesToScrape = None, language = "en"):
    
    #print("Getting quotes from author " + str(len(authorsList)) + " of " )
    allQuotes = []
    for author in authorsList:
        quotes = getQuotesByAuthor(author, maxChars, pagesToScrape, language)
        for quote in quotes:
            allQuotes.append(quote)

    with open(json_file_name, "w") as write_file:
        json.dump(allQuotes, write_file, indent=4)

def getRandomQuote():
    with open(json_file_name, "r") as read_file:
        quotes = json.load(read_file)
    randomNum = random.randrange(len(quotes)-1)
    print(quotes[randomNum][0])
    print(quotes[randomNum][1])

def getNumQuotes():
    with open(json_file_name, "r") as read_file:
        quotes = json.load(read_file)
    print("total number of quotes: " + str(len(quotes)))
