
class Product:
    def __init__(self, title, price, image, url):
        self.title = title
        self.price = price
        self.image = image
        self.url = url

    def __str__(self):
        return f"{self.title} - {self.price} - {self.url}"
    
    def filter_product(self, filter):
        return filter in self.title