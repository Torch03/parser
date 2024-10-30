import requests
from bs4 import BeautifulSoup
import csv

# URL сайта
base_url = 'https://habr.com/ru/articles/'

# Заголовки для запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Функция для получения HTML-кода страницы
def get_html(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        print(f"URL: {url}")
        print(f"Ответ: {response.text}")
        return None

# Функция для парсинга данных
def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')
    data = []

    for article in articles:
        title_tag = article.find('h2', class_='tm-title tm-title_h2')
        link_tag = article.find('a', class_='tm-title__link')
        summary_tag = article.find('div', class_='article-formatted-body')

        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = 'https://habr.com' + link_tag.get('href')
            summary = summary_tag.text.strip() if summary_tag else ''
            data.append([title, link, summary])
        else:
            print("Не удалось найти все необходимые элементы в статье")
            print(f"HTML статьи: {article}")

    return data

# Функция для записи данных в CSV файл
def write_to_csv(data):
    with open('habr_articles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Summary'])
        writer.writerows(data)

# Основная функция
def main():
    all_data = []
    page = 1
    while len(all_data) < 5000:  # Ограничение на 5000 символов
        url = f'{base_url}page{page}/'
        if page == 51:
            print(f"Пропускаем страницу {page}")
            page += 1
            continue
        html = get_html(url)
        if html:
            data = parse_data(html)
            if not data:
                break
            all_data.extend(data)
            page += 1
        else:
            break

    write_to_csv(all_data)
    print("Данные успешно сохранены в habr_articles.csv")

if __name__ == '__main__':
    main()
