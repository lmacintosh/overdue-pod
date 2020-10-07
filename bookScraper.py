import requests
import sqlite3

conn = sqlite3.connect('overduepod.db') #setting up access to sqlite db
c = conn.cursor() #make sure to end with and conn.commit() and conn.close()

c.execute("SELECT COUNT(*) FROM test")
numEp = c.fetchone() #count how many episides there are in the db
numEp = numEp[0] #extract just the number from the tuple

#the https response is a dictionary, the items value is a list of books, each book is a dictionary

#function that pulls google ID for a given title and author
def getBookID(title, author):
    queryStr = makeQueryStr(title, author) #format the query string w the helper function
    payload = {"q": queryStr}
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload) #pull book info
    print(r.status_code)
    print(r.url)
    if r.status_code==200: #check that we have a positive API response
        dict = r.json() #extract json response to a dictionary
        items = dict["items"] #separate out the search results from the response
        topBook = items[0] #going off the assumption that the first result is the one we want
        bookID = topBook["id"] 
        #print("Direct link is "+topBook["selfLink"]+" and the id is "+bookID)
    else: #other status codes can indicate error, break (currently setting bookID to 0 but I don't love it)
        print("Error with request: "+r.status_code)
        bookID=0
    return bookID
 
#helper function that formats a query string 
def makeQueryStr(title, author):
    cleanTitle=title.lower()
    cleanAuthor=author.lower() #make them lowercase (not acutally necessary, but it looks nicer)
    paramStr=cleanTitle+"+inauthor:"+cleanAuthor #add the "in author" search param
    return paramStr

#function that pulls page number and genere info for a given book ID

def getBookInfo(bookID):
    r = requests.get("https://www.googleapis.com/books/v1/volumes/"+bookID) #query with Google book ID
    bookInfo = r.json() #extract json response to a dictionary
    volumeInfo = bookInfo["volumeInfo"] #pull desired info with the relevant dictionary keys
    pageCount = volumeInfo["printedPageCount"]
    genres = volumeInfo["categories"]
    return [pageCount, genres]

#function that cycles through the epList to identify books
def epCycle():
    for n in range(1, numEp): #var up at the top that determines how many items are in the list
        print(str(n))
        c.execute("SELECT title, author FROM test WHERE epNumber =?", [str(n)])
        book = c.fetchone()
        title = book[0] 
        author = book[1]
        addBook(title, author) #trusting addBook to check to make sure it's not already there

#function that adds a record to the book database

def addBook(title, author):
    bookID = getBookID(title, author) #run helper function to identify book ID from title and author
    c.execute("INSERT INTO bookList VALUES (?, ?, ?)", (title, author, bookID)) #insert into SQL database

#function that adds other book into the book database

#Function that updates read info for a given book (unclear what the reference will be, or whether that should be in this file)


c.execute("SELECT title, author FROM test WHERE epNumber =?", ["53"])
book = c.fetchone()
testTitle = book[0]
testAuthor = book[1]
print(book)

bookID = getBookID(testTitle, testAuthor)
print(getBookInfo(bookID))

addBook(testTitle, testAuthor)

#epCycle()
#c.execute("SELECT * FROM bookList LIMIT 20")
#print(c.fetchall())


conn.close()



"""
current notes: fails on the "multiple short stories thing", like in ep 53 when they talk about The Lottery 
and The Yellow Wallpaper. No search results are found so it fails. The solution would seem to be like, having something
where each episode can point to multiple books, but that causes errors with having epNumber as a primary key.
"""