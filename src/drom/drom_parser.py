from bs4 import BeautifulSoup

extract_html_node_attr = lambda attr: lambda html_node: html_node.get(attr)
extract_html_node_value = lambda html_node: html_node.get_text() 

def parse_car(html):
    soup = BeautifulSoup(html, 'html.parser')
    car = {}
    car['Модель'] = extract_html_node_value(soup.find('h1', {'class': 'css-cgwg2n e18vbajn0'}))
    car['Цена'] = extract_html_node_value(soup.find('div', {'class': 'css-1hu13v1 e162wx9x0'}))
    params = list(
        map(
            extract_html_node_value,
            soup.find_all('th', {'class': 'css-k5ermf ezjvm5n0'})
        )
    )
    param_values = list(
        map(
            extract_html_node_value,
            soup.find_all('td', {'class': 'css-1uz0iw8 ezjvm5n1'})
        )
    )
    for param, param_value in zip(params, param_values):
        car[param] = param_value

    return car

def parse_cars_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    attr_extracter = extract_html_node_attr('href')
    return list(
        map(
            attr_extracter,
            soup.find_all('a', {
                'data-ftid': 'bulls-list_bull'
            })
        )
    )

def parse_car_brands(html):
    soup = BeautifulSoup(html, 'html.parser')
    return list(
        map(
            extract_html_node_value, 
            soup.find_all('a', {
                'class':'css-171rdfx ebqjjri2'
                }
            )
        )
    )