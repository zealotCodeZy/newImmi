from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.login_message = '请先登录才能访问此页面'
    
    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))
    
    with app.app_context():
        # 导入并注册蓝图
        from . import routes
        from . import auth
        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.bp, url_prefix='/auth')
        
        # 创建数据库表
        db.create_all()
        
    return app
