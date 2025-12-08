from flask import request, Blueprint, redirect, session

from database.add_user import add_user
from database.get_user_id import get_user_id

register_bp = Blueprint('register', __name__)


@register_bp.route('/register/submit', methods=['POST'])
def auth_submit():
    role = request.form.get('role')
    username = request.form.get('username')
    password = request.form.get('password')

    valid_roles = {'user', 'keeper', 'admin'}
    if role not in valid_roles or not username or not password:
        return "⚠️ Некорректные данные. <a href='/'>Назад</a>", 400

    role_names = {
        'user': 'Пользователь',
        'keeper': 'Кладовщик',
        'admin': 'Администратор'
    }

    if not add_user(username, password, role):
        print(role)
        return f"Пользователь с логином <strong>{username}</strong> уже существует. <a href='/'>Назад</a>", 409
    
    user_id = get_user_id(username)

    session['user_id'] = user_id

    return redirect(f'/{role}')



