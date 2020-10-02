import requests

#the https response is a dictionary, the items value is a list of books, each book is a dictionary

#function that pulls google ID for a given title and author
def getBookID(title, author):
    queryStr = makeQueryStr(title, author)
    payload = {"q": queryStr}
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload)
    #print(r.status_code)
    #print(r.url)
    if r.status_code==200:
        dict = r.json()
        items = dict["items"]
        topBook = items[1]
        bookID = topBook["id"]
        print("Direct link is "+topBook["selfLink"]+" and the id is "+bookID)
    else:
        print("Error with request: "+r.status_code)
        bookID=0
    return bookID
 
def makeQueryStr(title, author):
    cleanTitle=title.lower()
    cleanAuthor=author.lower()
    cleanAuthor = cleanAuthor.replace(" ", "+")
    paramStr=cleanTitle+"+inauthor:"+cleanAuthor
    return paramStr

#function that pulls page number and genere info for a given book ID

#Function that updates read info for a given book (unclear what the reference will be, or whether that should be in this file)

""" response = requests.get("https://www.googleapis.com/books/v1/volumes?q=Beowulf+inauthor:seamus+heaney")
print(response.status_code)
dict = response.json()
items = dict["items"]
topBook = items[1]
bookID = topBook["id"]
print("Direct link is "+topBook["selfLink"]+" and the id is "+bookID) """

getBookID("Beowulf", "Seamus Heaney")
