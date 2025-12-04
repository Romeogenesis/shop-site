from flask import Flask

from database.database_users import init_users_db
from database.database_products import init_products_db
from database.database_orders import init_orders_db
from routes.head import head_bp
from routes.register_submit import register_bp
from routes.auth_submit import auth_bp
from menu.admin_menu import admin_bp
from menu.user_menu import user_bp



app = Flask(__name__)
    
app.register_blueprint(head_bp)
app.register_blueprint(register_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    init_users_db()
    init_products_db()
    init_orders_db()
    app.run(debug=True, host='127.0.0.1', port=5000)