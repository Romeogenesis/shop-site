from flask import request, Blueprint

from database.check_user import check_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/submit', methods=['POST'])
def register_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if not check_user(username, password):
        return f"Пароль или логин указаны не верно</strong>. <a href='/'>Назад</a>", 409

    return f'''
    <h2>Успешная регистрация!</h2>
    <p><strong>Логин:</strong> {username}</p>
    <p>Теперь вы можете <a href="/main_menu">войти</a>.</p>
    '''

