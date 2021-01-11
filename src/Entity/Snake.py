import copy


class Body:
    def __init__(self, init_poz, color, dim):
        self.poz = init_poz
        self.color = color
        self.last_poz = init_poz
        self.dim = dim


class Snake:
    def __init__(self, head, dim):
        self.__body = [head]
        self.__dimension = dim
        self.__fed = 0
        self.__dir = (0, -1)
        self.__next_dir = (0, -1)
        self.__speed = 2
        self.__g = 0
        self.__r = 0
        self.__b = 0
        self.__body_color = (0, 0, 0)
        self.__commands = ['g = 255',
                           'r = 255',
                           'b = 125',
                           'g = -255',
                           'b = 130',
                           'g = 125',
                           'r = -255',
                           'g = 130',
                           'r = 125',
                           'b = -255',
                           'r = 130']
        self.__cmd_poz = 0

    @property
    def next_dir(self):
        return self.__next_dir

    @next_dir.setter
    def next_dir(self, value):
        self.__next_dir = value

    @property
    def body(self):
        return self.__body

    @property
    def dim(self):
        return self.__dimension

    @property
    def head(self):
        return self.__body[0]

    def eat(self):
        self.__fed += self.__dimension

    def new_color(self):
        red = self.__body_color[0]
        green = self.__body_color[1]
        blue = self.__body_color[2]
        if self.__g > 0:
            green = green + 1
            self.__g = self.__g - 1
        elif self.__g < 0:
            green = green - 1
            self.__g = self.__g + 1

        if self.__r > 0:
            red = red + 1
            self.__r = self.__r - 1
        elif self.__r < 0:
            red = red - 1
            self.__r = self.__r + 1

        if self.__b > 0:
            blue = blue + 1
            self.__b = self.__b - 1
        elif self.__b < 0:
            blue = blue - 1
            self.__b = self.__b + 1
        if (self.__b == 0) & (self.__r == 0) & (self.__g == 0):
            ldict = {}
            exec(self.__commands[self.__cmd_poz], globals(), ldict)
            try:
                self.__g = ldict['g']
            except:
                pass
            try:
                self.__r = ldict['r']
            except:
                pass
            try:
                self.__b = ldict['b']
            except:
                pass
            print(self.__b, self.__r, self.__g)
            if self.__cmd_poz == 10:
                self.__cmd_poz = 2
            else:
                self.__cmd_poz = self.__cmd_poz + 1
        self.__body_color = (red, green, blue)

    def change_dir(self):
        if self.__dir == self.__next_dir:
            return
        if (self.__dir[0] * self.__next_dir[0] != 0) | (self.__dir[1] * self.__next_dir[1] != 0):
            return
        self.__dir = self.__next_dir

    def move(self):
        for body in self.__body:
            body.last_poz = body.poz
        self.__body[0].poz = (self.__body[0].poz[0] + self.__dir[0]*self.__speed,
                              self.__body[0].poz[1] + self.__dir[1]*self.__speed)
        for i in range(1, len(self.__body)):
            self.__body[i].poz = self.__body[i-1].last_poz
        if (self.__body[0].poz[0] % self.__dimension == 0) & (self.__body[0].poz[1] % self.__dimension == 0):
            self.change_dir()
        if self.__fed > 0:
            self.__fed -= 1
            print(self.__body_color)
            self.__body.append(Body(self.__body[len(self.__body) - 1].last_poz, self.__body_color, self.__dimension))
            self.new_color()

    def check_collision(self):
        for i in range(1, len(self.__body)):
            if self.__body[0].poz == self.__body[i].poz:
                return True
        return False
