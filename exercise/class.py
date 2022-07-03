# Python program to
# demonstrate private methods

class Base:
    # Creating a Base class
    def fun(self):
        # Declaring public method
        print("Public method")
        
    def __fun(self):
        # Declaring private method
        print("Private method")

# Creating a derived class
class Derived(Base):
    def __init__(self):
        # Calling constructor of
        # Base class
        Base.__init__(self)
            
    def call_public(self):
        # Calling public method of base class
        print("\nInside derived class")
        self.fun()
            
    def call_private(self):
        # Calling private method of base class
        self.__fun()

    def virtual_fun(self):
        ...

# Driver code
obj1 = Base()

# Calling public method
obj1.fun()

obj2 = Derived()
obj2.call_public()
obj2.virtual_fun()

# Uncommenting obj1.__fun() will
# raise an AttributeError

# Uncommenting obj2.call_private()
# will also raise an AttributeError
