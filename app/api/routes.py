from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Content, content_schema, contents_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/data')
def getdata():
    return {'Hello': 'World'}

# CREATE
@api.route('/content', methods=['POST'])
@token_required
def create_content(current_user_token):
    title = request.json['title']
    text = request.json['text']
    date_added = request.json['date_added']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    content = Content(title, text, date_added, user_token=user_token)

    db.session.add(content)
    db.session.commit()

    response = content_schema.dump(content)
    return jsonify(response)

# RETRIEVE
# all selections
@api.route('/content', methods=['GET'])
@token_required
def get_all_content(current_user_token):
    a_user = current_user_token.token
    contents = Content.query.filter_by(user_token = a_user).all()
    response = contents_schema.dump(contents)
    return jsonify(response)

# singular selection
@api.route('/content/<id>', methods=['GET'])
@token_required
def get_single_content(current_user_token, id):
    content = Content.query.get(id)
    response = content_schema.dump(content)
    return jsonify(response)

# UPDATE
@api.route('/content/<id>', methods=['POST', 'PUT'])
@token_required
def update_content(current_user_token, id):
    content = Content.query.get(id)
    content.title = request.json['title']
    content.text = request.json['text']
    content.date_added = request.json['date_added']
    content.user_token = current_user_token.token

    db.session.commit()
    response = content_schema.dump(content)
    return jsonify(response)

# DELETE
@api.route('/content/<id>', methods=['DELETE'])
@token_required
def delete_content(current_user_token, id):
    content = Content.query.get(id)
    db.session.delete(content)
    db.session.commit()
    response = content_schema.dump(content)
    return jsonify(response)