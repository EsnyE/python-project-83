import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from page_analyzer import db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url = request.form.get('url', '').strip()
    
    is_valid, error_message = db.validate_url(url)
    if not is_valid:
        flash(error_message, 'danger')
        return render_template('index.html', url=url), 422
    
    normalized_url = db.normalize_url(url)
    existing_url = db.get_url_by_name(normalized_url)
    
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing_url['id']))
    
    try:
        url_id = db.add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=url_id))
    except Exception as e:
        flash('Произошла ошибка при добавлении', 'danger')
        return render_template('index.html', url=url), 500


@app.route('/urls')
def list_urls():
    urls = db.get_all_urls()

    for url in urls:
        last_check = db.get_last_check(url['id'])
        if last_check:
            url['last_check'] = last_check
            url['status_code'] = last_check['status_code']
    
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def show_url(id):
    url_data = db.get_url_by_id(id)
    
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('list_urls')), 404
    
    checks = db.get_url_checks(id)
    
    return render_template('url_detail.html', url=url_data, checks=checks)
@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url_data = db.get_url_by_id(id)
    
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('list_urls')), 404
    
    try:
        check_id = db.add_url_check(url_id=id)
        flash('Страница успешно проверена', 'success')
    except Exception as e:
        flash('Произошла ошибка при проверке', 'danger')
    
    return redirect(url_for('show_url', id=id))