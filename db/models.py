
import sqlalchemy as sqlAl
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase): pass

url_max_len = 2048

class CarAd(Base):
    __tablename__ = 'Car_ad'

    id: Mapped[int] = mapped_column(sqlAl.Integer, primary_key=True)
    external_id: Mapped[int] = mapped_column(sqlAl.Integer, unique=True)
    source_href: Mapped[str] = mapped_column(sqlAl.VARCHAR(url_max_len))
    pic_href: Mapped[str] = mapped_column(sqlAl.VARCHAR(url_max_len))
    model_name: Mapped[str] = mapped_column(sqlAl.VARCHAR(70))
    price_in_USD: Mapped[int] = mapped_column(sqlAl.Integer)

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

    def __repr__(self) -> str:
        return f"Search_demand(id={self.id}," \
               f" search_href={self.search_href}," \
               f" target_chat_id={self.target_chat_id})"

