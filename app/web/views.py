from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_required, current_user
from app import app, db
from app.web.forms import SignUpReaderForm, EditReaderForm, AddBookForm, EditBookForm, SearchForm
from database.models import Reader, Book
from datetime import datetime
import logging


def generate_form(form, obj=None):
    form = form(obj=obj)
    return form


@app.route('/books/<int:page>')
@app.route('/books')
@login_required
def get_books(page=1):
    books = Book.query.order_by(Book.id.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('books.html', books=books, user=current_user)


@app.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.form.get('cancel'):
        return redirect(url_for('index'))

    form = generate_form(AddBookForm)
    if request.method == 'POST':
        if form.validate_on_submit():
            book = Book()
            book.title = form.title.data
            book.author = form.author.data
            book.year = form.year.data
            try:
                db.session.add(book)
                db.session.commit()
                return redirect(url_for('get_books'))
            except Exception as error:
                msg = f"{datetime.now()} Error occurred adding {book.title}!\nError: {error}"
                logging.warning(msg=msg)
                db.session.rollback()
                form = generate_form(AddBookForm)
                flash(f'Error while adding {book.title}! Try again.')
    return render_template('add_book.html', form=form, user=current_user)


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_superuser:
        flash(f'Only library staff can edit book!')
        return redirect(url_for('get_books'))

    if request.form.get('cancel'):
        return redirect(url_for('index'))

    book = Book.query.filter_by(id=book_id).first()
    form = generate_form(EditBookForm, book)
    if request.method == 'POST':
        if form.validate_on_submit():
            book.title = form.title.data
            book.author = form.author.data
            book.year = form.year.data
            book.reader_id = None
            if form.reader.data:
                book.reader_id = form.reader.data.id
            try:
                db.session.commit()
                return redirect(url_for('get_books'))
            except Exception as error:
                msg = f"{datetime.now()} Error occurred adding {book.title}!\nError: {error}"
                logging.warning(msg=msg)
                db.session.rollback()
                form = generate_form(EditBookForm, book)
                flash(f'Error while adding {book.title}! Try again.')
    return render_template('edit_book.html', form=form, user=current_user)


@app.route('/readers')
@login_required
def get_readers(page=1):
    if not current_user.is_superuser:
        flash(f'Only library staff can see all readers!')
        return redirect(url_for('get_books'))
    readers = Reader.query.order_by(Reader.last_login.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('readers.html', readers=readers, user=current_user)


@app.route('/readers/<int:reader_id>/books/<int:page>')
@app.route('/readers/<int:reader_id>/books')
@login_required
def get_reader_books(reader_id, page=1):
    reader = Reader.query.filter_by(id=reader_id).first()
    books = Book.query.filter_by(reader_id=reader.id).paginate(page=page, per_page=50, error_out=False)
    return render_template('reader_books.html', reader=reader, books=books, user=current_user)


@app.route('/reader/<int:reader_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reader(reader_id):
    if current_user.is_superuser or current_user.id == reader_id:
        if request.form.get('cancel'):
            return redirect(url_for('get_books'))
        reader = Reader.query.filter_by(id=reader_id).first()
        form = generate_form(EditReaderForm, reader)
        if request.method == 'POST':
            if form.validate_on_submit():
                reader.name = form.name.data
                reader.surname = form.surname.data
                reader.email = form.email.data
                if form.password.data and form.password.data == form.confirm_password.data:
                    reader.set_password(form.password.data)
                if current_user.is_superuser:
                    reader.is_active = form.is_active.data
                    reader.is_superuser = form.is_superuser.data
                reader.update_at = datetime.now()
                try:
                    db.session.commit()
                    return redirect(url_for('get_books'))
                except Exception as error:
                    msg = f"{datetime.now()} Error occurred editing {reader.name}!\nError: {error}"
                    logging.warning(msg=msg)
                    db.session.rollback()
                    form = generate_form(EditReaderForm, reader)
                    flash(f'Error while editing {reader.name}! Try again.')
        return render_template('edit_reader.html', form=form, user=current_user)
    else:
        flash(f'You can edit only your account!')
        return redirect(url_for('get_books'))


@app.route('/search/<int:page>', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search(page=1):
    query = g.search_form.data.get('query')
    if query:
        books = Book.query.filter(Book.title.like(f"%{query}%")).paginate(page=page, per_page=15, error_out=False)
        return render_template('search_books.html', books=books, query=query, user=current_user)
    return redirect('/books')


@app.errorhandler(404)
def not_found(exception):
    context = {'wait_time': 3000, 'url': '/'}
    return render_template('404.html', context=context)


@app.errorhandler(500)
def internal_error(exception):
    return render_template('500.html')


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.search_form = SearchForm()
