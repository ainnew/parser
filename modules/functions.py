import json
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

# Функция получения ссылок на страницы карточек товаров
def _get_page_articles_links(driver, utils):
    """
    Возвращает список ссылок на карточки товара, собранные с текущей страницы категории
    При скроллинге в браузере подгружаются все теги со ссылками на карточки товара для получения всех ссылок на странице
    Параметры:
        driver : драйвер для работы с браузером
        utils : данные для поиска тегов и навигации (локатор
            ARTICLE - локатор для элементов с информацией о товарах на странице категории,
        )
    Возвращает:
        list : список ссылок на карточки товара
    """
    rep = 0
    previous_articles_count = 0
    while True:
        # Эмуляция скроллинга для получения всех ссылок на карточки товара со страницы категории
        driver.execute_script("window.scrollBy(0, 500)")
        wait = WebDriverWait(driver, timeout=10)
        articles = wait.until(expected_conditions.presence_of_all_elements_located(utils.ARTICLE))
        
        articles_count = len(articles)
        if articles_count == previous_articles_count:
            rep += 1
        else:
            rep = 0
        if rep == 10:
            break
        previous_articles_count = articles_count
        print(articles_count)
    article_links = []

    # Сбор ссылок на карточки товара в рамках страницы категории
    for article in articles:
        article_link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if article_link:
            article_links.append(article_link)
    return article_links

# Функция добавления полученных ссылок на страницы карточек товаров с каждой страницы категории
def get_all_pages_articles_links(driver, utils):
    """
    Возвращает полный список ссылок на карточки товара со всех страниц категории
    При скроллинге в браузере подгружаются все теги со ссылками на карточки товара для получения всех ссылок на странице
    Параметры:
        driver : драйвер для работы с браузером
        utils : данные для поиска тегов и навигации (локатор
            NEXT_PAGE - локатор для кнопки перехода на следующую страницу с товарами
        )
    Возвращает:
        list : список ссылок на карточки товара
    """
    all_article_links = []
    page_num = 1
    print('page_num' , page_num)

    # count = 0 # тест
    while True:
        driver.get(url = utils.URI + f"&page={page_num}")
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
        all_article_links += _get_page_articles_links(driver, utils)
        try:
            driver.implicitly_wait(1)
            driver.find_element(*utils.NEXT_PAGE)
            page_num += 1
            print('page_num' , page_num)
        except NoSuchElementException:
            print("Элемент не найден на странице")
            break
        # count += 1 # тест
        # if count == 2: # тест
        #     break # тест
    print(len(all_article_links))
    return all_article_links

