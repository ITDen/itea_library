"""
Main configurations module
"""
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Default config class"""

    print(f"[*] {datetime.datetime.now()} Started service configuration...")
    ENV = os.getenv('Environment')

    # Setup sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, f'{ENV}_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        # 'pool': Pool,
        # 'pool_size': 10,
        # 'pool_recycle': 600,
        'pool_pre_ping': True
    }

    # Setup web app
    CSRF_ENABLED = True
    SECRET_KEY = 'xrGTCQhZNy4dvZfNClOD21Z47anOckYQvI4UuUHB22ACeFFvg3D0oyDcx7iiLO2p'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=int(os.getenv('PERMANENT_SESSION_LIFETIME', 10)))
    REMEMBER_COOKIE_DURATION = datetime.timedelta(minutes=int(os.getenv('REMEMBER_COOKIE_DURATION', 60)))
    print(f"[+] {datetime.datetime.now()} Service configuration done")


class ProductionConfig(BaseConfig):
    """Production config class"""
    DEBUG = False
    TESTING = False
    ERROR_INCLUDE_MESSAGE = False


class DevelopmentConfig(BaseConfig):
    """Development config class"""
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """Test config class"""
    DEBUG = False
    TESTING = True


class StagingConfig(BaseConfig):
    """Staging config class"""
    DEBUG = False
    TESTING = False
    ERROR_INCLUDE_MESSAGE = False


# Define configurations map
config_map = {
    'Development': DevelopmentConfig,
    'Staging': StagingConfig,
    'Testing': TestingConfig,
    'Production': ProductionConfig
}
