import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        url = request.form.get('url')
        flash('URL успешно добавлен', 'success')
        return redirect(url_for('urls'))
    
    urls_list = []
    return render_template('urls.html', urls=urls_list)


@app.route('/urls/<int:id>')
def url_detail(id):
    url_data = {'id': id, 'name': f'https://example{id}.com'}
    return render_template('url_detail.html', url=url_data)