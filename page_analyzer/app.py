import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv

from page_analyzer import db
from page_analyzer.url_normalizer import normalize, validate
from page_analyzer.parser import parse_seo_data

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url = request.form.get('url', '').strip()
    is_valid, error_message = validate(url)
    
    if not is_valid:
        flash(error_message, 'danger')
        return render_template('index.html', url=url), 422
    
    normalized_url = normalize(url)
    existing_url = db.get_url_by_name(normalized_url)
    
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing_url['id']))
    
    try:
        url_id = db.add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=url_id))
    except Exception:
        flash('Произошла ошибка при добавлении', 'danger')
        return render_template('index.html', url=url), 500


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url_data = db.get_url_by_id(id)
    
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('list_urls')), 404
    
    try:
        response = requests.get(
            url_data['name'],
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; PageAnalyzer/1.0)'}
        )
        response.raise_for_status()
        h1, title, description = parse_seo_data(response)
        
        db.add_url_check(
            url_id=id,
            status_code=response.status_code,
            h1=h1,
            title=title,
            description=description
        )
        flash('Страница успешно проверена', 'success')
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    
    return redirect(url_for('show_url', id=id))


@app.route('/urls')
def list_urls():
    urls = db.get_all_urls()
    result_urls = []
    
    for url in urls:
        url_dict = dict(url)
        last_check = db.get_last_check(url_dict['id'])
        if last_check:
            url_dict['last_check_date'] = last_check['created_at']
            url_dict['status_code'] = last_check['status_code']
        result_urls.append(url_dict)
    
    return render_template('urls.html', urls=result_urls)


@app.route('/urls/<int:id>')
def show_url(id):
    url_data = db.get_url_by_id(id)
    
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('list_urls')), 404
    
    checks = db.get_url_checks(id)
    return render_template('url_detail.html', url=url_data, checks=checks)


@app.context_processor
def inject_now():
    from datetime import datetime
    return {'now': datetime.now()}


@app.template_filter('truncate')
def truncate_filter(s, length=200):
    if s is None:
        return ''
    s = str(s)
    if len(s) <= length:
        return s
    return s[:length] + '...'