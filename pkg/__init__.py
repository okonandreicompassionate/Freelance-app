from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

from pkg import config #the class is the BaseConfig
csrf =CSRFProtect()
def create_app():
    # import the db instance from SQLALCHEMY
    from pkg.models import db
    # app = Flask(__name__)
    app = Flask(__name__, instance_relative_config=True) #load config from instance folder
    app.config['SECRET_KEY'] = '59InUNHh4Yqh2yzW_ieqv5CBOJnmW0Z73E2hZhPT8Ss'

    app.config.from_pyfile("config.py")
    app.config.from_object(config.TestConfig) #load config from the class

    #prtect our routes with csrf
    csrf.init_app(app)

    # db = SQLAlchemy(app)
    db.init_app(app) 
    migrate = Migrate(app,db)



    return app

app = create_app()

from pkg import client_routes,freelancer_routes,staticroutes