import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import advertise_api

advert_id = {}

advert_id['9819'] = 19508986
advert_id['30077'] = 17373900
advert_id['1266'] = 17245390

articles = {
    "1266": 54414568,
    "30077": 92094244,
    "9819": 223291011
}


def get_product_positions(driver, articles):
    products = driver.find_elements(By.CLASS_NAME, "product-card__wrapper")
    positions = {}

    for index, product in enumerate(products):
        try:
            link = product.find_element(By.CLASS_NAME, "product-card__link").get_attribute("href")
            articul = re.search(r'/catalog/(\d+)/detail.aspx', link).group(1) if link else None
            if articul:
                articul = int(articul)
                if articul in articles.values():
                    position = index + 1
                    positions[articul] = position
        except Exception as e:
            print(f"Error: {e}")
            continue

    return positions

def advertise_30077(pos_30077, pos_1266):
    print("Информация по кампании 30077:")
    cpm, type, status = advertise_api.get_auto_campaign_bid_type_status(advert_id['30077'])
    if status == 9:
        print(f"Текущая ставка: {cpm}")
        if (pos_30077 > 5):
            if cpm + 25 <= 700:
                if pos_1266 != -1000:
                    if pos_30077 - pos_1266 >= 1:
                        print("Увеличиваю ставку")
                        new_cpm = cpm + 25
                        advertise_api.change_campaign_bid(advert_id=advert_id['30077'], campaign_type=type,
                                                          cpm=new_cpm)
                else:
                    print("Увеличиваю ставку")
                    new_cpm = cpm + 25
                    advertise_api.change_campaign_bid(advert_id=advert_id['30077'], campaign_type=type,
                                                      cpm=new_cpm)
        else:
            if pos_30077 == 5:
                print("На краю, стоим")
            else:
                print("Уменьшаю ставку")
                new_cpm = cpm - 25
                advertise_api.change_campaign_bid(advert_id=advert_id['30077'], campaign_type=type, cpm=new_cpm)
    else:
        print('Кампания 30077 на паузе')

def advertise_1266(pos_1266):
    print("Информация по кампании 1266:")
    cpm, type, status = advertise_api.get_search_campaign_bid_type_status(advert_id['1266'])
    if status == 9:
        print(f"Текущая ставка: {cpm}")
        if (pos_1266 > 2):
            if cpm + 25 <= 800:
                print("Увеличиваю ставку")
                new_cpm = cpm + 25
                advertise_api.change_campaign_bid(advert_id=advert_id['1266'], campaign_type=type,
                                                  cpm=new_cpm)
        else:
            if pos_1266 == 2:
                print("На краю, стоим")
            else:
                print("Уменьшаю ставку")
                new_cpm = cpm - 25
                advertise_api.change_campaign_bid(advert_id=advert_id['1266'], campaign_type=type, cpm=new_cpm)
    else:
        print('Кампания 1266 на паузе')

def advertise_9819(pos_1266, pos_9819):
    print("Информация по кампании 9819:")
    cpm, type, status = advertise_api.get_search_campaign_bid_type_status(advert_id['9819'])
    if status == 9:
        print(f"Текущая ставка: {cpm}")
        if (pos_9819 > 4):
            if cpm + 25 <= 800:
                if pos_1266 != -1000:
                    if pos_9819 - pos_1266 >= 1:
                        print("Увеличиваю ставку")
                        new_cpm = cpm + 25
                        advertise_api.change_campaign_bid(advert_id=advert_id['9819'], campaign_type=type,
                                                          cpm=new_cpm)
                else:
                    print("Увеличиваю ставку")
                    new_cpm = cpm + 25
                    advertise_api.change_campaign_bid(advert_id=advert_id['9819'], campaign_type=type,
                                                      cpm=new_cpm)
        else:
            if pos_9819 == 4:
                print("На краю, стоим")
            else:
                print("Уменьшаю ставку")
                new_cpm = cpm - 25
                advertise_api.change_campaign_bid(advert_id=advert_id['9819'], campaign_type=type, cpm=new_cpm)
    else:
        print('Кампания 9819 на паузе')


def main():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")  # Безголовый режим
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Настройка драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        while True:
            url = "https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B8%D0%BD%D1%86%D0%B5%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%B1%D1%80%D0%BE%D0%B2%D0%B5%D0%B9"
            driver.get(url)

            time.sleep(3)

            with open("cookies.json") as f:
                cookies = json.load(f)
            with open("local_storage.json") as f:
                local_storage = json.load(f)

            for key, value in local_storage.items():
                driver.execute_script("window.localStorage.setItem('{}', '{}');".format(key, value))

            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print("Failed to add cookie:", e)

            driver.refresh()

            time.sleep(3)

            positions = get_product_positions(driver, articles)

            pos_1266 = -1000
            pos_9819 = -1000
            pos_30077 = -1000

            if articles['30077'] in positions.keys():
                pos_30077 = positions[articles['30077']]
            if articles['1266'] in positions.keys():
                pos_1266 = positions[articles['1266']]
            if articles['9819'] in positions.keys():
                pos_9819 = positions[articles['9819']]

            print(f"Позиция 1266: {pos_1266}")
            print(f"Позиция 30077: {pos_30077}")
            print(f"Позиция 9819: {pos_9819}")

            print()

            advertise_30077(pos_30077, pos_1266)

            print()

            advertise_1266(pos_1266)

            print()

            advertise_9819(pos_1266, pos_9819)

            print("\n")

            time.sleep(150)

    finally:
        # Закрытие драйвера
        driver.quit()


if __name__ == "__main__":
    main()
