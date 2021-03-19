from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from getpass import getpass
from app import app, db
from database.models import Reader

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def superuser():
    while True:
        name = input('Enter superuser name: ')
        surname = input('Enter superuser surname: ')
        email = input('Enter superuser email: ')
        password = getpass('Enter superuser password: ')
        password2 = getpass('Reenter superuser password: ')
        if password == password2:
            answer = input(f'Is it correct data username: {name} email: {email} (y/yes)?\n')
            if answer.lower() in ['yes', 'y']:
                admin = Reader(name=name, surname=surname, email=email, is_active=True, is_superuser=True)
                try:
                    admin.set_password(password)
                    db.session.add(admin)
                    db.session.commit()
                    print('Superuser created successfully!')
                    return
                except (IntegrityError, InvalidRequestError) as error:
                    db.session.rollback()
                    print('Something wrong! Try again!')
                finally:
                    db.session.close()
            else:
                continue
        else:
            print('Passwords mismatch!')
            continue


if __name__ == '__main__':
    manager.run()
