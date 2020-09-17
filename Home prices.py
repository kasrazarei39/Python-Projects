import re
import mysql.connector
import requests
from bs4 import BeautifulSoup
from sklearn import tree

detail = list()
print('takes time; please wait...')
for j in range(1, 5):
    # Web scrape
    r = requests.get(
        'https://ihome.ir/rent-residential-apartment/th-tehran?locations=iran.th.tehran&property_type=residential'
        '-apartment&paginate=30&page=%s&is_sale=0&source=website&order_by=deposit&order_by_type=desc' % j)   # different pages of site
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find_all('div', {'class': 'completeDeposit-value'})
    output = soup.find_all('span', {'class': 'property-detail__icons-item__value'})
    temp = list(output)
    for i in range(len(price)):
        year = lambda x: '0' if x == 'نوساز' else x
        correct_price = lambda x: int(x) / 1000 if len(x) > 3 else x
        detail.append([temp[3 * i].text.strip(), year(temp[3 * i + 1].text.strip()), temp[3 * i + 2].text.strip(),
                       correct_price(''.join(re.findall(r'\d+', price[i].text.strip())))])

# Create databases
user = input('mysql user: ')
password_host = input("mysql password: ")
host = input('host: ')
database = input('database: ')
table = input('table: ')
cnx = mysql.connector.connect(user=user, password=password_host,
                              host=host)
cursor = cnx.cursor()
cursor.execute("CREATE DATABASE if not exists " + database)
cursor.execute("use " + database)
cursor.execute("CREATE table if not exists " + table +
               '(area varchar(30), year varchar(30), bedrooms varchar(30), price varchar(30));')

x = list()
y = list()
for i in range(len(detail)):
    cursor.execute('INSERT INTO ' + table + ' VALUES (\'%s\', \'%s\',\'%s\', \'%s\');' % (
        detail[i][0], detail[i][1], detail[i][2], detail[i][3]))
    cnx.commit()
    x.append(detail[i][:3])
    y.append(detail[i][3])
cnx.close()

# Machine Learning
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
area = input('area: ')
year = input('year: ')
bedrooms = input('bedrooms: ')
new_place = [[area, year, bedrooms]]
print('price: ', clf.predict(new_place))
