# server/app.py

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #helps to avoid building up too much unhelpful data in memory

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    response_body = f"<h1>Welcome to the pet/owner directory!</h1>"
    status_code = 200
    response = make_response(response_body, status_code)
    
    return response

@app.route("/pets/<int:id>")
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        response_body = '<h1>404, pet not found</h1>'
        status_code = 404
    else:
        response_body = f'''
                    <h1>Information for {pet.name}</h1>
                    <h2>Pet Species is {pet.species}</h2>
                    <h2>Pet Owner is {pet.owner.name}</h2>
                    '''
        status_code = 200

    reponse = make_response(response_body, status_code )
    return reponse

@app.route("/owner/<int:id>")
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        response_body = '<h1>404, pet not found</h1>'
        status_code = 404
    else:
        response_body = f'<h1>Information for {owner.name}</h1>\n'
        status_code = 200

    pets = [pet for pet in owner.pets]

    if not pets:
        response_body += f'<h2>This owner has no pets at this time</h2><br>'
    else:
        for pet in pets:
            response_body += f'This owner has the following pet {pet.species} named {pet.name}</h2><br>'

    response = make_response(response_body, status_code)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)