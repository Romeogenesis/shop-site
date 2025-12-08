from flask import request, Blueprint, redirect, session

from database.check_user import check_user
from database.get_user_role import get_user_role
from database.get_user_id import get_user_id


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/submit', methods=['POST'])
def auth_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if not check_user(username, password):
        return f"Пароль или логин указаны не верно</strong>. <a href='/'>Назад</a>", 409
    
    
    return redirect(f'/{get_user_role(username)}')
