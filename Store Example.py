from abc import ABC, abstractmethod

"""
An example of multiple classes working together via inheritance and composition. 
Also with some dunder methods for operator overloading. Not perfect but a decent
showcase of what can be done with classes.
"""

class Asset():
    
    ID_LENGTH = 6
    total_assets = 0
    
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
        Asset.total_assets += 1

    @property
    def name(self): return self._name
    
    @property
    def id(self): return self._id
        
    @id.setter
    def id(self, new_id):
        if len(str(new_id)) > Asset.ID_LENGTH:
             raise ValueError("ID must be 6 digits or less")
        elif not isinstance(new_id, int):
            raise ValueError("ID must be only integers")
        elif new_id <= 0:
            raise ValueError("ID must be larger than 0")
        elif len(str(new_id)) == Asset.ID_LENGTH:
            self._id = new_id
        else:
            new_id = str(new_id)
            while len(new_id) < Asset.ID_LENGTH:
                new_id = '0' + new_id
            # Must keep ID as a string or the extra 0s at the start go away
            self._id = new_id
            
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise ValueError("Name must be a string") 
        elif new_name.isalpha():
            self._name = new_name
        else:
            self._name = None
            raise ValueError("Name must be only letters")

    def __str__(self):
        return f'Name: {self._name} - ID: {self.id} - Object Type: {type(self)}'


class Container(ABC):

    @abstractmethod
    def list_items(self, **kwargs): pass

    @abstractmethod
    def add_product(self, **kwargs): pass

    @abstractmethod
    def del_product(self, **kwargs): pass


class Store():
    def __init__(self, name: str, id: int):
        super().__init__(name, id)
        self.shelves = []

    def add_shelf(self, shelf):
        if isinstance(shelf, Shelf):
            self.shelves.append(shelf)
            print(f'Added shelf: {shelf.name}')
        else:
            raise ValueError('Only Shelf objects can be added to the Store')


class Shelf(Asset, Container):
    def __init__(self, name: str, id: int, slot_width: int, slot_height: int, is_cooled: bool):
        super().__init__(name, id)
        self.slot_width = slot_width
        self.slot_height = slot_height
        self.is_cooled = is_cooled
        self.contents = [[None for _ in range(slot_width)] for _ in range(slot_height)]

    @property
    def slot_width(self): return self._slot_width
    
    @property
    def slot_height(self): return self._slot_height

    @slot_width.setter
    def slot_width(self, new_slot_width):
        if not isinstance(new_slot_width, int):
            raise ValueError("Slot width must be only integers")
        elif new_slot_width <= 0 or new_slot_width >= 100:
            raise ValueError("Slot width must be larger than 0 and less than 100")
        else: self._slot_width = new_slot_width

    @slot_height.setter
    def slot_height(self, new_slot_height):
        if not isinstance(new_slot_height, int):
            raise ValueError("Slot height must be only integers")
        elif new_slot_height <= 0 or new_slot_height >= 100:
            raise ValueError("Slot height must be larger than 0 and less than 100")
        else: self._slot_height = new_slot_height
        
    def __str__(self):
        return f"""
Shelf name: {self._name}
Shelf ID: {self._id}
Shelf width: {self._slot_width}
Shelf height: {self._slot_height}
Shelf cooling: {self.is_cooled}
Use list_items() to see shelf contents
"""  
    
    def list_items(self):
        for i in self.contents:
            print('\n')
            for j in i:
                if isinstance(j, Product):
                    print(f"{j.quantity} {j.name}(s) at ${j.price}", end=',')
                else:
                    print(j, end=',')
        print("\n")

    def add_product(self, product, x_loc: int, y_loc: int):
        if not isinstance(product, Product):
            raise ValueError("Product must be of the Product class")
        elif x_loc < 0 or x_loc >= self.slot_width or y_loc < 0 or y_loc >= self.slot_height:
            raise ValueError("Item location must exist inside the Shelf")
        elif product.need_cooled is True and self.is_cooled is False:
            raise ValueError(f"Item ({product._name}) requires a cooled shelf, this shelf is not cooled")
        else:
            if self.contents[y_loc][x_loc] is not None:
                raise ValueError(f"Slot occupied by {self.contents[y_loc][x_loc]._name}, use del_product() to remove")
            self.contents[y_loc][x_loc] = product

    def del_product(self, x_loc: int, y_loc: int):
        if x_loc < 0 or x_loc > self.slot_width or y_loc < 0 or y_loc > self.slot_height:
            raise ValueError("Item delete location must exist inside the Shelf") 
        elif self.contents[y_loc][x_loc] is None:
            print("Slot already empty")
        else:
            print(f"Item {self.contents[y_loc][x_loc]._name} deleted")
            self.contents[y_loc][x_loc] = None

    def set_discount(self, new_discount: float):
        count = 0
        try:
            new_discount = float(new_discount)
        except:  
            raise ValueError("Discount must be a float 0-1")
        else:
            if new_discount < 0 or new_discount > 1:
                raise ValueError("Discount must be a float 0-1")
            else:
                for i in self.contents:
                    for j in i:
                        if isinstance(j, Product):
                            j.discount = new_discount
                            count += j.quantity
                print(f"{count} item(s) set to a {new_discount * 100}% discount")

    def clear(self):
        count = 0
        for y, row in enumerate(self.contents):  
            for x, item in enumerate(row):    
                if isinstance(item, Product):
                    count += item.quantity
                    self.contents[y][x] = None
        print(f"Cleared {count} item(s) from shelf")


class Product(Asset):
    def __init__(self, name: str, id: int, price: float, quantity: int, need_cooled: bool):
        super().__init__(name, id)
        self.quantity = quantity
        self.need_cooled = need_cooled
        self.discount = 0
        self.price = price

    @property # make it so discount itself does its own math
    def price(self):
        return round(self._price * (1 - self.discount), 2)
    
    @property
    def quantity(self): return self._quantity
        
    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, float):
            raise ValueError("Price must be a float")
        elif new_price <= 0:
            raise ValueError("Price must be larger than 0")
        else: self._price = round((new_price), 2)
        
    @quantity.setter # isinstance vs :int for all of these ###
    def quantity(self, new_quantity):
        if not isinstance(new_quantity, int):
            raise ValueError("Quantity must be a integer")
        elif new_quantity <= 0:
            raise ValueError("Quantity must be larger than 0")
        else: self._quantity = new_quantity

    def __add__(self, other):
        return round((self.price * self.quantity) + (other.price * other.quantity), 2)

    def __sub__(self, other): 
        return round((self.price * self.quantity) - (other.price * other.quantity), 2)

    def __str__(self):
        return f"""
Product name {self.name}
Product ID: {self.id}
Product Price: ${self.price}
Product Quantity: {self.quantity}
Product Discount: {self.discount}
Product Needs Cooling: {self.need_cooled}"""

    def set_discount(self, new_discount: float): # also try vs if for error checks here
        if not isinstance(new_discount, float) or new_discount < 0 or new_discount > 1:
            raise ValueError("Discount must be a float 0-1")
        else: self.discount = new_discount
        

#### Testing ####

apple = Product("Apple", 12, 2.99, 2, True)

bananna = Product("Bananna", 13, 4.99, 1, False)

print(apple)

shelf = Shelf("fruitshelf", 1234, 3, 5, True)

shelf.add_product(apple, 0, 0)

shelf.add_product(bananna, 0, 1)

shelf.list_items()

shelf.del_product(0, 1)

shelf.set_discount(.2)

shelf.list_items()

print(Asset.total_assets)

shelf.clear()

shelf.list_items()

print(apple - bananna)

print(shelf)


