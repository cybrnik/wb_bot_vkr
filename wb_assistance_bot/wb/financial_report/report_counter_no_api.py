import os
import uuid
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment


def report_counter(file_name, tax_rate, tax_system):
    df = pd.read_excel(file_name)
    df["Тип документа"] = df["Тип документа"].str.lower()
    df["Обоснование для оплаты"] = df["Обоснование для оплаты"].str.lower()

    # количество проданных товаров, возвращенных товаров
    sell = df[df["Тип документа"] == "продажа"][df["Обоснование для оплаты"] == "продажа"]
    sell = sell.groupby("Артикул поставщика")[("Кол-во",)].sum()
    sell = sell.rename(columns={'Кол-во': 'Кол-во проданных товаров'})

    returned = df[df["Тип документа"] == "возврат"][df["Обоснование для оплаты"] == "возврат"]
    returned = returned.groupby("Артикул поставщика")[("Кол-во",)].sum()
    returned = returned.rename(columns={'Кол-во': 'Кол-во возвращенных товаров'})
    sell = sell.join(returned, on='Артикул поставщика').fillna(0)

    sell['Кол-во проданных - возвращенных товаров'] = sell['Кол-во проданных товаров'] - sell[
        'Кол-во возвращенных товаров']

    # сумма продаж, реализованных Wildberries
    real = df[df["Тип документа"] == "продажа"]
    real = real.groupby("Артикул поставщика")[("Вайлдберриз реализовал Товар (Пр)",)].sum()

    # сумма возвратов
    ret = df[df["Тип документа"] == "возврат"]
    ret = ret.groupby("Артикул поставщика")[("Вайлдберриз реализовал Товар (Пр)",)].sum()

    res = sell.join(real, on="Артикул поставщика").join(ret, on="Артикул поставщика", rsuffix=" возвраты").fillna(0)

    # сумма продаж итоговая (продажи - возвраты)
    res["Вайлдберриз реализовал Товар (Пр)"] -= res["Вайлдберриз реализовал Товар (Пр) возвраты"]
    res = res.drop(columns=["Вайлдберриз реализовал Товар (Пр) возвраты"])
    res = res.rename(columns={"Вайлдберриз реализовал Товар (Пр)": "Сумма продажи WB (продажи - возвраты)"})

    # сумма к перечислению продавцу
    sum_to_go = df[df["Тип документа"] == "продажа"]
    sum_to_go = df.groupby("Артикул поставщика")[("К перечислению Продавцу за реализованный Товар",)].sum().rename(
        columns={"К перечислению Продавцу за реализованный Товар": "Сумма к перечислению за продажи"})
    res = res.join(sum_to_go, on="Артикул поставщика")

    # к перечислению за возвраты и общая к перечислению
    ret_sum = df[df["Тип документа"] == "возврат"]
    ret_sum = ret_sum.groupby("Артикул поставщика")[
        ("К перечислению Продавцу за реализованный Товар",)].sum().abs().rename(
        columns={"К перечислению Продавцу за реализованный Товар": "Сумма к перечислению возвратов"})
    res = res.join(ret_sum, on="Артикул поставщика").fillna(0)
    res["Сумма к перечислению продавцу"] = res["Сумма к перечислению за продажи"] - res[
        "Сумма к перечислению возвратов"]

    # сумма логистики
    log = df[df["Обоснование для оплаты"] == "логистика"]
    log = log.groupby("Артикул поставщика")[("Услуги по доставке товара покупателю",)].sum().rename(
        columns={"Услуги по доставке товара покупателю": "Сумма логистики"})
    res = res.join(log, on="Артикул поставщика", how='outer', rsuffix='log').fillna(0)

    # сумма комиссии
    res["Сумма комиссии"] = res["Сумма продажи WB (продажи - возвраты)"] - res["Сумма к перечислению продавцу"]
    res = res.drop(columns=['Сумма к перечислению за продажи', 'Сумма к перечислению возвратов'])

    # сумма штрафов
    penalty = df[df["Обоснование для оплаты"] == "штрафы"]
    penalty = penalty.groupby("Артикул поставщика")[("Общая сумма штрафов",)].sum()
    res = res.join(penalty, on="Артикул поставщика").fillna(0)
    res.reset_index(inplace=True)

    # сумма к перечислению продавцу с учетом всех расходов вб
    res['Cумма к перечислению продавцу с учетом всех расходов вб'] = res['Сумма к перечислению продавцу'] - res[
        'Сумма логистики']

    # налог
    if tax_system == "incomes":
        res["Налог"] = res["Сумма продажи WB (продажи - возвраты)"] * tax_rate / 100

    res = res.drop(columns=['index'], errors='ignore')

    reports_dir = 'reports'

    unique_filename = f"final_{uuid.uuid4().hex}.xlsx"

    final_file = os.path.join(reports_dir, unique_filename)

    res.to_excel(final_file, index=False)

    wb = openpyxl.load_workbook(final_file)
    ws = wb.active

    for row in ws.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.alignment = Alignment(
                    wrapText=True,
                    vertical='center',
                    horizontal='center',
                    textRotation=0,
                    indent=0,
                    shrinkToFit=False
                )

    for col in ws.columns:
        column = col[0].column_letter
        current_width = ws.column_dimensions[column].width
        new_width = current_width * 1.5

        ws.column_dimensions[column].width = new_width

    wb.save(final_file)

    return final_file
