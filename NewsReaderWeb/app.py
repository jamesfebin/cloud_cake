from flask import Flask,jsonify,render_template
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
    return render_template('index.html')

@app.route("/api/news")
def news():
    tech_news = News.query.filter(News.category=='tech').order_by(News.published.desc()).limit(2).all()
    entertainment_news = News.query.filter(News.category=='business').order_by(News.published.desc()).limit(2).all()
    business_news = News.query.filter(News.category=='entertainment').order_by(News.published.desc()).limit(2).all()
    news = tech_news + entertainment_news + business_news
    return news_schema.jsonify(news)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
