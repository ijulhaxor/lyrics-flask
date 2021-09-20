from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from bs4 import BeautifulSoup as bs
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)

class NameForm(FlaskForm):
    key    = StringField('Judul Lagu : ')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    key  = form.key.data
    title = ""
    lyrics = ""
    lirik = ""
    message = ""
    if form.validate_on_submit():
        userAgent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
        page      = requests.get(f'https://www.google.com/search?q=lirik+lagu+{key}', headers=userAgent)
        s         = bs(page.content, 'html.parser')

        try:
            artis     = s.find('h2', class_='qrShPb').text
        except Exception as e:
            message = "Lirik lagu tidak ditemukan"

        try:
            artis     = s.find('h2', class_='qrShPb').text
            judul     = s.find('div', class_='wwUB2c').text
            lirik     = s.find_all('span', jsname="YS01Ge")
            title = f'{artis} - {judul}'
        except Exception as e:
            pass

        try:
            mess      = s.find('a', class_='gL9Hy').text
            userAgent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
            page      = requests.get(f'https://www.google.com/search?q={mess}', headers=userAgent)
            s         = bs(page.content, 'html.parser')
            title = f'{artis} - {judul}'
        except Exception as e:
            pass

    return render_template('index.html', form=form, message=message, title=title, lyrics=lirik)

# running server
# if __name__ == '__main__':
#     app.run(port=80)
    # app.run(host="192.168.43.2", port=5000)
    # app.run(host="192.168.43.2", port=5000, debug=True)
