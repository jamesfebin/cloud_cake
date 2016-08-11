from sqlalchemy import Column, Integer, String,Text,Numeric
from database import Base
from sqlalchemy.inspection import inspect



class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    summary = Column(Text)
    image = Column(Text)
    link = Column(Text)
    category = Column(String(50))
    published = Column(Numeric)

    def __init__(self, title=None, summary=None, image=None, link=None, category=None, published=None):
        self.title = title
        self.summary = summary
        self.image = image
        self.link = link
        self.category = category
        self.published = published

    def __repr__(self):
        return '<News %r>' % (self.title)

    def to_json(self):
        return dict(id=self.id,
                    title=self.title,
                    summary=self.summary,
                    image=self.image,
                    link=self.link,
                    category=self.category,
                    published=self.published)