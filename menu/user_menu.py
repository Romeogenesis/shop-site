from flask import Blueprint, request, render_template_string, session, redirect, url_for
from models.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['GET', 'POST'])
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('head.registration'))

    user_id = session['user_id']
    user = User()
    message = ""
    current_order = None

    all_products = user.get_all_products()

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'create_order':
                product_id = request.form.get('product_id')
                if not product_id:
                    message = "⚠️ Выберите товар"
                else:
                    try:
                        product_id = int(product_id)
                        product = next((p for p in all_products if p["id"] == product_id), None)
                        if not product:
                            message = "❌ Товар не найден"
                        else:
                            order_id = user.create_order(
                                user_id=user_id,
                                total_price=product["price"],
                                product_names=[product["name"]]
                            )
                            message = f"✅ Заказ №{order_id} создан"
                            current_order = user.get_order(user_id, order_id)
                    except ValueError:
                        message = "⚠️ Некорректный ID товара"

            elif action == 'get_order':
                order_id_str = request.form.get('order_id')
                if not order_id_str:
                    message = "⚠️ Укажите номер заказа"
                else:
                    try:
                        order_id = int(order_id_str)
                        current_order = user.get_order(user_id, order_id)
                        if current_order:
                            message = f"✅ Заказ №{order_id} загружен"
                        else:
                            message = f"❌ Заказ не найден или не принадлежит вам"
                    except ValueError:
                        message = "⚠️ Номер заказа должен быть числом"

            elif action == 'add_product':
                order_id_str = request.form.get('order_id')
                product_id = request.form.get('product_id')
                if not order_id_str or not product_id:
                    message = "⚠️ Укажите заказ и выберите товар"
                else:
                    try:
                        order_id = int(order_id_str)
                        product_id = int(product_id)
                        product = next((p for p in all_products if p["id"] == product_id), None)
                        if not product:
                            message = "❌ Товар не найден"
                        elif user.add_product_to_order(user_id, order_id, product["name"]):
                            order = user.get_order(user_id, order_id)
                            if order:
                                total = sum(
                                    next((p["price"] for p in all_products if p["name"] == name), 0)
                                    for name in order["products"]
                                )
                                conn = user._get_connection()
                                try:
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "UPDATE orders SET total_price = ? WHERE id = ? AND user_id = ?",
                                        (total, order_id, user_id)
                                    )
                                    conn.commit()
                                finally:
                                    conn.close()
                            message = f"✅ Товар '{product['name']}' добавлен"
                            current_order = user.get_order(user_id, order_id)
                        else:
                            message = f"❌ Не удалось добавить товар (возможно, заказ не ваш)"
                    except ValueError:
                        message = "⚠️ Некорректные данные"

            elif action == 'remove_product':
                order_id_str = request.form.get('order_id')
                product_name = request.form.get('product_name')
                if not order_id_str or not product_name:
                    message = "⚠️ Укажите заказ и товар"
                else:
                    try:
                        order_id = int(order_id_str)
                        if user.remove_product_from_order(user_id, order_id, product_name):
                            order = user.get_order(user_id, order_id)
                            if order:
                                total = sum(
                                    next((p["price"] for p in all_products if p["name"] == name), 0)
                                    for name in order["products"]
                                )
                                conn = user._get_connection()
                                try:
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "UPDATE orders SET total_price = ? WHERE id = ? AND user_id = ?",
                                        (total, order_id, user_id)
                                    )
                                    conn.commit()
                                finally:
                                    conn.close()
                            message = f"✅ Товар '{product_name}' удалён"
                            current_order = user.get_order(user_id, order_id)
                        else:
                            message = f"❌ Товар не найден в заказе или заказ не ваш"
                    except ValueError:
                        message = "⚠️ Ошибка данных"

            elif action == 'set_payment':
                order_id_str = request.form.get('order_id')
                method = request.form.get('payment_method')
                if not order_id_str or not method:
                    message = "⚠️ Укажите заказ и способ оплаты"
                elif method not in ['наличные', 'карта']:
                    message = "⚠️ Способ оплаты: только 'наличные' или 'карта'"
                else:
                    try:
                        order_id = int(order_id_str)
                        if user.set_payment_method(user_id, order_id, method):
                            message = f"✅ Оплата '{method}' установлена"
                            current_order = user.get_order(user_id, order_id)
                        else:
                            message = f"❌ Не удалось установить оплату (заказ не найден или не ваш)"
                    except ValueError:
                        message = "⚠️ Некорректный номер заказа"

        except Exception as e:
            message = f"❌ Ошибка: {e}"

    return render_template_string('''
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Меню пользователя</title>
<style>body{font-family:sans-serif;max-width:900px;margin:20px auto;padding:20px}
.card{background:#fff;padding:20px;margin:15px 0;border-radius:8px;box-shadow:0 1px 3px #0001}
.btn{padding:8px 16px;border:none;border-radius:4px;cursor:pointer;margin:4px}
.btn-primary,.btn-success,.btn-info{color:#fff}
.btn-primary{background:#0d6efd}
.btn-success{background:#198754}
.btn-info{background:#0dcaf0}
.btn-warning{background:#ffc107;color:#000}
input,select{padding:6px 10px;border:1px solid #ccc;border-radius:4px}
.msg{padding:10px;margin:15px 0;border-radius:4px}
.msg-ok{background:#d4edda;color:#155724}
.msg-err{background:#f8d7da;color:#721c24}
</style></head><body>

<h1>🛒 Меню пользователя</h1>

{% if message %}
<div class="msg {% if '✅' in message %}msg-ok{% elif '❌' in message %}msg-err{% endif %}">
{{ message|safe }}</div>
{% endif %}

<div class="card">
<h3>🆕 Создать заказ</h3>
<form method="POST">
<input type="hidden" name="action" value="create_order">
<select name="product_id" required>
  <option value="">Выберите первый товар</option>
  {% for p in all_products %}
  <option value="{{ p.id }}">{{ p.name }} ({{ p.price }} ₽)</option>
  {% endfor %}
</select>
<button type="submit" class="btn btn-success">Создать</button>
</form>
</div>

<div class="card">
<h3>🔍 Загрузить заказ</h3>
<form method="POST">
<input type="hidden" name="action" value="get_order">
<input name="order_id" type="number" placeholder="№ заказа" required style="width:120px">
<button type="submit" class="btn btn-primary">Показать</button>
</form>
</div>

{% if current_order %}
<div class="card">
<h3>📦 Заказ №{{ current_order.id }}</h3>
<p><strong>Статус:</strong> {{ current_order.status }}</p>
<p><strong>Оплата:</strong> 
  {% if current_order.payment == 'наличные' %}
    💵 Наличные
  {% elif current_order.payment == 'карта' %}
    💳 Карта
  {% else %}
    {{ current_order.payment }}
  {% endif %}
</p>
<p><strong>Итого:</strong> {{ current_order.total_price }} ₽</p>

<h4>Товары:</h4>
<ul style="list-style:none;padding-left:0">
{% for p in current_order.products %}
  <li style="margin:4px 0">
    {{ p }}
    <form method="POST" style="display:inline">
      <input type="hidden" name="action" value="remove_product">
      <input type="hidden" name="order_id" value="{{ current_order.id }}">
      <input type="hidden" name="product_name" value="{{ p }}">
      <button type="submit" class="btn btn-warning" style="padding:2px 6px;font-size:12px">✕</button>
    </form>
  </li>
{% endfor %}
</ul>

<h4>➕ Добавить товар</h4>
<form method="POST">
<input type="hidden" name="action" value="add_product">
<input type="hidden" name="order_id" value="{{ current_order.id }}">
<select name="product_id" required>
  <option value="">Выберите товар</option>
  {% for p in all_products %}
  <option value="{{ p.id }}">{{ p.name }} ({{ p.price }} ₽)</option>
  {% endfor %}
</select>
<button type="submit" class="btn btn-info">Добавить</button>
</form>

<h4>💳 Оплата</h4>
<form method="POST">
<input type="hidden" name="action" value="set_payment">
<input type="hidden" name="order_id" value="{{ current_order.id }}">
<select name="payment_method" required>
  <option value="">Выберите</option>
  <option value="наличные">Наличные</option>
  <option value="карта">Карта</option>
</select>
<button type="submit" class="btn btn-primary">Применить</button>
</form>
</div>
{% endif %}

</body></html>
''', message=message, current_order=current_order, all_products=all_products)