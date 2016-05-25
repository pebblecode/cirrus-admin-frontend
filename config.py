import os
import jinja2
from dmutils.status import enabled_since, get_version_label
from dmutils.asset_fingerprint import AssetFingerprinter

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    VERSION = get_version_label(
        os.path.abspath(os.path.dirname(__file__))
    )
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_NAME = 'dm_admin_session'
    SESSION_COOKIE_PATH = '/admin'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    DM_S3_DOCUMENT_BUCKET = None
    DM_DOCUMENTS_URL = 'https://assets.cirrus.dev.pebblecode.com'
    DM_DATA_API_URL = None
    DM_DATA_API_AUTH_TOKEN = None
    SECRET_KEY = None

    DM_AGREEMENTS_BUCKET = None
    DM_COMMUNICATIONS_BUCKET = None
    DM_ASSETS_URL = None

    STATIC_URL_PATH = '/admin/static'
    ASSET_PATH = STATIC_URL_PATH + '/'
    BASE_TEMPLATE_DATA = {
        'header_class': 'with-proposition',
        'asset_path': ASSET_PATH,
        'asset_fingerprinter': AssetFingerprinter(asset_root=ASSET_PATH)
    }

    # Logging
    DM_LOG_LEVEL = 'DEBUG'
    DM_APP_NAME = 'admin-frontend'
    DM_LOG_PATH = '/var/log/digitalmarketplace/application.log'
    DM_DOWNSTREAM_REQUEST_ID_HEADER = 'X-Amz-Cf-Id'

    # Feature Flags
    RAISE_ERROR_ON_MISSING_FEATURES = True

    SHARED_EMAIL_KEY = None
    INVITE_EMAIL_SALT = 'InviteEmailSalt'

    INVITE_EMAIL_NAME = 'Cirrus Admin'
    INVITE_EMAIL_FROM = 'enquiries@cirrus.pebblecode.com'
    INVITE_EMAIL_SUBJECT = 'Your Cirrus invitation'
    CREATE_USER_PATH = 'suppliers/create-user'

    @staticmethod
    def init_app(app):
        repo_root = os.path.abspath(os.path.dirname(__file__))
        template_folders = [
            os.path.join(repo_root, 'app/templates')
        ]
        jinja_loader = jinja2.FileSystemLoader(template_folders)
        app.jinja_loader = jinja_loader


class Test(Config):
    DEBUG = True
    AUTHENTICATION = True
    WTF_CSRF_ENABLED = False
    DM_DOCUMENTS_URL = 'https://assets.test.cirrus.pebblecode.com'
    SECRET_KEY = "test_secret"

    DM_LOG_LEVEL = 'CRITICAL'
    SHARED_EMAIL_KEY = 'KEY'
    INVITE_EMAIL_SALT = 'SALT'
    DM_COMMUNICATIONS_BUCKET = 'cirrus-communications-dev-dev'
    DM_AGREEMENTS_BUCKET = 'cirrus-documents-dev-dev'


class Development(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = False
    AUTHENTICATION = True
    DM_COMMUNICATIONS_BUCKET = 'cirrus-communications-dev-dev'
    DM_AGREEMENTS_BUCKET = 'cirrus-documents-dev-dev'

    DM_DATA_API_URL = os.getenv('DM_DATA_API_URL', "http://localhost:5000")
    DM_DATA_API_AUTH_TOKEN = os.getenv('DM_API_AUTH_TOKEN', "myToken")
    SECRET_KEY = "verySecretKey"
    DM_S3_DOCUMENT_BUCKET = "cirrus-documents-dev-dev"
    DM_DOCUMENTS_URL = "https://{}.s3-eu-west-1.amazonaws.com".format(DM_S3_DOCUMENT_BUCKET)
    SHARED_EMAIL_KEY = "very_secret"


class Live(Config):
    DEBUG = False
    AUTHENTICATION = True
    DM_HTTP_PROTO = 'https'
    DM_DOCUMENTS_URL = 'https://assets.cirrus.pebblecode.com'


class Staging(Config):
    DEBUG = False
    AUTHENTICATION = True
    WTF_CSRF_ENABLED = False
    DM_DOCUMENTS_URL = 'https://assets.cirrus.pebblecode.com'


configs = {
    'development': Development,
    'preview': Development,
    'staging': Staging,
    'production': Live,
    'test': Test,
}
