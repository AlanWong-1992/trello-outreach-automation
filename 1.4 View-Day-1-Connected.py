import re, webbrowser, json, trello, requests, ssl

# Trello API Key, Token, and Board Names
ApiKey = ''
token = ''
boardName =''

# Variables to find lists variables
lists = []
day1 = {}
nameListDay1 = []
sslContext = ssl.SSLContext()

extension = 'detail/recent-activity/shares/' #add this to go to specific linkedIn page to show their posts
linkedInURLsDay1 = ['www.google.com']

# get all the boards from my account
boards = requests.get('https://api.trello.com/1/members/me/boards?fields=name,url&key={}&token={}'.format(ApiKey, token))
boards = json.loads(boards.content)

# find the right board
for board in boards:
    if board["name"] == boardName:
        boardID = board["id"]
        boardReq = board
        break

# get all lists from board and get the id for the lists
getLists = trello.Boards(ApiKey, token).get_list(boardID)
for list in getLists:
    lists.append({"id": list["id"], "name": list["name"]})

# setting days to the id and name of each list from lists
day1 = lists[0]

# get list of cards names in list I want
cardList = trello.Lists(ApiKey, token).get_card(day1["id"])
for card in cardList:
    nameListDay1.append(card["name"])

# append the posts extension to URL
for name in nameListDay1:
    URLStart = re.search("https://+", name) # find linkedIn URL by searching for the start point of https://
    if URLStart:
        linkedInURLsDay1.append(name[URLStart.start():len(name)])

# Opens new tab for all linkedIn URLs
for URL in linkedInURLsDay1:
    webbrowser.open(URL, new=1)

