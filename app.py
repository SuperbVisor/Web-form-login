from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin




app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti 'your_secret_key' dengan secret key yang kuat
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user_home'  # 'home' adalah nama fungsi view untuk halaman login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def is_active(self):
        return True 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/to')
def to():
    username = current_user.username if current_user.is_authenticated else "Guest"
    return render_template('todo.html', username=username)

@app.route('/setting')
def setting():
    username = current_user.username if current_user.is_authenticated else "Guest"
    return render_template('sett.html', username=username)

@app.route('/profil')
def profile():
    username = current_user.username if current_user.is_authenticated else "Guest"
    return render_template('profile.html', username=username)
    
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashbord')
@login_required
def dashbord():
    username = current_user.username if current_user.is_authenticated else "Guest"
    return render_template('dash.html', username=username)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('Web form login/static', filename)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user and user.password == password:  # Memeriksa kredensial pengguna
        login_user(user)  # Login pengguna menggunakan Flask-Login
        return redirect(url_for('user_home'))  # Pengguna diarahkan ke halaman home jika kredensial benar
    else:
        flash('Username atau password salah')
        return redirect(url_for('home'))  # Pengguna tetap di halaman login jika kredensial salah
   



@app.route('/user_home')
@login_required  # Mengharuskan pengguna untuk login sebelum masuk ke halaman ini
def user_home():
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            # Jika email sudah ada, tampilkan pesan error
            flash('Email sudah digunakan')
        else:
            # Jika email belum ada, tambahkan user baru ke database
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Akun berhasil dibuat')
            return redirect(url_for('home'))

    return render_template('register.html')
    

    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=9898)
