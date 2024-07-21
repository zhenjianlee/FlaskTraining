class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY="learningpythonisfun12345678"
    PROPAGATE_EXCEPTIONS= True
    #Flask Smorest
    #------------
    API_TITLE = "Stores REST API"
    API_VERSION= "v1"
    OPENAPI_VERSION="3.0.3"
    OPENAPI_URL_PREFIX="/"
    #Swagger
    #-------------
    OPENAPI_SWAGGER_UI_PATH="/swagger-ui"
    OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="mysql://zhenjianlee:zhenjianlee@localhost/flaskTraining"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    