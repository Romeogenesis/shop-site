from flask import Flask

from database.database import init_db
from routes.head import head_bp
from routes.register_submit import register_bp
from routes.auth_submit import auth_bp



app = Flask(__name__)
    
app.register_blueprint(head_bp)
app.register_blueprint(register_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)