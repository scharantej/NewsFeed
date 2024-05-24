
from flask import Flask, render_template, request, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_news')
async def get_news():
  async with aiohttp.ClientSession() as session:
    async with session.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=API_KEY') as response:
      news = await response.json()
      return jsonify(news)

if __name__ == '__main__':
  app.run()
