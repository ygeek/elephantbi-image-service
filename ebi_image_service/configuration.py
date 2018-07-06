import os

LOG_FILE_DIR = './local_data/logs/'


class BaseConfig:
    # Builtin Configuration
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200M
    SERVER_NAME = os.getenv('SERVER_NAME')


class GeneralConfig(BaseConfig):
    pass


class TestConfig(GeneralConfig):
    TESTING = True


class DevelopConfig(GeneralConfig):
    DEBUG = True


class ProductionConfig(GeneralConfig):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True


def get_config(env='develop'):
    configs = {
        'develop': DevelopConfig,
        'production': ProductionConfig,
        'test': TestConfig,
    }
    return configs[env]
