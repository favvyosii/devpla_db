# backend/app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Flask configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///developer1.db'  # SQLite for development, replace with your DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)  # Enable CORS 


class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(100))
    portfolio_website = db.Column(db.String(255))
    github = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    technologies = db.Column(db.String(255))
    niche = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)
    hidden_countries = db.Column(db.String(200), default='')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'country': self.country,
            'portfolio_website': self.portfolio_website,
            'github': self.github,
            'linkedin': self.linkedin,
            'technologies': self.technologies,
            'niche': self.niche,
            'hidden_countries': self.hidden_countries.split(',') if self.hidden_countries else [],
        }

# Create the database tables (run once)
with app.app_context():
    db.create_all()

# Route to create a new developer profile (signup)
@app.route('/signup', methods=['POST'])
def create_developer():
    data = request.get_json()

    required_fields = ['name', 'email', 'phone', 'country', 'portfolio_website', 'github', 'linkedin', 'technologies', 'niche', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_developer = Developer(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        country=data['country'],
        portfolio_website=data['portfolio_website'],
        github=data['github'],
        linkedin=data['linkedin'],
        technologies=data['technologies'],
        niche=data['niche'],
        password=hashed_password  # Store hashed password
    )

    try:
        db.session.add(new_developer)
        db.session.commit()
        return jsonify(new_developer.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create profile', 'message': str(e)}), 400

# Route to get a developer's profile by user ID
@app.route('/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    developer = Developer.query.get(user_id)
    
    if developer:
        return jsonify(developer.to_dict()), 200
    else:
        return jsonify({'error': 'Profile not found'}), 404
@app.route('/profile', methods=['DELETE'])
def delete_profile():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    developer = Developer.query.get(user_id)
    
    if not developer:
        return jsonify({'error': 'Profile not found'}), 404
    
    db.session.delete(developer)
    db.session.commit()
    
    return jsonify({'message': 'Profile deleted successfully'}), 200
@app.route('/developers', methods=['GET'])
def get_developers():
    developers = Developer.query.all()
    return jsonify([dev.to_dict() for dev in developers]), 200
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    developer = Developer.query.filter_by(email=data['email']).first()
    
    if developer and check_password_hash(developer.password, data['password']):
        return jsonify({'message': 'Login successful', 'user_id': developer.id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
        
@app.route('/profile/<int:user_id>', methods=['GET'])
def fetch_profile(user_id):  # Changed function name
    developer = Developer.query.get(user_id)
    if developer:
        return jsonify({
            'name': developer.name,
            'email': developer.email,
            'technologies': developer.technologies,
            # Add other fields as needed
        }), 200
    return jsonify({'message': 'Profile not found'}), 404 

@app.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    developer = Developer.query.get(user_id)
    if not developer:
        return jsonify({'message': 'Profile not found'}), 404

    data = request.get_json()
    
    # Update the developer's attributes
    developer.name = data.get('name', developer.name)
    developer.email = data.get('email', developer.email)
    developer.technologies = data.get('technologies', developer.technologies)
    developer.country = data.get('country', developer.country)  # Update country
    developer.hidden_countries = data.get('hidden_countries', developer.hidden_countries)
    db.session.commit()

    return jsonify(developer.to_dict()), 200
     
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
