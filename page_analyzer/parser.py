from bs4 import BeautifulSoup


def parse_seo_data(response):
    if response.apparent_encoding:
        response.encoding = response.apparent_encoding
    
    soup = BeautifulSoup(response.text, 'html.parser')

    h1_tag = soup.find('h1')
    h1 = h1_tag.text.strip() if h1_tag else ''

    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ''

    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag.get('content', '').strip() if desc_tag else ''
    
    return h1, title, description