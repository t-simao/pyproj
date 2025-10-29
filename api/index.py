from flask import Flask, request
from flask_cors import CORS
from userApi import users
from recipeApi import recipes

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'HEJ Hej'

app.register_blueprint(users)
app.register_blueprint(recipes)


if __name__ == '__main__':
    app.run(port=5000, debug=True)