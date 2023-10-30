from sqlalchemy import Column, Integer, Float, String, JSON
from sqlalchemy.orm import declarative_base
from modules.settings import TABLE_WB, TABLE_YM


Base = declarative_base()

# Класс модели данных BaseClass, содержащий общие поля для классов WB и YM
class BaseClass(Base):
    __tablename__ = "baseclass"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float, nullable=True)
    reg_price = Column(Float, nullable=True)
    rate = Column(Float, nullable=True)
    rate_count = Column(Integer, nullable=True)
    text = Column(String, nullable=True)
    specs = Column(JSON, nullable=True)

# Класс модели данных WB, наследующий поля из BaseClass
class WB(BaseClass):
    __tablename__ = TABLE_WB
    id = Column(Integer, primary_key=True)
    __mapper_args__ = {
        'inherit_condition': id == BaseClass.id
    }

# Класс модели данных YM, наследующий поля из BaseClass с дополнитьельным полем card_price
class YM(Base):
    __tablename__ = TABLE_YM
    id = Column(Integer, primary_key=True)
    card_price = Column(Float, nullable=True)
    __mapper_args__ = {
        'inherit_condition': id == BaseClass.id
    }