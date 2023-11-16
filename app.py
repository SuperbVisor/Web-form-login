from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti 'your_secret_key' dengan secret key yang kuat
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)



@app.route('/')
def home():
    return render_template('login.html')

@app.route('/play_snake')
def play_snake():
    return render_template('snake.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('Web form login/static', filename)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return redirect(url_for('user_home'))  # Pengguna diarahkan ke halaman home jika kredensial benar
    else:
        flash('Username atau password salah')
        return redirect(url_for('home'))  # Pengguna tetap di halaman login jika kredensial salah


@app.route('/user_home')
def user_home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username sudah digunakan')
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Akun berhasil dibuat')
            return redirect(url_for('home'))  # Mengarahkan ke halaman login setelah pendaftaran berhasil

    return render_template('register.html')

    

    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
