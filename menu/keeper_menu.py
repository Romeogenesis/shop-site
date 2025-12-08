# keeper_menu.py
from flask import Blueprint, request, render_template_string
from models.keeper import Keeper

keeper_bp = Blueprint('keeper', __name__)


@keeper_bp.route('/keeper', methods=['GET', 'POST'])
def keeper_dashboard():
    keeper = Keeper()
    message = ""
    orders = []

    filter_status = request.args.get('status') 
    if filter_status not in ('в сборке', 'готов', None):
        filter_status = None

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'update_status':
                order_id_str = request.form.get('order_id')
                new_status = request.form.get('new_status')

                if not order_id_str or not new_status:
                    message = "⚠️ Не указан заказ или статус"
                else:
                    try:
                        order_id = int(order_id_str)
                        if keeper.update_order_status(order_id, new_status):
                            message = f"✅ Статус заказа №{order_id} изменён на «{new_status}»"
                        else:
                            message = f"❌ Заказ №{order_id} не найден или статус не изменился"
                    except ValueError:
                        message = "⚠️ Некорректный номер заказа"

        except Exception as e:
            message = f"❌ Ошибка: {e}"

    orders = keeper.get_all_orders(status_filter=filter_status)

    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>📦 Меню кладовщика</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 1000px; margin: 20px auto; padding: 20px; background: #f8f9fa; }
    .header { text-align: center; margin-bottom: 30px; }
    .filters { margin: 15px 0; text-align: center; }
    .btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin: 0 4px; }
    .btn-primary { background: #0d6efd; color: white; }
    .btn-success { background: #198754; color: white; }
    .btn-warning { background: #ffc107; color: black; }
    .card { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    .order { margin-bottom: 20px; padding: 15px; border-left: 4px solid #0d6efd; }
    .order.status-ready { border-left-color: #198754; }
    .order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .order-id { font-weight: bold; font-size: 1.1em; }
    .status-badge { padding: 4px 10px; border-radius: 12px; font-size: 0.85em; }
    .status-in-progress { background: #e7f1ff; color: #0d6efd; }
    .status-ready { background: #d4edda; color: #155724; }
    .products ul { padding-left: 20px; margin: 8px 0; }
    .products li { margin: 4px 0; }
    .msg { padding: 12px; margin: 15px 0; border-radius: 6px; }
    .msg-ok { background: #d4edda; color: #155724; }
    .msg-err { background: #f8d7da; color: #721c24; }
    .no-orders { text-align: center; color: #6c757d; padding: 30px; }
  </style>
</head>
<body>

<div class="header">
  <h1>📦 Меню кладовщика</h1>
  {% if message %}
    <div class="msg {% if '✅' in message %}msg-ok{% elif '❌' in message %}msg-err{% endif %}">
      {{ message|safe }}
    </div>
  {% endif %}
</div>

<div class="filters">
  <a href="{{ url_for('keeper.keeper_dashboard') }}" class="btn {% if not request.args.get('status') %}btn-primary{% else %}btn-outline-primary{% endif %}">Все заказы</a>
  <a href="{{ url_for('keeper.keeper_dashboard', status='в сборке') }}" class="btn {% if request.args.get('status') == 'в сборке' %}btn-warning{% else %}btn-outline-primary{% endif %}">В сборке</a>
  <a href="{{ url_for('keeper.keeper_dashboard', status='готов') }}" class="btn {% if request.args.get('status') == 'готов' %}btn-success{% else %}btn-outline-primary{% endif %}">Готовые</a>
</div>

{% if orders %}
  <div class="card">
    <h3>Список заказов (всего: {{ orders|length }})</h3>
    
    {% for order in orders %}
      <div class="order {% if order.status == 'готов' %}status-ready{% endif %}">
        <div class="order-header">
          <div>
            <span class="order-id">Заказ №{{ order.id }}</span>
            <span class="status-badge {% if order.status == 'готов' %}status-ready{% else %}status-in-progress{% endif %}">
              {{ order.status }}
            </span>
          </div>
          <div>
            <form method="POST" style="display:inline">
              <input type="hidden" name="action" value="update_status">
              <input type="hidden" name="order_id" value="{{ order.id }}">
              {% if order.status == 'в сборке' %}
                <input type="hidden" name="new_status" value="готов">
                <button type="submit" class="btn btn-success" title="Отметить как готовый">✅ Готов</button>
              {% else %}
                <input type="hidden" name="new_status" value="в сборке">
                <button type="submit" class="btn btn-warning" title="Вернуть в сборку">🔄 В сборку</button>
              {% endif %}
            </form>
          </div>
        </div>

        <div class="details">
          <p><strong>Оплата:</strong> 
            {% if order.payment == 'наличные' %}💵 Наличные{% else %}💳 Карта{% endif %}
          </p>
          <p><strong>Итого:</strong> {{ order.total_price }} ₽</p>
          <div class="products">
            <strong>Товары:</strong>
            <ul>
              {% for p in order.products %}
                <li>{{ p }}</li>
              {% endfor %}
            </ul>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
{% else %}
  <div class="card no-orders">
    <p>Нет заказов {% if filter_status %}со статусом «{{ filter_status }}»{% endif %}.</p>
  </div>
{% endif %}

</body>
</html>
''', message=message, orders=orders, request=request)