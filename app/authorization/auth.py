from datetime import datetime
from flask import flash, redirect, url_for, request, render_template
from app import app, login_manager, db
from app.web.forms import SignInForm, SignUpReaderForm
from database.models import Reader
from flask_login import login_required, current_user, login_user, logout_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if current_user.is_authenticated:
        return redirect(url_for('get_books'))
    if request.method == 'POST':
        if form.validate_on_submit():
            reader = Reader.query.filter_by(email=form.email.data).first()
            if reader:
                if reader.check_password(password=form.password.data):
                    if reader.is_active:
                        reader.last_login = datetime.now()
                        db.session.commit()
                        login_user(reader, remember=form.remember_me.data)
                        return redirect(url_for('get_books'))
                    else:
                        flash(f'Access denied!')
                else:
                    flash(f'Wrong password!')
            else:
                flash(f'You should sign in!')
    return render_template('login.html', title='Sign Up', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpReaderForm()
    if current_user.is_authenticated:
        return redirect(url_for('get_books'))
    if request.method == 'POST':
        reader = Reader()
        if not form.password.data and not form.confirm_password.data:
            del form['password']
            del form['confirm_password']
        elif form.password.data and form.password.data != form.confirm_password.data:
            flash(f'Passwords mismatch! Try again.')
            return render_template('register.html', title='Sign In', form=form)
        elif form.password.data == form.confirm_password.data:
            reader.set_password(form.password.data)
        if form.validate_on_submit():
            reader.name = form.name.data
            reader.surname = form.surname.data
            reader.email = form.email.data
            reader.update_at = datetime.now()
            if Reader.query.filter_by(email=reader.email).one_or_none():
                flash(f'User with {reader.email} already registered!')
                return render_template('register.html', title='Sign Up', form=form)
            try:
                db.session.add(reader)
                db.session.commit()
                login_user(reader)
            except Exception as error:
                print(error)
                db.session.rollback()
                flash(f'Error while registering {reader.name}! Try again.')
            else:
                flash(f'{reader.name} registered successfully!')
                return redirect(url_for('get_books'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have been log out!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Reader.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))
