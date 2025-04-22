#product class
class Product:
    def __init__(self,id,name,price):
        self.id=id
        self.name=name
        self.price=price

#products class
class Products:
    def __init__(self):
        self.products=[Product(1,'Realme',20000),Product(2,'Redmi',15000),Product(3,'Samsung',25000),Product(4,'Apple',67000),Product(5,'Vivo',17000)]
    def add(self):
        id=int(input('Enter Product Id :'))
        name=input('Enter Product Name :')
        price=int(input('Enter Product Price :'))
        self.products.append(Product(id,name,price))
        print('New Product Successfully Added to Products')
    def display(self):
        print('PRODUCT ID','  ','PRODUCT NAME',"  ",'PRODUCT PRICE')
        for product in self.products:
            
            print(product.id,'  ',product.name,"  ",product.price)
        print('\n \n')


class Cart:
    def __init__(self):
        self.cartProducts=[]
    def addToCart(self,product):
        self.cartProducts.append(product)
        print(product.name ,'  Successfully added to Cart')
    def display(self):
        print('PRODUCT ID','  ','PRODUCT NAME',"  ",'PRODUCT PRICE')
        for product in self.cartProducts:
            
            print(product.id,'  ',product.name,"  ",product.price)
        print('\n \n')
    def totalPrice(self):
        total_price=0
        for product in self.cartProducts:
            total_price+=product.price
        print('Total Amount to Buy :',total_price,'\n')

products=Products()
cart=Cart()
while True:
    

    print('1.Display Products \n 2.Display Cart \n 3.Add Product to Products \n 4.Add to Cart\n  5.Total Amount \n 6.Exit')
    choice=int(input('Enter your choice :'))
    match(choice):
        case 1:
            products.display()
            
        case 2:
            cart.display()
            
        case 3:
            products.add()
            
        case 4:
            id=int(input('Please Enter Product ID :'))
            cart.addToCart(products.products[id-1])
            
        case 5:
            cart.totalPrice()
        case 6:
            exit(1)
        
            

