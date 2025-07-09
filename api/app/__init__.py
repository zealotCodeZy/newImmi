from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # 只允许前端静态站点跨域并带cookie
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}}, supports_credentials=True)
    
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
        from . import admin
        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(admin.bp, url_prefix='/admin')
        
        # 创建数据库表
        db.create_all()
        
    return app