# Функция для парсинга страницы товара
def get_articles_info(driver, utils, features = False):
    """
    Возвращает датафрейм с данными из карточек товара со всех страниц категории.
    Переходит на страницы карточек товаров и парсит html-код с помощью библиотеки BeautifulSoup, записывая данные в датафрейм
    Для Яндекс.Маркет требуется дополнительный переход для получения всех характеристик товара
    Параметры:
        driver : драйвер для работы с браузером
        utils : данные для поиска тегов и навигации (локаторы
            FEATURES - дополнительный переход на страницу характеристик товара (Яндекс.Маркет),
            CARD_PRICE - цена по карте (Яндекс.Маркет),
            REG_PRICE - регулярная цена (прежняя цена) (Яндекс.Маркет, Wildberries),
            PRICE - цена со скидкой (текущая цена) (Яндекс.Маркет, Wildberries),
            RATE - рейтинг товара (Яндекс.Маркет, Wildberries), 
            RATE_COUNT - количество оценок (Яндекс.Маркет, Wildberries),
            TEXT - описание товара (Яндекс.Маркет, Wildberries),
            SPECS - переход к списку (Яндекс.Маркет),
            SPECS_KEY - характеристика (Яндекс.Маркет),
            SPECS_VALUE - значение характеристики (текущая цена) (Яндекс.Маркет),
            TABLE_SPECS - переход к списку (Wildberries),
            ROW_SPECS - переход к элементу списка (Wildberries),
            CELL_SPECS - характеристика (Wildberries)
        )
        features :  bool (default False), переключение для использования других атрибутов тегов и навигации (значение True для Яндекс.Маркет)
    Записывает:
        датафрейм с данными из карточек товара в файл csv с именем таблицы базы данных
    Возвращает:
        df : датафрейм с данными из карточек товара
    """
    df = pd.DataFrame() #columns=utils.CLASS.__table__.columns.keys()[1:]
    all_article_links = get_all_pages_articles_links(driver, utils)
    articles_count = 0

    # Переход по всем ссылкам на карточки товара для парсинга
    for article_link in all_article_links: #[:7]  # тест
        articles_count += 1
        driver.get(article_link)
        print(articles_count, article_link)

        # Дополнительный переход на страницу Яндекс.Маркет для получения всех необходимых атрибутов в случае сущестования параметра features
        if features:
            wait = WebDriverWait(driver, 10)
            features_tag = wait.until(expected_conditions.presence_of_element_located(utils.FEATURES))
            features_link = features_tag.get_attribute("href")
            driver.get(features_link)

        # Дожидаемся появления тега в html-коде
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "h1")))
        
        # Парсинг html-кода с помощью BeautifulSoup
        bs = BeautifulSoup(driver.page_source, 'html.parser')

        # Получаем название товара
        title = bs.find("h1").text.strip()

        # Получаем информацию c Яндекс.Маркет в случае сущестования параметра features
        if features:
            # Получаем цену товара со скидкой по карте
            tag_card_price = bs.find(utils.CARD_PRICE[0], class_= utils.CARD_PRICE[1])
            if tag_card_price is not None:
                card_price =''.join(filter(str.isdigit, tag_card_price.text))
            else:
                card_price = None

            # Получаем регулярную цену товара
            tag_reg_price = bs.find(utils.REG_PRICE[0], class_= utils.REG_PRICE[1])
            if tag_reg_price is not None:
                reg_price =''.join(filter(str.isdigit, tag_reg_price.text))
            else:
                reg_price = None
            
            # Получаем цену со скидкой
            tag_price = bs.find(utils.PRICE[0], class_= utils.PRICE[1])
            if tag_price is not None:
                if reg_price:
                    price =''.join(filter(str.isdigit, tag_price.text))[:-len(reg_price)]
                else:
                    price =''.join(filter(str.isdigit, tag_price.text))
            else:
                price = None

            # Получаем рейтинг товара
            tag_rate = bs.find(utils.RATE[0], class_= utils.RATE[1])
            if tag_rate is not None:
                rate = rate = tag_rate.text.strip()
            else:
                rate = None

            # Получаем количество отзывов о товаре
            tag_rate_count = bs.find(utils.RATE_COUNT[0], class_= utils.RATE_COUNT[1])
            if tag_rate_count is not None:
                rate_count = ''.join(filter(str.isdigit, tag_rate_count.text))
            else:
                rate_count = None

            # Получаем описание товара
            text = bs.find(utils.TEXT[0], class_= utils.TEXT[1]).text

            # Получаем характеристики товара
            specs = bs.find_all(utils.SPECS[0], class_= utils.SPECS[1])
            specs_dict = {}
            for spec in specs:
                specs_dict[spec.find(utils.SPECS_KEY).text.strip()] = spec.find(utils.SPECS_VALUE[0], class_= utils.SPECS_VALUE[1]).text.strip()
            # Создаем временный датафрейм с полученными данными
            temp_df = pd.DataFrame({'title':[title], 'card_price':[card_price], 'price':[price], 'reg_price':[reg_price], 'rate':[rate], 'rate_count':[rate_count], 'text':[text], 'specs': [specs_dict]}) #
        
        # Иначе получаем информацию c Wildberries
        else:
            # Получаем регулярную цену товара
            tag_reg_price = bs.find(utils.REG_PRICE)
            if tag_reg_price is not None:
                reg_price =''.join(filter(str.isdigit, tag_reg_price.text))
            else:
                reg_price = None
            
             # Получаем цену со скидкой
            tag_price = bs.find(utils.PRICE)
            if tag_price is not None:
                price =''.join(filter(str.isdigit, tag_price.text))
            else:
                price = None

            # Получаем рейтинг товара
            tag_rate = bs.select(utils.RATE)[0]
            if tag_rate is not None:
                rate = tag_rate.text.strip()
            else:
                rate = None

            # Получаем количество отзывов о товаре
            tag_rate_count = bs.select(utils.RATE_COUNT)[0]
            if tag_rate_count is not None:
                rate_count = ''.join(filter(str.isdigit, tag_rate_count.text))
            else:
                rate_count = None

            # Получаем описание товара
            text = bs.select(utils.TEXT)[0].text

            # Получаем характеристики товара
            tables = bs.select(utils.TABLE_SPECS)
            specs_dict = {}
            for table in tables:
                specs = table.select(utils.ROW_SPECS)
                for spec in specs:
                    cell1 = spec.select(utils.CELL_SPECS)[0]
                    # cell2 = spec.find("td", class_="product-params__cell")
                    specs_dict[cell1.text.strip()] = cell1.next_sibling.text.strip()
            # Создаем временный датафрейм с полученными данными
            temp_df = pd.DataFrame({'title':[title], 'price':[price], 'reg_price':[reg_price], 'rate':[rate], 'rate_count':[rate_count], 'text':[text], 'specs': [specs_dict]})
        
        # Добавляем данные временного датафрейм в сводный датафрейм
        df = pd.concat([df, temp_df], ignore_index=True)

        print(articles_count, reg_price, price, title, rate, rate_count)
        print('specs_len:', len(specs_dict))
        # print('specs_dict:', specs_dict)
        print('df_shape:', df.shape)
        # print(df)

   # Преобразуем столбец со списком характеристик в формат json и сохраняем датафрейм в файл
    df['specs'] = df['specs'].apply(lambda x: json.dumps(x, ensure_ascii=False))
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    df.to_csv(f'{utils.TABLE}.csv', index = False)
    # print(df.columns)
    return df