from selenium.webdriver.common.by import By
from .models import WB, YM
from .settings import TABLE_WB, TABLE_YM


# Класс WBUtils, содержащий переменные и локаторы для парсинга Wildberries
class WBUtils:
    TABLE = TABLE_WB
    CLASS = WB
    URI = 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BE%D1%82%D0%BE%D0%BF%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%BE%D1%82%D0%BB%D1%8B'
    ARTICLE = (By.CLASS_NAME, "j-card-item")
    NEXT_PAGE = (By.CLASS_NAME, "pagination-next")

    REG_PRICE = "del"
    PRICE = "ins"
    RATE = "span.product-review__rating"
    RATE_COUNT = "span.product-review__count-review"
    TEXT = "p.collapsable__text"
    TABLE_SPECS = "table.product-params__table"
    ROW_SPECS = "tr.product-params__row"
    CELL_SPECS = "th.product-params__cell"


# Класс WBUtils, содержащий переменные и локаторы для парсинга Яндекс.Маркет
class YMUtils:
    TABLE = TABLE_YM
    CLASS = YM
    URI = "https://market.yandex.ru/catalog--otopitelnye-kotly/18063252/list?srnum=2324&was_redir=1&rt=9&rs=eJwdjz9LA0EUxG8NAaOthWCzkEohjVgZD64TO8UvcKVfII1p7kyjxMpGCQh2goWKcBI986fQTnEPRLRbEMRSsA5482tmh3mzb94sX1U2zW51-mTyV-2ZuhsWe27oRq5fvpnLi0M3KLous-6eUV50n0wQ7YQl2uNmiWc_a0LzIKUiZXwgJa6hp3mJQUd6kqMcCaN5_C1NEy_F3or7TDxoML2REr-JBxvCeEu50ZI8SQf_s7jvC8e1OzmNPMklKZ_K9e2R8JRpiL7Nhdfa6ddD7gdn-JuCJNoA3qDFPi3aJE644YXLH2nRo937qpwX7P9A-dUv-w1fJH1hoA0r8CkazTI9Z_McXb5onbKfS_yrUmy9-Q8DXaIS&suggest=1&suggest_type=search&suggest_text=%D0%BE%D1%82%D0%BE%D0%BF%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%BE%D1%82%D0%BB%D1%8B&hid=12385944&allowCollapsing=1&local-offers-first=0"
    ARTICLE = (By.XPATH, '//article[(@data-autotest-id="product-snippet")]')
    NEXT_PAGE = (By.CLASS_NAME, "_3e9Bd")
    FEATURES = (By.CSS_SELECTOR, "a._2S7Nj._3i2oe")

    CARD_PRICE = ("h3", "_1stjo")
    REG_PRICE = ("s", "_3vySE")
    PRICE = ("span", "_8-sD9")
    RATE = ("span", "ybvaC") 
    RATE_COUNT = ("span", "_1qYU6")
    TEXT = ("div", "_1AayP")
    SPECS = ("dl", "sZB0N")
    SPECS_KEY = "span"
    SPECS_VALUE = ("div", "_3PnEm")