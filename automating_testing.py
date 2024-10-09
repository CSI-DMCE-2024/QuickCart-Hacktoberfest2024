class Square:
    def __init__(self, side):
        &quot;&quot;&quot; creates a square having the given side
        &quot;&quot;&quot;
        self.side = side

    def area(self):
        &quot;&quot;&quot; returns area of the square
        &quot;&quot;&quot;
        return self.side**2

    def perimeter(self):
        &quot;&quot;&quot; returns perimeter of the square
        &quot;&quot;&quot;
        return 4 * self.side

    def __repr__(self):
        &quot;&quot;&quot; declares how a Square object should be printed
        &quot;&quot;&quot;
        s = 'Square with side = ' + str(self.side) + '\n' + \
        'Area = ' + str(self.area()) + '\n' + \
        'Perimeter = ' + str(self.perimeter())
        return s


if __name__ == '__main__':
    # read input from the user
    side = int(input('enter the side length to create a Square: '))
    
    # create a square with the provided side
    square = Square(side)

    # print the created square
    print(square)
