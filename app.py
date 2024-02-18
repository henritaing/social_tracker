from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from enum import Enum
from flask_migrate import Migrate # python -m flask db init
                                  # python -m flask db migrate/upgrade


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class HealthStatus(Enum):
    Sick = "Sick"
    OK = "OK"
    Rocking = "Rocking"

class District(Enum):
    PITSEA = "Pitsea"
    LAINDON = "Laindon"
    VANGE = "Vange"
    FRYERNS = "Fryerns"
    CRAYLANDS = "Craylands"
    BARSTABLE = "Barstable"
    KINGSWOOD = "Kingswood"
    GHYLLGROVE = "Ghyllgrove"
    LEE_CHAPEL_SOUTH = "Lee Chapel South"
    LEE_CHAPEL_NORTH = "Lee Chapel North"
    LANGDON_HILLS = "Langdon Hills"
    DRY_STREET = "Dry Street"
    GREAT_BERRY = "Great Berry"
    NOAK_BRIDGE = "Noak Bridge"
    STEEPLE_VIEW = "Steeple View"
    PIPPS_HILL = "Pipps Hill"
    CRANES = "Cranes"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    feel = db.Column(db.Integer, default=None)
    day = db.Column(db.Integer, default=None)
    health = db.Column(db.Enum(HealthStatus), default=None)
    district = db.Column(db.Enum(District), default=None)  # Modification ici

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
    try:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username  # Définir le nom d'utilisateur dans la session
            return redirect(url_for('inputs'))
    except IntegrityError:
        pass
    return render_template('login.html', error='Invalid credentials. Please try again.')


@app.route('/process_register', methods=['POST'])  
def process_register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('register.html', error='Password and confirm password do not match')

    new_user = User(username=username, password=password, feel=None, day=None, health=None, district=None)

    db.session.add(new_user)
    try:
        db.session.commit()
        session['username'] = username  # Définir le nom d'utilisateur dans la session
        return redirect(url_for('login'))
    except IntegrityError:
        db.session.rollback()
        return render_template('register.html', error='The username has already been taken')


@app.route('/inputs')
def inputs():
    return render_template('inputs.html')


@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    feel = int(request.form['feel'])
    day = int(request.form['day'])
    health = request.form['health']
    district = request.form['district']

    # Validation du district
    try:
        district_enum = District[district.upper()]  # Convertit le district en Enum
    except KeyError:
        return render_template('inputs.html', error='Invalid district selected.')

    # Validation de la santé
    try:
        health_enum = HealthStatus[health.upper()]  # Convertit la santé en Enum
    except KeyError:
        return render_template('inputs.html', error='Invalid health status selected.')

    user = User.query.filter_by(username=session['username']).first()
    if user:
        user.feel = feel
        user.day = day
        user.health = health_enum  # Utiliser la valeur d'énumération convertie
        user.district = district_enum  # Utiliser la valeur d'énumération convertie
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirection vers le dashboard après la soumission des données

    return render_template('inputs.html', error='User not found')  # Ajouter une gestion si l'utilisateur n'est pas trouvé



def get_responses_count_per_district():
    districts = District.__members__.values()
    responses_count_per_district = {}

    for district in districts:
        count = User.query.filter_by(district=district).count()
        responses_count_per_district[district] = count

    return responses_count_per_district


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
