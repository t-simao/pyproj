"""User interface/Terminal """

import requests

def login(username, password):
    url = f'http://127.0.0.1:5000/api/users/login'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    
    return response.json()

def register(username, password):
    url = f'http://127.0.0.1:5000/api/users/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    
    return response.json()

def get_all_ingredients():
    url = 'http://127.0.0.1:5000/api/recipes/all'
    response = requests.get(url)
    
    return response.json()

def get_ingredients_by_title(title):
    url = f'http://127.0.0.1:5000/api/recipes?title={title}'
#     data = {'title': title}
    response = requests.get(url)
    
    return response.json()

def get_ingredients_by_ingredients(ingredients):
    url = f'http://127.0.0.1:5000/api/recipes?ingredients={ingredients}'
#     data = {'ingredients': ingredients}
    response = requests.get(url)
    
    return response.json()

def get_ingredients_by_id(num: int):
    url = f'http://127.0.0.1:5000/api/recipes/{num}'
    response = requests.get(url)
    
    return response.json()

def add_favorite(num: int, username):
    url = f'http://127.0.0.1:5000/api/recipes/add-favorite/{num}'
    data = {'username': username}
    response = requests.post(url, json=data)
    
    return response.json()

def get_favorites(username):
    url = f'http://127.0.0.1:5000/api/recipes/favorites'
    data = {'username': username}
    response = requests.get(url, json=data)
    
    return response.json()

def remove_favorite(num: int, username):
    url = f'http://127.0.0.1:5000/api/recipes/rm-favorite/{num}'
    data = {'username': username}
    response = requests.post(url, json=data)
    
    return response.json()

def display_recipes(dictionary: dict):
    for k in dictionary:
        print(k['id'], k['title'], sep=': ')
        
def display_recipe(dictionary: dict):
    print(dictionary['title'])
    print(dictionary['servings'])
#     num = 1
    for ingredient in dictionary['ingredients']:
        print(ingredient)
#         num += 1
        
    print(dictionary['instructions'])

def display_option(dictionary: dict, username=None):
    if username:
        for k, v in dictionary.items():
            print(k, v[0], sep='| ')
    else:
        for k, v in dictionary.items():
            print(k, v, sep='| ')

def option_prompt(dictionary: dict, prompt: str):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in list(dictionary):
            return user_input
        print('Invalid input')
        continue
    
def userRegisterLogin(o):
    username = input('Enter username: ').strip()
    password = input('Enter password: ').strip()

    if not username or not password:
        res = f"Invalid username/password"
    if o == 'r':
        res = register(username, password)
    elif o == 'l':
        res = login(username, password)
    return res

def search(o, username=None, prompt=None):
    if o == 'a':
        res = get_all_ingredients()
        display_recipes(res)
        return
    elif o == 'sf':
        res = get_favorites(username)
        display_recipes(res)
        return
    
    user_input = input(prompt).strip()
    check_num = user_input.isdigit()
    if not user_input:
        print('Nothing was entered')
        return
    if o == 't':
        res = get_ingredients_by_title(user_input)
        display_recipes(res)
    elif o == 'i':
        res = get_ingredients_by_ingredients(user_input)
        display_recipes(res)
    elif o == 'id':
        if check_num == False:
            return
        res = get_ingredients_by_id(int(user_input))
        if 'title' not in res:
            return
        display_recipe(res)
    elif o == 'af':
        if check_num == False:
            return
        res = add_favorite(int(user_input), username)
        print(res["message"])
    elif o == 'rmf':
        if check_num == False:
            return
        res = remove_favorite(int(user_input), username)
        print(res["message"])

option_no_user = {'l': 'Logg in', 'r': 'Register', 'q': 'Quit'}
option_user = {
    'a': ['Show all recipes', 'Enter you choice: '], 't': ['Search by title', 'Enter the title: '],
    'i': ['Search by ingredients', 'Enter the ingredients: '],
    'id': ['Get recipe information by id', 'Enter the id: '], 'af': ['Add to favorites by id', 'Enter the id: '],
    'sf': ['Show favorites', 'Enter you choice: '], 'rmf': ['Remove favorite by id', 'Enter the id: '],
    'q': ['Logout', 'Enter you choice: ']
    }
user = None
user_id = None
while True:
    display_option(option_no_user)
    user_choice = option_prompt(option_no_user, 'Enter your choice: ')
    
    if user_choice == 'q':
        break
    res = userRegisterLogin(user_choice)
    if not '_id' in res or not 'username' in res:
        print(res['message'])
        continue
    user = res['username']
    user_id = res['_id']
    
    while user and user_id:
        display_option(option_user, user)
        user_choice = option_prompt(option_user, 'Enter your choice: ')
        
        if user_choice == 'q':
            user = None
            user_id = None
            continue
            
        res = search(user_choice, user, option_user[user_choice][1])
        
        
    