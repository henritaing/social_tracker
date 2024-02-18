from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_migrate import Migrate




app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_ici'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class HealthStatus(Enum):
    SICK = "Sick"
    OK = "OK"
    ROCKING = "Rocking"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    feel = db.Column(db.Integer, default=None)
    day = db.Column(db.Integer, default=None)
    health = db.Column(db.Enum(HealthStatus), default=None)

    # Ajouter des contraintes pour feel et day
    __table_args__ = (
        db.CheckConstraint('feel >= 1 AND feel <= 5', name='check_feel_range'),
        db.CheckConstraint('day >= 1 AND day <= 5', name='check_day_range'),
    )

with app.app_context():
    db.create_all()

@app.route('/register')  
def register():
    return render_template('register.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username  # Définir le nom d'utilisateur dans la session
        return redirect(url_for('inputs'))
    else:
        return render_template('login.html', error='Invalid credentials. Please try again.')

@app.route('/process_register', methods=['POST'])  
def process_register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('register.html', error='Password and confirm password do not match')

    new_user = User(username=username, password=password, feel=None, day=None, health=None)
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username  # Définir le nom d'utilisateur dans la session
    return redirect(url_for('login'))


@app.route('/inputs')
def inputs():
    return render_template('inputs.html')


@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    feel = int(request.form['feel'])
    day = int(request.form['day'])
    health = request.form['health']

    user = User.query.filter_by(username=session['username']).first()
    if user:
        user.feel = feel
        user.day = day
        user.health = health
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
