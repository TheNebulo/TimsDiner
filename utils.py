import json


def load_menu():
  with open("menu.json", "r") as f:
    return json.load(f)


def save_menu(menu):
  with open('menu.json', 'w') as f:
    json.dump(menu, f)


menu = load_menu()


def validate_order(order):
  try:
    order = order.split(',')
    order = [int(x) for x in order]
    if len(order) < 2:
      return None
    if order[0] > 0:
      for item in order[1:]:
        if str(item) not in menu.keys(): return None
    return order
  except:
    return None


def calculate_cost(order):
  items, cost = order[1:], 0.00
  for item in items:
    cost += menu[str(item)][1]
  return cost


def load_orders():
  with open('orders.json', 'r') as f:
    return json.load(f)


def save_orders(orders):
  with open('orders.json', 'w') as f:
    json.dump(orders, f)


def submit_order(order):
  table, items = order[0], order[1:]
  orders = load_orders()

  order_number = len(orders["orders"]) + 1

  cost = calculate_cost(order)

  orders["total_spent"] += cost

  orders["orders"].append({
    "order_number": order_number,
    "table": table,
    "cost": cost
  })

  save_orders(orders)

  final_order = []

  for item in items:
    in_final_order = False
    for index, entry in enumerate(final_order):
      if entry[0] == item:
        final_order[index][-1] += 1
        in_final_order = True
        break
    if not in_final_order:
      final_order.append([item, menu[str(item)][0], 1])

  for item in final_order:
    update_purchased(item[1], item[2])

  return table, cost, final_order


def load_purchased():
  with open('purchased.json', 'r') as f:
    return json.load(f)


def save_purchased(purchased):
  with open('purchased.json', 'w') as f:
    json.dump(purchased, f)


def refresh_purchased():
  purchased = load_purchased()

  for item in menu.values():
    item_name = item[0]
    if item_name not in purchased:
      purchased[item_name] = 0

  save_purchased(purchased)


def update_purchased(name, quantity):
  refresh_purchased()
  purchased = load_purchased()

  purchased[name] += quantity

  save_purchased(purchased)


refresh_purchased()
