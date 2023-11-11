from flask import Flask, render_template, url_for
import requests 
from post import Post

response = requests.get('https://api.npoint.io/eb6cd8a5d783f501ee7d')

data = response.json()

post_objs = []

for post in data:
    post_obj = Post(post['id'], post['body'] ,post['date'], post['title'], post['author'], post['subtitle'], post['image_url'])
    post_objs.append(post_obj)
    


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', all_posts = post_objs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post/<int:id>')
def show_post(id):
    for post in post_objs:
        if id == post.id:
            return render_template('post.html', post=post)



if __name__ == "__main__":
    app.run(debug=True)
