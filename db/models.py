
import sqlalchemy as sqlAl
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List


class Base(DeclarativeBase): pass

url_max_len = 2048

class CarAd(Base):
    __tablename__ = 'Car_ad'

    id: Mapped[int] = mapped_column(sqlAl.Integer, primary_key=True)
    external_id: Mapped[int] = mapped_column(sqlAl.Integer, unique=True) #TODO: set to an url-field
    source_href: Mapped[str] = mapped_column(sqlAl.VARCHAR(url_max_len)) #TODO: set to an url-field
    pic_href: Mapped[str] = mapped_column(sqlAl.VARCHAR(url_max_len))
    model_name: Mapped[str] = mapped_column(sqlAl.VARCHAR(70))
    price_in_USD: Mapped[int] = mapped_column(sqlAl.Integer)
    bonded_search_demands: Mapped[List['SearchDemand']] = relationship(
        back_populates='bonded_car_ads'        ,
        secondary='Car_ad__Search_demand__Bond',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f"id={self.id}," \
               f" external_id={self.external_id}," \
               f" source_href={self.source_href}," \
               f" pic_href={self.pic_href}," \
               f" model_name={self.model_name}," \
               f" price_in_USD={self.price_in_USD})"

class SearchDemand(Base):
    __tablename__ = 'Search_demand'

    id: Mapped[int] = sqlAl.Column('id', sqlAl.Integer, primary_key=True)
    search_href: Mapped[str] = sqlAl.Column('search_href', sqlAl.VARCHAR(url_max_len))
    target_chat_id: Mapped[int] = sqlAl.Column('target_chat_id', sqlAl.Integer)
    bonded_car_ads: Mapped[List['CarAd']] = relationship(
        back_populates='bonded_search_demands' ,
        secondary='Car_ad__Search_demand__Bond',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f"Search_demand(id={self.id}," \
               f" search_href={self.search_href}," \
               f" target_chat_id={self.target_chat_id})"


class BondCarAdSearchDemand(Base):
    __tablename__ = 'Car_ad__Search_demand__Bond'

    car_ad: Mapped[int] = mapped_column(sqlAl.ForeignKey('Car_ad.id', ondelete='CASCADE'), primary_key=True)
    search_demand: Mapped[int] = mapped_column(sqlAl.ForeignKey('Search_demand.id', ondelete='CASCADE'), primary_key=True)