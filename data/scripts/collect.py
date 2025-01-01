
import requests
from bs4 import BeautifulSoup
from newspaper import Article as NewspaperArticle
import re


class Article:
    def __init__(self, url):
        self.url = url
        self.question = None
        self.text = None

    def get_article(self):
        response = requests.get(self.url)
        response.raise_for_status()  # Check if the request was successful
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        question_div = soup.find('div', class_='rn_AnswerQuestion')
        question = question_div.get_text()
        self.question = self.remove_new_lines(question)
        body = soup.find('div', class_='rn_AnswerText')
        text = body.get_text()
        text = self.remove_multiple_new_lines(text)

        self.text = text

    def print_article(self):
        print(self.question)
        print(self.text)

    def remove_multiple_new_lines(self, text):
        pattern = re.compile(r'\n+')
        text = re.sub(pattern, '\n', text)
        return text

    def remove_new_lines(self, text):
        pattern = re.compile(r'\n')
        text = re.sub(pattern, '', text)
        return text

    def remove_spaces(self, text):
        pattern = re.compile(r'\s+')
        text = re.sub(pattern, ' ', text)
        return text

    def get_file_name(self):
        # change spaces to underscores
        file_name = re.sub(r'\s+', '_', self.question)
        # remove any special characters from the question except underscores
        file_name = re.sub(r'[^a-zA-Z0-9_]', '', file_name)
        return file_name

    def save_article(self):
        file_name = self.get_file_name()
        with open(f'data\\raw\\{file_name}.txt', 'w', encoding="utf-8") as file:
            file.write("## Question\n")
            file.write(self.question)
            file.write('\n## Answer\n')
            file.write(self.text)


class ArticleCollector:
    def __init__(self):
        pass

    def parse(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all(
            'a', href=lambda href: href and '/app/answers/detail/a_id/' in href)

        for link in links:
            article_url = link.get('href')
            article_url = 'https://ask.uwindsor.ca' + article_url
            article = Article(article_url)
            article.get_article()
            article.print_article()
            article.save_article()


# # Perform natural language processing (NLP) on the article
# article.nlp()
# # Extract details
# title = article.title
# authors = article.authors
# publish_date = article.publish_date
# text = article.text
# summary = article.summary
# Print the extracted details
# url = "https://ask.uwindsor.ca/app/answers/detail/a_id/1"

# art = Article(url)
# art.get_article()
# art.save_article()
# art.print_article()

url = "https://ask.uwindsor.ca/app/answers/list/st/4/page/"

collector = ArticleCollector()
for i in range(46, 57):
    url = "https://ask.uwindsor.ca/app/answers/list/st/4/page/" + str(i)
    collector.parse(url)
