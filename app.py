from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import click

app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wardrobe.db'
db = SQLAlchemy(app)

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Wardrobe API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Models
outfit_clothing = db.Table('outfit_clothing',
    db.Column('outfit_id', db.Integer, db.ForeignKey('outfit.id'), primary_key=True),
    db.Column('clothing_item_id', db.Integer, db.ForeignKey('clothing_item.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    clothing_items = db.relationship('ClothingItem', backref='user', cascade="all, delete-orphan")
    outfits = db.relationship('Outfit', backref='user', cascade="all, delete-orphan")

    def as_dict(self):
        return {'id': self.id, 'username': self.username}

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(80), nullable=False)
    style = db.Column(db.String(80), nullable=False)
    season = db.Column(db.String(80), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'color': self.color,
            'style': self.style,
            'season': self.season
        }

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    clothing_items = db.relationship('ClothingItem', secondary=outfit_clothing, backref='outfits')

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'clothing_items': [item.as_dict() for item in self.clothing_items]
        }

# Routes

# Test route to check if the server is running
@app.route('/test', methods=['GET'])
def test_route():
    return "Server is running", 200

# Log registered routes (Not currently functional?)
@app.cli.command()
def list_routes():
    """List all registered routes."""
    for rule in app.url_map.iter_rules():
        click.echo(f"{rule.endpoint}: {rule.rule}")

# Output the routes to a page
@app.route('/routes', methods=['GET'])
def routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule.endpoint}: {rule.rule}")
    return jsonify(output)

# Helper function to capitalize the first letter of each word
def capitalize_words(s):
    return ' '.join(word.capitalize() for word in s.split())

# User Routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data['username'].strip()
    normalized_username = username.lower()
    if User.query.filter(db.func.lower(User.username) == normalized_username).first():
        return jsonify({'error': 'User Already Exists'}), 400
    # Capitalize the first letter of each word in the username
    capitalized_username = capitalize_words(username)
    new_user = User(username=capitalized_username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.as_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.as_dict())

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get_or_404(id)
    user.username = data['username']
    db.session.commit()
    return jsonify(user.as_dict())

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 204

@app.route('/users', methods=['DELETE'])
def delete_all_users():
    db.session.query(ClothingItem).delete()
    db.session.query(Outfit).delete()
    db.session.query(User).delete()
    db.session.commit()
    return jsonify({'message': 'All users, clothing items, and outfits deleted'}), 204

# ClothingItem Routes
@app.route('/users/<int:user_id>/clothing_items', methods=['POST'])
def create_clothing_item(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    new_item = ClothingItem(
        user_id=user.id,
        type=data['type'],
        color=data['color'],
        style=data['style'],
        season=data['season']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.as_dict()), 201

@app.route('/users/<int:user_id>/clothing_items', methods=['GET'])
def get_clothing_items(user_id):
    user = User.query.get_or_404(user_id)
    items = ClothingItem.query.filter_by(user_id=user.id).all()
    return jsonify([item.as_dict() for item in items])

@app.route('/users/<int:user_id>/clothing_items/<int:item_id>', methods=['GET'])
def get_clothing_item(user_id, item_id):
    user = User.query.get_or_404(user_id)
    item = ClothingItem.query.filter_by(user_id=user.id, id=item_id).first_or_404()
    return jsonify(item.as_dict())

@app.route('/users/<int:user_id>/clothing_items/<int:item_id>', methods=['PUT'])
def update_clothing_item(user_id, item_id):
    user = User.query.get_or_404(user_id)
    item = ClothingItem.query.filter_by(user_id=user.id, id=item_id).first_or_404()
    data = request.json
    item.type = data['type']
    item.color = data['color']
    item.style = data['style']
    item.season = data['season']
    db.session.commit()
    return jsonify(item.as_dict())

@app.route('/users/<int:user_id>/clothing_items/<int:item_id>', methods=['DELETE'])
def delete_clothing_item(user_id, item_id):
    user = User.query.get_or_404(user_id)
    item = ClothingItem.query.filter_by(user_id=user.id, id=item_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Clothing item deleted'}), 204

# Outfit Routes
@app.route('/outfits', methods=['POST'])
def create_outfit():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name', "").strip()  # Trim leading and trailing spaces
    clothing_item_ids = data.get('clothing_item_ids')

    if not user_id or not name:
        return jsonify({"error": "User ID and outfit name are required"}), 400
    
    # Capitalize the first character of the outfit name
    name = name.capitalize()

    # Check if the name is empty after trimming
    if name == "":
        return jsonify({"error": "Outfit name cannot be empty"}), 400

    # Check if an outfit with the same name already exists for the user (case-insensitive)
    existing_outfit = Outfit.query.filter_by(user_id=user_id).filter(db.func.lower(Outfit.name) == name.lower()).first()
    if existing_outfit:
        return jsonify({"error": "You already have an outfit with this name"}), 400

    # Create and save the new outfit
    outfit = Outfit(user_id=user_id, name=name)
    db.session.add(outfit)
    db.session.commit()

    # Add clothing items to the outfit
    for item_id in clothing_item_ids:
        clothing_item = ClothingItem.query.get(item_id)
        if clothing_item:
            outfit.clothing_items.append(clothing_item)

    db.session.commit()

    return jsonify(outfit.as_dict()), 201



@app.route('/users/<int:user_id>/outfits', methods=['GET'])
def get_user_outfits(user_id):
    outfits = Outfit.query.filter_by(user_id=user_id).all()
    return jsonify([outfit.as_dict() for outfit in outfits])

@app.route('/outfits/<int:id>', methods=['GET'])
def get_outfit(id):
    outfit = Outfit.query.get_or_404(id)
    return jsonify(outfit.as_dict())

@app.route('/outfits/<int:id>', methods=['PUT'])
def update_outfit(id):
    data = request.json
    outfit = Outfit.query.get_or_404(id)
    outfit.name = data.get('name', outfit.name)

    clothing_item_ids = data.get('clothing_item_ids')
    if clothing_item_ids:
        outfit.clothing_items = []
        for item_id in clothing_item_ids:
            clothing_item = ClothingItem.query.get(item_id)
            if clothing_item:
                outfit.clothing_items.append(clothing_item)

    db.session.commit()
    return jsonify(outfit.as_dict())

@app.route('/outfits/<int:id>', methods=['DELETE'])
def delete_outfit(id):
    outfit = Outfit.query.get_or_404(id)
    db.session.delete(outfit)
    db.session.commit()
    return jsonify({'message': 'Outfit deleted'}), 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
