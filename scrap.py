import requests
from bs4 import BeautifulSoup
from product import Product
# https://www.youtube.com/watch?v=gJCrr-FzhMY&ab_channel=RoCode

# URL to be scraped
# https://listado.mercadolibre.com.ar/libros-revistas-comics/libros-fisicos/babilonia_Desde_51_OrderId_PRICE_NoIndex_True

class Target:
    def __init__(self, target, query):
        self.target = target
        self.query = query
        self.target_url = self.get_target_url()
        self.url = self.generate_query_url()
        self.request = self.get_request()
        self.soup = self.get_soup()
        self.product_list = self.generate_product_list()
        self.title_keyword = "Windows 11"
        
    def get_target_url(self):
        if self.target == "MeLi":
            return f"https://listado.mercadolibre.com.ar/"

    def generate_query_url(self):
        return f"{self.target_url}{self.query}"

    def get_request(self):
        return requests.get(self.url)

    def get_soup(self):
        return BeautifulSoup(self.request.content, "html.parser")

    def get_title_list(self):
        return [title.text for title in self.get_title()]

    def get_title(self):
        return self.soup.find_all("h2", class_="ui-search-item__title")

    def get_product_url_list(self):
        return [product_url["href"] for product_url in self.get_product_url()]
    
    def get_product_url(self):
        return self.soup.find_all("a", class_="ui-search-item__group__element ui-search-link")
    
    def get_price_list(self):
        return [price.text for price in self.get_price()]
    
    def get_price(self):
        return self.soup.find_all("span", class_="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript")
    
    def get_image_list(self):
        return [image["src"] for image in self.get_image()]
    
    def get_image(self):
        return self.soup.find_all("img", class_="ui-search-result-image__element")
    
    def generate_product_list(self):
        list = zip(self.get_title_list(), self.get_price_list(), self.get_image_list(), self.get_product_url_list())
        filtered_list = filter(lambda x: "" in x[0] and x[1] != "" and x[2] != "" and x[3] != "", list)
        return [Product(title, price, image, url) for title, price, image, url in filtered_list]
    
    def get_product(self, number):
        return self.product_list[number]
    
    def delete_product(self, number):
        self.product_list.pop(number)
