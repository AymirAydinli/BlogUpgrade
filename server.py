from flask import Flask, render_template, url_for, request
import requests
from post import Post
from dotenv import load_dotenv
import os
import smtplib



load_dotenv()

app_pwd = os.getenv("APP_PWD")

response = requests.get('https://api.npoint.io/eb6cd8a5d783f501ee7d')

data = response.json()

post_objs = []

for post in data:
    post_obj = Post(post['id'], post['body'], post['date'], post['title'], post['author'], post['subtitle'],
                    post['image_url'])
    post_objs.append(post_obj)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', all_posts=post_objs)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        sender = request.form['email']
        number = request.form['phone_number']
        message = request.form['message']
        receivers = 'aaaxilles@gmail.com'

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
            connection.login(receivers, app_pwd)
            connection.sendmail(from_addr=sender,
                                to_addrs='aaaxilles@gmail.com',
                                msg=f'Subject: from {name} \n\n {message}'
                                )
            connection.close()

        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)



@app.route('/post/<int:id>')
def show_post(id):
    for post in post_objs:
        if id == post.id:
            return render_template('post.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
