from flask import Flask, render_template, url_for, request
import requests
from post import Post
from dotenv import load_dotenv
import os
import smtplib



load_dotenv()

app_pwd = os.getenv("APP_PWD")
email_account = os.getenv("EMAIL")

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
        email = request.form['email']
        phone = request.form['phone_number']
        message = request.form['message']
        send_email(name, email, phone, message)

        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(email_account, app_pwd)
        connection.sendmail(email_account, email_account, message)




@app.route('/post/<int:id>')
def show_post(id):
    for post in post_objs:
        if id == post.id:
            return render_template('post.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
