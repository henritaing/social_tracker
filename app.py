from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    # Logique de la page de login
    return render_template('login.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    username = request.form['username']
    password = request.form['password']
    # Vérifiez les informations de connexion (exemple simplifié)
    if username == 'admin' and password == 'password':
        # Redirigez l'utilisateur vers le dashboard après connexion réussie
        return redirect(url_for('dashboard'))
    else:
        # Redirigez l'utilisateur vers la page de login avec un message d'erreur
        return render_template('login.html', error='Invalid credentials. Please try again.')


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
