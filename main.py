from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas
import collections
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def years_word_form(age):
    last_number = age % 10
    pre_last_number = age // 10 % 10
    if last_number >= 2 and last_number <= 4:
        if pre_last_number == 1:
            write_year = "лет"
        else:
            write_year = "года"
    elif last_number >= 5 and last_number <= 9 or last_number == 0:
        write_year = "лет"
    elif last_number == 1:
        if pre_last_number == 1:
            write_year = "лет"
        else:
            write_year = "год"
    return write_year
wines = pandas.read_excel("wine3.xlsx", na_values=['N/A', 'NA'], keep_default_na=False).to_dict("records")
grouped_wines = collections.defaultdict(list)
for wine in wines:
    grouped_wines[wine["Категория"]].append(wine)
print(grouped_wines)
template = env.get_template('template.html')
now_year = datetime.now().year
foundation_year = 1920
age = now_year - foundation_year
rendered_page = template.render(
    age=age,
    age_word=years_word_form(age),
    wines=grouped_wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
