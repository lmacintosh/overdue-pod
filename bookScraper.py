import requests
import sqlite3

conn = sqlite3.connect('overduepod.db') #setting up access to sqlite db
c = conn.cursor() #make sure to end with and conn.commit() and conn.close()

#the https response is a dictionary, the items value is a list of books, each book is a dictionary

#function that pulls google ID for a given title and author
def getBookID(title, author):
    queryStr = makeQueryStr(title, author)
    payload = {"q": queryStr}
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload)
    #print(r.status_code)
    print(r.url)
    if r.status_code==200:
        dict = r.json()
        items = dict["items"]
        topBook = items[0]
        bookID = topBook["id"]
        print("Direct link is "+topBook["selfLink"]+" and the id is "+bookID)
    else:
        print("Error with request: "+r.status_code)
        bookID=0
    return bookID
 
#helper function that formats a query string 
def makeQueryStr(title, author):
    cleanTitle=title.lower()
    cleanAuthor=author.lower()
    paramStr=cleanTitle+"+inauthor:"+cleanAuthor
    return paramStr

#function that pulls page number and genere info for a given book ID

def getBookInfo(bookID):
    r = requests.get("https://www.googleapis.com/books/v1/volumes/"+bookID)
    bookInfo = r.json()
    volumeInfo = bookInfo["volumeInfo"]
    pageCount = volumeInfo["printedPageCount"]
    genres = volumeInfo["categories"]
    return [pageCount, genres]

#function that cycles through the epList to identify books
def epCycle():
    for n in range(450):
        c.execute("SELECT title, author FROM epList WHERE epNumber =?", n)
        c.fetchone()

#function that adds a record to the book database

def addBook(title, author):
    bookID = getBookID(title, author)
    c.execute("INSERT INTO bookList VALUES (?, ?, ?)", (title, author, bookID))

#function that adds other book into the book database

#Function that updates read info for a given book (unclear what the reference will be, or whether that should be in this file)

""" response = requests.get("https://www.googleapis.com/books/v1/volumes?q=Beowulf+inauthor:seamus+heaney")
print(response.status_code)
dict = response.json()
items = dict["items"]
topBook = items[1]
bookID = topBook["id"]
print("Direct link is "+topBook["selfLink"]+" and the id is "+bookID) """

testTitle = "Portnoy's Complaint"
testAuthor = "Philip Roth"

#bookID = getBookID(testTitle, testAuthor)
#print(getBookInfo(bookID))
addBook(testTitle, testAuthor)

conn.close()