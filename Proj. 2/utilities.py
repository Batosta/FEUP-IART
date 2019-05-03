def inputRing():
        while True:
            ring = input("Select position (outer/middle/inner):  ")

            if ring in ['outer','middle','inner']:
                return ring
            else:
                print("Insert a valid ring (outer/middle/inner)\n")

def inputNumber():
    while True:
        pos = input("Select position (0-7):  ")
        try:
            number = int(pos)
        except :
            print("Type a number (0-7)\n")
            continue
        if number >= 0 and number <=7:
            return number
        else:
            print("Insert a valid number (0-7)\n")


def printMap(intersections):
        print(intersections[0].getValue(), end='-------')
        print(intersections[1].getValue(), end='-------')
        print(intersections[2].getValue())

        print('|       |       |')

        print('|  ', end='')
        print(intersections[8].getValue(), end='----')
        print(intersections[9].getValue(), end='----')
        print(intersections[10].getValue(), end='  |\n')
        
        print('|  |    |    |  |')

        print('|  |  ', end='')
        print(intersections[16].getValue(), end='-')
        print(intersections[17].getValue(), end='-')
        print(intersections[18].getValue(), end='  |  |\n')
        
        print('|  |  |   |  |  |')

        print(intersections[7].getValue(), end='--')
        print(intersections[15].getValue(), end='--')
        print(intersections[23].getValue(), end='   ')
        print(intersections[19].getValue(), end='--')
        print(intersections[11].getValue(), end='--')
        print(intersections[3].getValue())
        
        print('|  |  |   |  |  |')

        print('|  |  ', end='')
        print(intersections[22].getValue(), end='-')
        print(intersections[21].getValue(), end='-')
        print(intersections[20].getValue(), end='  |  |\n')

        print('|  |    |    |  |')

        print('|  ', end='')
        print(intersections[14].getValue(), end='----')
        print(intersections[13].getValue(), end='----')
        print(intersections[12].getValue(), end='  |\n')

        print('|       |       |')

        print(intersections[6].getValue(), end='-------')
        print(intersections[5].getValue(), end='-------')
        print(intersections[4].getValue())
