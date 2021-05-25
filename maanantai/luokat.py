class Animal():
    name = "Apu apustaja"

    def sound(self):
        return "Siip huup"

class Sanmako(Animal):
    def sound(self):
        return "Ilon moista"

def main():
    sanmako = Sanmako()
    print(sanmako.sound())

if __name__ == "__main__":
    main()
