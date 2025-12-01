from flask import request, Blueprint

head_bp = Blueprint('head', __name__)


@head_bp.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        html = '''
        <!DOCTYPE html>
        <html>
        <head><title>Регистрация</title></head>
        <body>
          <h2>У вас уже есть аккаунт?</h2>
          <form method="POST">
            <label><input type="radio" name="has_account" value="yes" required> Да, хочу войти</label><br>
            <label><input type="radio" name="has_account" value="no"> Нет, хочу создать новый</label><br><br>
            <button type="submit">Далее</button>
          </form>
        </body>
        </html>
        '''
        return html

    elif request.method == 'POST':
        has_account = request.form.get('has_account')

        if has_account == 'yes':
            return '''
            <h2>Вы уже зарегистрированы?</h2>
            <p>Отлично! Перейдите на <a href="/main_menu">страницу входа</a>.</p>
            <a href="/">← Назад</a>
            '''

        elif has_account == 'no':
            html = '''
            <!DOCTYPE html>
            <html>
            <head><title>Выбор роли</title></head>
            <body>
              <h2>Создание нового аккаунта</h2>
              <form method="POST" action="/register/submit">
                <label><input type="radio" name="role" value="user" required> Пользователь</label><br>
                <label><input type="radio" name="role" value="warehouse"> Кладовщик</label><br>
                <label><input type="radio" name="role" value="admin"> Администратор</label><br><br>

                <label>Логин: <input type="text" name="username" required minlength="3"></label><br><br>
                <label>Пароль: <input type="password" name="password" required minlength="6"></label><br><br>

                <button type="submit">Зарегистрироваться</button>
              </form>
              <a href="/">← Назад</a>
            </body>
            </html>
            '''
            return html

        else:
            return "⚠️ Неверный выбор. <a href='/register'>Попробуйте снова</a>", 400