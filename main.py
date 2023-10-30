from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

import pandas as pd
import json

from modules.functions import get_articles_info

from modules.utils import WBUtils, YMUtils
from modules.settings import PSTGRS

# Создание подключения к базе данных
engine = create_engine(PSTGRS)

# Установка и настройка драйвера для работы с браузером
service=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.set_window_size(800, 600)

# Поиск и получение информации с карточек товаров с маркетплейсов
df_wb = get_articles_info(driver, WBUtils)
df_ym = get_articles_info(driver, YMUtils, features = True)

# Проверка наличия таблиц в базе данных и их создание при необходимости
if inspect(engine).has_table(WBUtils.TABLE):
    print(f'Таблица {WBUtils.TABLE} существует')
else:
    WBUtils.CLASS.__table__.create(bind=engine)

if inspect(engine).has_table(YMUtils.TABLE):
    print(f'Таблица {YMUtils.TABLE} существует')
else:
    YMUtils.CLASS.__table__.create(bind=engine)

# Создание сессии для работы с базой данных и запись полученных данных в таблицы
Session = sessionmaker(bind=engine)
session = Session()
df_wb.to_sql(WBUtils.TABLE, con=engine, if_exists='replace', index=False) #if_exists='append'
df_ym.to_sql(YMUtils.TABLE, con=engine, if_exists='replace', index=False) #if_exists='append'  
session.close()

# df_specs_ym = df_ym['specs'].apply(lambda x: json.loads(str(x))).apply(pd.Series)
# df_ext_ym = pd.concat([df_ym.drop(['specs'], axis=1), df_specs_ym], axis=1)

# df_specs_wb = df_wb['specs'].apply(lambda x: json.loads(str(x))).apply(pd.Series)
# df_ext_wb = pd.concat([df_wb.drop(['specs'], axis=1), df_specs_wb], axis=1)