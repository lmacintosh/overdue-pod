import requests
response = requests.get("https://www.googleapis.com/books/v1/volumes?q=harry+potter&callback=handleResponse")
print(response.status_code)