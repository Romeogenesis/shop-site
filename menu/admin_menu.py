from flask import Blueprint, request, render_template_string
from database.add_users import add_user
from database.delete_user import delete_user
from database.all_users_info import get_all_users
from database.add_product import add_product
from database.delete_product import delete_product
from database.all_products_info import get_all_products

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    message = ""
    users = []
    products = []

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'list_users':
                users = get_all_users() or []
                message = f"Загружено {len(users)} пользователей"
            elif action == 'list_products':
                products = get_all_products() or []
                message = f"Загружено {len(products)} товаров"
            elif action == 'add_user':
                name = request.form.get('user_name')
                password = request.form.get('user_pass')
                role = request.form.get('user_role', 'user')
                if name and password:
                    if add_user(name, password, role):
                        message = f"✅ Пользователь '{name}' добавлен"
                    else:
                        message = f"❌ Пользователь '{name}' уже существует"
                else:
                    message = "⚠️ Логин и пароль обязательны"
            elif action == 'add_product':
                name = request.form.get('prod_name')
                price_str = request.form.get('prod_price', '').strip()

                if not name or not price_str:
                    message = "⚠️ Название и цена обязательны"
                else:
                    try:
                        price = int(price_str)  # ← только целое число
                        if price < 0:
                            message = "⚠️ Цена должна быть ≥ 0"
                        elif add_product(name, price):
                            message = f"✅ Товар '{name}' добавлен"
                        else:
                            message = f"❌ Товар '{name}' уже существует"
                    except ValueError:
                        message = "⚠️ Цена должна быть целым числом (например, 1000)"
            elif action == 'delete_user':
                name = request.form.get('del_name')
                if name:
                    if delete_user(name):
                        message = f"✅ Пользователь '{name}' удалён"
                    else:
                        message = f"❌ Пользователь '{name}' не найден"
                else:
                    message = "⚠️ Укажите имя"
            elif action == 'delete_product':
                name = request.form.get('del_name')
                if name:
                    if delete_product(name):
                        message = f"✅ Товар '{name}' удалён"
                    else:
                        message = f"❌ Товар '{name}' не найден"
                else:
                    message = "⚠️ Укажите название"
        except Exception as e:
            message = f"❌ Ошибка: {e}"

    users = users or (get_all_users() or [])
    products = products or (get_all_products() or [])

    return render_template_string('''
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Админка</title>
<style>body{font-family:sans-serif;max-width:900px;margin:20px auto;padding:20px}
.card{background:#fff;padding:20px;margin:15px 0;border-radius:8px;box-shadow:0 1px 3px #0001}
.btn{padding:8px 16px;border:none;border-radius:4px;cursor:pointer;margin:4px}
.btn-primary{background:#0d6efd;color:#fff}
.btn-success{background:#198754;color:#fff}
.btn-danger{background:#dc3545;color:#fff}
input,select{padding:6px 10px;border:1px solid #ccc;border-radius:4px}
.msg{padding:10px;margin:15px 0;border-radius:4px}
.msg-ok{background:#d4edda;color:#155724}
.msg-err{background:#f8d7da;color:#721c24}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:8px;text-align:left;border-bottom:1px solid #eee}
th{background:#f8f9fa}
</style></head><body>

<h1>Админ-панель</h1>

{% if message %}
<div class="msg {% if '✅' in message %}msg-ok{% elif '❌' in message %}msg-err{% endif %}">
{{ message|safe }}</div>
{% endif %}

<div class="card">
<h3>Просмотр</h3>
<form method="POST"><input type="hidden" name="action" value="list_users">
<button type="submit" class="btn btn-primary">Пользователи</button></form>
<form method="POST" style="display:inline"><input type="hidden" name="action" value="list_products">
<button type="submit" class="btn btn-primary">Товары</button></form>
</div>

<div class="card">
<h3>Добавить пользователя</h3>
<form method="POST">
<input type="hidden" name="action" value="add_user">
<input name="user_name" placeholder="Логин" required>
<input name="user_pass" type="password" placeholder="Пароль" required>
<select name="user_role"><option value="user">user</option>
<option value="warehouse">warehouse</option><option value="admin">admin</option></select>
<button type="submit" class="btn btn-success">Добавить</button>
</form>
</div>

<div class="card">
<h3>Добавить товар</h3>
<form method="POST">
<input type="hidden" name="action" value="add_product">
<input name="prod_name" placeholder="Название" required>
<input name="prod_price" type="number" step="1" min="0" placeholder="Цена (целое число)" required>
<button type="submit" class="btn btn-success">Добавить</button>
</form>
</div>

<div class="card">
<h3>Удалить</h3>
<form method="POST">
<input type="hidden" name="action" value="delete_user">
<input name="del_name" placeholder="Имя пользователя" required>
<button type="submit" class="btn btn-danger">Удалить юзера</button>
</form>
<form method="POST" style="margin-top:8px">
<input type="hidden" name="action" value="delete_product">
<input name="del_name" placeholder="Название товара" required>
<button type="submit" class="btn btn-danger">Удалить товар</button>
</form>
</div>

{% if users %}
<div class="card">
<h3>Пользователи ({{ users|length }})</h3>
<table><tr><th>ID</th><th>Логин</th><th>Роль</th></tr>
{% for u in users %}<tr><td>{{ u.id }}</td><td>{{ u.name }}</td><td>{{ u.role }}</td></tr>{% endfor %}
</table></div>
{% endif %}

{% if products %}
<div class="card">
<h3>Товары ({{ products|length }})</h3>
<table><tr><th>ID</th><th>Название</th><th>Цена</th></tr>
{% for p in products %}<tr><td>{{ p.id }}</td><td>{{ p.name }}</td><td>{{ p.price }} ₽</td></tr>{% endfor %}
</table></div>
{% endif %}

</body></html>
''', message=message, users=users, products=products)