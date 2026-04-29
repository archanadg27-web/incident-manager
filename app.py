from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from models import db, Incident

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

db.init_app(app)
mail = Mail(app)

# Create tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    incidents = Incident.query.all()
    return render_template('index.html', incidents=incidents)

# Get all incidents
@app.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([i.to_dict() for i in incidents])

# Create incident
@app.route('/incidents', methods=['POST'])
def create_incident():
    data = request.json
    incident = Incident(
        title=data['title'],
        description=data['description'],
        priority=data.get('priority', 'Medium'),
        assigned_to=data.get('assigned_to', 'Unassigned')
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify(incident.to_dict()), 201

# Update incident
@app.route('/incidents/<int:id>', methods=['PUT'])
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    data = request.json
    incident.title = data.get('title', incident.title)
    incident.description = data.get('description', incident.description)
    incident.priority = data.get('priority', incident.priority)
    incident.assigned_to = data.get('assigned_to', incident.assigned_to)
    db.session.commit()
    return jsonify(incident.to_dict())

# Resolve incident
@app.route('/incidents/<int:id>/resolve', methods=['PATCH'])
def resolve_incident(id):
    incident = Incident.query.get_or_404(id)
    incident.status = 'Resolved'
    db.session.commit()
    return jsonify(incident.to_dict())

# Delete incident
@app.route('/incidents/<int:id>', methods=['DELETE'])
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Incident deleted'})

if __name__ == '__main__':
    app.run(debug=True)
