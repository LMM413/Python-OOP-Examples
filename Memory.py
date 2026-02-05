"""
Memory class, contains a single private __memory dict attribute that can be 
accessed via list(), read(), add(), force_add(), delete(), and force_delete.
Supports memory addresses pointing to another memory address for add() and delete().
When defined as an object it only needs the amount of addresses to start
"""
class Memory():

    """
    Init for a memory object, takes the amount of address and thier default values
    as args, the amount of starting addresses is saved as a private variable, but
    the default value for all addresses is not saved
    """
    def __init__(self, start_address_amount: int, default_val = 0):
        self.__start_address_amount = start_address_amount
        self.__create(default_val)
        

    # Protected dict, users cannot directly write or read to the memory
    __memory = {}

    """
    Called upon the creation of a memory object, makes the amount of addresses
    specified as the memory size when the object was created, the default value
    for all values is 0, though can be given when the object is created.
    Private as it should only be used once during the creation of the object
    """
    def __create(self, default_val):
        for i in range(self.__start_address_amount):
            i = str(i)
            while len(i) < 4:
                i = '0' + i
            self.__memory.update({f'0x{i}': default_val})    
            

    """
    Displays all address and value pairs as reading memory directly is not possible
    """
    def list(self):
        print('Address | Value\n---------------')
        for i in Memory.__memory:
            print(f'{i}  :  {Memory.__memory[i]}')

    """
    Reads the value and address of a single address given
    """
    def read(self, address: str):
        print('Address | Value\n---------------')
        print(f'{address}  :  {Memory.__memory[address]}')

    """
    Allows editing or adding new address value pairs with little restriction
    If the address given contains an address as its value, it will hop to that
    Address and continue reading until it finds a non address value to override
    Will try to iterate through the value, and test for a '0x' at the start, if
    either fail it will break and add the value at the current address
    """
    def add(self, address: str, value):
        while True:
            try:
                if Memory.__memory.get(address)[0] == '0' and Memory.__memory.get(address)[1] == 'x':
                    address = Memory.__memory.get(address)
                else:
                    break
            except:
                break
        Memory.__memory.update({address: value})

    """
    Allows editing or adding new address value pairs with no restriction, 
    does not check what is as the address nor try to jump to any new addresses found
    """
    def force_add(self, address: str, value):
        Memory.__memory.update({address: value})

    
    """
    Allows deleting of address value pairs with little restriction
    If the address given contains an address as its value, it will hop to that
    Address and continue reading until it finds a non address value pair to delete 
    Will try to iterate through the value, and test for a '0x' at the start, if
    either fail it will break and delete the pair at the current address
    """
    def delete(self, address: str):
        while True:
            try:
                if Memory.__memory.get(address)[0] == '0' and Memory.__memory.get(address)[1] == 'x':
                    address = Memory.__memory.get(address)
                else:
                    break
            except:
                break
        Memory.__memory.pop(address)

    """
    Removes an address value pair based off given address with no restriction
    """
    def force_delete(self, address: str):
        Memory.__memory.pop(address)
