from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_migrate import Migrate
from config import Config
from models import db, Contact, User, Item
from forms import ContactForm, RegistrationForm, LoginForm, ItemForm
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Pro přístup k této stránce se musíte přihlásit.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html', title='Domovská stránka')


@app.route('/healthz')
def healthz():
    return 'ok', 200

@app.route('/about')
def about():
    return render_template('about.html', title='O nás')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Nejprve zkontrolujeme, zda uživatel s daným emailem nebo uživatelským jménem již neexistuje
            existing_user = User.query.filter(
                (User.email == form.email.data) | 
                (User.username == form.username.data)
            ).first()
            
            if existing_user:
                if existing_user.email == form.email.data:
                    flash('Tento email je již zaregistrován.', 'danger')
                else:
                    flash('Toto uživatelské jméno je již obsazené.', 'danger')
                return render_template('register.html', title='Registrace', form=form)

            # Vytvoření nového uživatele
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            user.created_at = datetime.utcnow()
            
            db.session.add(user)
            db.session.commit()
            
            # Automatické přihlášení po registraci
            session['user_id'] = user.id
            flash('Registrace proběhla úspěšně! Byli jste automaticky přihlášeni.', 'success')
            return redirect(url_for('home'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Chyba při registraci: {str(e)}')
            flash('Došlo k neočekávané chybě. Prosím zkuste to znovu.', 'danger')
            
    return render_template('register.html', title='Registrace', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            
            if user is None:
                flash('Uživatel s tímto emailem není registrován.', 'danger')
                return render_template('login.html', title='Přihlášení', form=form)
            
            if not user.check_password(form.password.data):
                flash('Nesprávné heslo.', 'danger')
                return render_template('login.html', title='Přihlášení', form=form)
            
            session['user_id'] = user.id
            flash('Úspěšně jste se přihlásili!', 'success')
            return redirect(url_for('home'))
            
        except Exception as e:
            app.logger.error(f'Chyba při přihlašování: {str(e)}')
            flash('Došlo k neočekávané chybě. Prosím zkuste to znovu.', 'danger')
            
    return render_template('login.html', title='Přihlášení', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Byli jste odhlášeni.', 'info')
    return redirect(url_for('home'))

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user = User.query.get(session['user_id'])
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data,
            author=user
        )
        db.session.add(contact)
        db.session.commit()
        flash('Vaše zpráva byla úspěšně odeslána!', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html', title='Kontakt', form=form)

@app.route('/items')
def items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('items.html', title='Položky', items=items)

@app.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        try:
            price = float(form.price.data.replace(',', '.'))
            item = Item(
                name=form.name.data,
                description=form.description.data,
                price=price,
                category=form.category.data,
                is_available=form.is_available.data,
                user_id=session['user_id']
            )
            db.session.add(item)
            db.session.commit()
            flash('Položka byla úspěšně přidána!', 'success')
            return redirect(url_for('items'))
        except ValueError:
            flash('Neplatný formát ceny. Použijte číslo.', 'danger')
    return render_template('add_item.html', title='Přidat položku', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
