class Jar:

    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError
        else:
            self.cookies = []                       # Initialising an array of characters to store the cookies

    def __str__(self):
        cookie = ''
        for i in range(len(self.cookies)):          # Printing a cookie for each cookie in 'cookies'
            cookie += '\U0001F36A'
        return cookie

    def deposit(self, n):                           # Check if there is enough room to add n cookies in the jar
        if (len(self.cookies) + n) > self.capacity:
            raise ValueError
        else:
            while n > 0:
                n -= 1
                self.cookies.append('\U0001F36A')

    def withdraw(self, n):                          # Check if there is enough cookies to remove
        if (len(self.cookies) - n) < 0:
            raise ValueError
        else:
            while n > 0:
                n -= 1
                self.cookies.remove('\U0001F36A')   

    @property
    def capacity(self):
        return 12

    @property
    def size(self):
        return len(self.cookies)

def main():
    jar = Jar()
    print(str(jar.capacity))
    print(str(jar))

    jar.deposit(8)
    print(str(jar))

    jar.withdraw(5)
    print(str(jar))

main()