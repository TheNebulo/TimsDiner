import utils
import os
import time

menu = utils.load_menu()

clear_command = 'cls'


def make_order():
  print_menu()
  print(
    "\nOrder like this: Table Number, Item 1, Item 2\nSo for example, 1,4,9 means:\nTable 1 ordered a burger and a milkshake.\n"
  )
  order = input("Make your order (if you want to cancel, type cancel): ")
  if order.lower() == "cancel":
    os.system(clear_command)
    print("Order cancelled.")
    return
  order = utils.validate_order(order)
  if order == None:
    os.system(clear_command)
    print("Invalid order!\nPlease wait a second.")
    time.sleep(1)
    os.system(clear_command)
    make_order()
  else:
    table, cost, order = utils.submit_order(order)
    os.system(clear_command)
    print(f'Table {table} spent ${cost}. They ordered:')
    for item in order:
      print(f'{item[2]}x of {item[0]}. {item[1]}')


def print_menu():
  print("Menu:")
  for item_id, item_info in menu.items():
    print(f"{item_id}. {item_info[0]} - ${item_info[1]}")


def edit_menu():
  while True:
    os.system(clear_command)
    print_menu()
    print("Options:")
    print("1. Add item")
    print("2. Edit item")
    print("3. Delete item")
    print("q. Go back")
    option = input("Choose an option: ")

    if option == '1':
      item_name = input("Enter the new item name: ")
      try:
        item_price = float(input("Enter the new item price: "))
      except ValueError:
        print("Invalid price. Please try again.")
        continue

      item_id = str(len(menu) + 1)
      menu[item_id] = [item_name, item_price]
      utils.save_menu(menu)

    elif option == '2':
      try:
        item_id = input("Enter the item ID of the item you want to edit: ")
        if item_id not in menu:
          raise ValueError()

        item_name = input("Enter the new item name: ")
        try:
          item_price = float(input("Enter the new item price: "))
        except ValueError:
          print("Invalid price. Please try again.")
          continue
        else:
          if item_price <= 0:
            print("Invalid price. Please try again.")
            continue

        menu[item_id] = [item_name, item_price]
        utils.save_menu(menu)

      except ValueError:
        print("Invalid item ID. Please try again.")

    elif option == '3':
      try:
        item_id = input("Enter the item ID of the item you want to delete: ")
        if item_id not in menu:
          raise ValueError()

        del menu[item_id]
        utils.save_menu(menu)

      except ValueError:
        print("Invalid item ID. Please try again.")

    elif option.lower() == 'q':
      break

    else:
      print("Invalid option. Please try again.")


def print_orders(orders):
  if orders["orders"] == []:
    print("No orders have been placed yet.")
    return
  for order in orders["orders"]:
    print(
      f"Order Number: {order['order_number']}, Table: {order['table']}, Cost: ${order['cost']}"
    )


def print_purchased():
  purchased = utils.load_purchased()
  for item, quantity in purchased.items():
    print(f"{item}: {quantity}")


def main_menu():
  os.system(clear_command)
  print("Tim's Diner Management Tool")
  print("---------------------------")
  print("Options:")
  print("1. Make an order")
  print("2. View all orders")
  print("3. Find all orders per table")
  print("4. Find an order by order number")
  print("5. View how many of each item has been purchased")
  print("6. View menu")
  print("7. Edit menu")
  print("q. Quit")
  return input("\nChoose an option: ")


while True:
  option = main_menu()
  os.system(clear_command)

  if option == '1':
    make_order()
    input("\nPress enter to continue: ")

  elif option == '2':
    print("All Orders:")
    orders = utils.load_orders()
    print_orders(orders)
    input("\nPress enter to continue: ")

  elif option == '3':
    try:
      table = int(input("Enter the table number: "))
    except ValueError:
      print("Invalid table number.")
      input("\nPress enter to continue: ")
      continue

    orders = utils.load_orders()
    table_orders = {
      "total_spent": 0.0,
      "orders":
      [order for order in orders["orders"] if order["table"] == table]
    }
    if table_orders["orders"]:
      print(f"Orders for Table {table}:")
      print_orders(table_orders)
      input("\nPress enter to continue: ")
    else:
      print(f"No orders found for Table {table}.")
      input("\nPress enter to continue: ")

  elif option == '4':
    try:
      order_number = int(input("Enter the order number: "))
    except ValueError:
      print("Invalid order number.")
      input("\nPress enter to continue: ")
      continue

    orders = utils.load_orders()
    order = next(
      (order
       for order in orders["orders"] if order["order_number"] == order_number),
      None)
    if order is not None:
      print(f"Order Number {order_number}:")
      print(f"Table: {order['table']}, Cost: ${order['cost']}")
      input("\nPress enter to continue: ")
    else:
      print(f"No order found with order number {order_number}.")
      input("\nPress enter to continue: ")

  elif option == '5':
    print("Purchased Items:")
    print_purchased()
    input("\nPress enter to continue: ")

  elif option == '6':
    print_menu()
    input("\nPress enter to continue: ")

  elif option == '7':
    edit_menu()

  elif option.lower() == 'q':
    while True:
      os.system(clear_command)
      confirm = input("Are you sure you want to quit? (y/n) ")
      if confirm.lower() == "y":
        os.system(clear_command)
        print("Goodbye!")
        quit()
      elif confirm.lower() == "n":
        break
      else:
        os.system(clear_command)
        print("I didn't quite get you. Try again in a second.")
        time.sleep(1)
        os.system(clear_command)

  else:
    print("Invalid option. Please try again.")
    input("\nPress enter to continue: ")
