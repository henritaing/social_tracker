from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Chemin vers la base de données
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Utiliser un décorateur pour exécuter le code à l'intérieur du contexte de l'application Flask
with app.app_context():
    # Créer toutes les tables de la base de données (si elles n'existent pas déjà)
    db.create_all()

@app.route('/register')  # Route pour afficher la page d'inscription
def register():
    return render_template('register.html')

@app.route('/')
def login():
    # Logique de la page de login
    return render_template('login.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        # Connexion réussie, redirigez l'utilisateur vers le dashboard
        return redirect(url_for('dashboard'))
    else:
        # Redirigez l'utilisateur vers la page de login avec un message d'erreur
        return render_template('login.html', error='Invalid credentials. Please try again.')

@app.route('/process_register', methods=['POST'])  # Route pour traiter le formulaire d'inscription
def process_register():
    # Récupérer les données soumises par le formulaire
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Vérifier si le mot de passe et la confirmation de mot de passe correspondent
    if password != confirm_password:
        # Rediriger l'utilisateur vers la page d'inscription avec un message d'erreur
        return render_template('register.html', error='Password and confirm password do not match')

    # Si les mots de passe correspondent, enregistrer l'utilisateur dans la base de données ou effectuer toute autre action nécessaire

    # Rediriger l'utilisateur vers la page de connexion après inscription réussie
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    # Logique du dashboard
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    # Logique de la page de paramètres
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
