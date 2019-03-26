def chooseAlg():

    print("Please, choose which search method do you wish to use:")
    print("A) Breadth-first search.")
    print("B) Depth-first search.")
    print("C) Progressive deepening.")
    print("D) Uniform cost search.")
    print("E) Greedy.")
    print("F) A*.")

    ans=input()
    
    if ans == "A" or ans == "a":
        return 'A'
    elif ans == "B" or ans == "b":
        return 'B'
    elif ans == "C" or ans == "c":
        return 'C'
    elif ans == "D" or ans == "d":
        return 'D'
    elif ans == "E" or ans == "e":
        return 'E'
    elif ans == "F" or ans == "f":
        return 'F'
    else:
        chooseAlg()