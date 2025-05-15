from datetime import datetime, timedelta
from wb_assistance_bot.wb.supply_notifier.wb_get_info import Statistics

key = ""
wb_bot = Statistics(key=key)

current_date = datetime.now().date()
last_day = current_date - timedelta(days=1)
last_day = last_day.strftime("%Y-%m-%d")
first_day = current_date - timedelta(days=7)
first_day = first_day.strftime("%Y-%m-%d")

orders = wb_bot.get_orders(date_from=first_day)
remains = wb_bot.get_remains(date_from=first_day)

warehouses_sales = {}

for order in orders:
    if (not order["isCancel"]) and (order["orderType"] == "Клиентский"):
        article = order["supplierArticle"]
        warehouse = order["warehouseName"]
        if warehouse in warehouses_sales:
            if article in warehouses_sales[warehouse]:
                warehouses_sales[warehouse][article] += 1
            else:
                warehouses_sales[warehouse][article] = 1
        else:
            warehouses_sales[warehouse] = {}
            warehouses_sales[warehouse][article] = 1

warehouses_quantities = {}

for remain in remains:
    article = remain["supplierArticle"]
    warehouse = remain["warehouseName"]
    quantity = remain["quantity"]
    if quantity > 0:
        if warehouse in warehouses_quantities:
            if article in warehouses_quantities[warehouse]:
                print("опа")
            else:
                warehouses_quantities[warehouse][article] = quantity
        else:
            warehouses_quantities[warehouse] = {}
            warehouses_quantities[warehouse][article] = quantity

days_to_notify = 8

for warehouse in warehouses_sales.keys():
    for article in warehouses_sales[warehouse]:
        mean_sales = warehouses_sales[warehouse][article] // 7
        mean_sales += mean_sales * 0.1  # средние продажи увеличиваем на 10% в силу роста
        mean_sales = int(mean_sales)
        if mean_sales > 2:
            if warehouse in warehouses_quantities:
                if article in warehouses_quantities[warehouse]:
                    days_left = warehouses_quantities[warehouse][article] / mean_sales
                    if days_left <= days_to_notify:
                        days_left = int(days_left)
                        print(warehouse, article, days_left)
