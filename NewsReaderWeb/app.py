from flask import Flask,jsonify
from database import init_db
from sqlalchemy.ext.serializer import loads, dumps
from models import News
from flask_marshmallow import Marshmallow

import json
app = Flask(__name__)
ma = Marshmallow(app)


class NewsSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'summary', 'image','link','category','published')

news_item_schema = NewsSchema()
news_schema = NewsSchema(many=True)


@app.route("/")
def home():
    tech_news = News.query.filter(News.category=='tech').order_by(News.published.desc()).limit(2).all()
    entertainment_news = News.query.filter(News.category=='business').order_by(News.published.desc()).limit(2).all()
    business_news = News.query.filter(News.category=='entertainment').order_by(News.published.desc()).limit(2).all()
    news = tech_news + entertainment_news + business_news
    html = ''
    old_category = ''
    index = 0
    for news_item in news:
        html = html + "<center>"
        if old_category != news_item.category:
            html = html + "<h1>" + news_item.category.capitalize() +"</h1>"
            old_category = news_item.category
        if news_item.image != '':
            html = html + "<img width=70% src='"+news_item.image+"'/>"
        html = html + " <a style='text-decoration:none;' href='"+ news_item.link + "'>"+ "<p style='color:blue' >" + news_item.title+ "</p></a>"
        html = html + "</center>"
    return html

@app.route("/api/news")
def news():
    tech_news = News.query.filter(News.category=='tech').order_by(News.published.desc()).limit(2).all()
    entertainment_news = News.query.filter(News.category=='business').order_by(News.published.desc()).limit(2).all()
    business_news = News.query.filter(News.category=='entertainment').order_by(News.published.desc()).limit(2).all()
    news = tech_news + entertainment_news + business_news
    news = news_schema.dump(news)
    return json.dumps(news)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
