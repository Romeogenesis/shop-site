from flask import request, Blueprint, render_template # Добавлен render_template

head_bp = Blueprint('head', __name__)


@head_bp.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        # Вместо возврата строки HTML, рендерим шаблон index.html
        return render_template('index.html')

    elif request.method == 'POST':
        has_account = request.form.get('has_account')

        if has_account == 'yes':
            # Рендерим шаблон login.html
            return render_template('login.html')

        elif has_account == 'no':
            # Рендерим шаблон register.html
            return render_template('register.html')

        else:
            return "⚠️ Неверный выбор. <a href='/'>Попробуйте снова</a>", 400