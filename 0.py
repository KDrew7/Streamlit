

def main():
    numList =[]
    for x in range(0,44):
        numList.append(input("enter a number"))
    #numList = [2,4,7,3,2,7,8435,34,123,654,5686,324264,467,23,312,546,635,23312,65476,546,24213,123,343,345,5345]
    evenList = []

    for x in numList:
        if (x%2 == 0):
            evenList.append(x)

    evenListString = ""
    for x in evenList:
        evenListString = evenListString + str(x) + ", "
    print("even numbers are " + evenListString + "and " + str(evenList[-1]))
    #return evenList


main()