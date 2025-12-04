from flask import request, Blueprint, redirect

from database.add_user import add_user

register_bp = Blueprint('register', __name__)


@register_bp.route('/register/submit', methods=['POST'])
def register_submit():
    role = request.form.get('role')
    username = request.form.get('username')
    password = request.form.get('password')

    valid_roles = {'user', 'warehouse', 'admin'}
    if role not in valid_roles or not username or not password:
        return "⚠️ Некорректные данные. <a href='/'>Назад</a>", 400

    role_names = {
        'user': 'Пользователь',
        'warehouse': 'Кладовщик',
        'admin': 'Администратор'
    }

    if not add_user(username, password, role):
        return f"Пользователь с логином <strong>{username}</strong> уже существует. <a href='/'>Назад</a>", 409

    return redirect(f'/{role}')

