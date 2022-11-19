from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('contacts', user='', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Contacts(BaseModel):
  first_name = CharField()
  last_name = CharField()
  address = CharField()
  phone_number = CharField()

db.connect()
db.drop_tables([Contacts])
db.create_tables([Contacts])

Contacts(first_name='Jean', last_name='Reyes', address='123 Park Ave', phone_number='7185555555').save()
Contacts(first_name='CARLOS', last_name='GRULLON', address='123 Madison Ave', phone_number='7185555551').save()


app = Flask(__name__)


@app.route('/contact/', methods=['GET', 'POST'])
@app.route('/contact/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Contacts.get(id)))
    else:
        contacts_list = []
        for contact in Contacts.select():
            contacts_list.append(model_to_dict(contact))
        return jsonify(contacts_list)

  if request.method =='PUT':
    body = request.get_json()
    Contacts.update(body).where(Contacts.id == id).execute()
    return "Contacts " + str(id) + " has been updated."

  if request.method == 'POST':
    new_contact = dict_to_model(Contacts, request.get_json())
    new_contact.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Contacts.delete().where(Contacts.id == id).execute()
    return "Contacts " + str(id) + " deleted."


# Run our application, by default on port 5000
app.run(port=9000, debug=True)