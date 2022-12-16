#!/usr/bin/env python
import os
import subprocess
import typer
from flask_migrate import Migrate
from app import create_app, db, socket
from app.models import Role, User
from config import Config
import logging
from flask_socketio import SocketIO




app = create_app(os.getenv('FLASK_CONFIG', 'default'))
logging.getLogger('flask_cors').level = logging.DEBUG





manager = typer.Typer()
migrate = Migrate(app, db)


@manager.command()
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command()
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


@manager.command()
def run_socket_server():
    """runs a seperate socketio instance"""
    socketio = SocketIO(app)
    socketio.run(app, host='0.0.0.0', port=5000)
    

@manager.command()
def runserver():
    src.run('0.0.0.0', 5000)


@manager.command()
def create_tables():
    """
    Creates only database tables without dropping the database.
    """
    # db.drop_all()
    with app.app_context():
        db.create_all()
        db.session.commit()


def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command()
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command()
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    with app.app_context():
        Role.insert_roles()
        admin_query = Role.query.filter_by(name='Administrator')
        if admin_query.first() is not None:
            if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
                user = User(first_name='Admin',
                            last_name='Account',
                            password=Config.ADMIN_PASSWORD,
                            confirmed=True,
                            username='Admin',
                            email=Config.ADMIN_EMAIL)
                db.session.add(user)
                db.session.commit()
                print('Added administrator {}'.format(user.full_name()))



@manager.command()
def run_cron_worker():
    """Triggers a celery worker process"""
    from app.common.celery import celery
    worker = celery.Worker()
    worker.start()


@manager.command()
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager()
