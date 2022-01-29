import os
from dotenv import load_dotenv
import click
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import User, Role, Post, Comment, Todo, TimeLog


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post, Comment=Comment,
                Todo=Todo, TimeLog=TimeLog)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    """Run deployment tasks."""

    # create or update user roles
    Role.insert_roles()
