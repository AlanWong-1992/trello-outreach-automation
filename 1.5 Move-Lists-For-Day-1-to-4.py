import re, webbrowser, json, trello, requests, datetime

# Trello API Key, Token, and Board Names
ApiKey = ''
token = ''
boardName =''

# Variables to find lists variables    
lists = []
listID = []
cardLists = []
numOfListsToMove = 5
today = datetime.datetime.now()
newDueDate = today + datetime.timedelta(days=4)

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
lists = trello.Boards(ApiKey, token).get_list(boardID)
for list in lists:
    listID.append(list["id"])

# get call cards for each list
count = 0
while count < numOfListsToMove-1: # this only goes through the first 4 borads
    cardLists.append(trello.Lists(ApiKey, token).get_card(listID[count]))
    card = trello.Lists(ApiKey, token).get_card(listID[count])
    count += 1

user_answer = input("Are you sure you want to move all the cards from Day 1 to Day 4? (Part 1) \n Type Yes or No\n ")  

# move card from current list to the next list if the user answer is yes
if (user_answer.lower() == 'yes'):
    user_answer_again = input("Are you sure you want to do this \n Type Yes or No?\n")
    if (user_answer_again.lower() == 'yes'):
        count = 0
        for cardList in cardLists:
            if count<3:
                for card in cardList:
                    # print(card["id"], card["name"])
                    trello.Cards(ApiKey, token).update(card["id"], idList=listID[count+1])
            else:
                for card in cardList:
                    hasDueDate = card["due"]
                    currentDueDate = datetime.datetime.strptime(card["due"], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None) if hasDueDate else today
                    if (currentDueDate.date() <= today.date()): # count determines the number of boards to edit
                        card["due"] = today.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
                        trello.Cards(ApiKey, token).update(card["id"], idList=listID[count+2], due = newDueDate.date())        
            count += 1

