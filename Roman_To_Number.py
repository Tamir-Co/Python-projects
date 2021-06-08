def RomanToNumber(str_roman):
    str_roman = str_roman.upper()
    letters = {'I' : 1, 'V' : 5, 'X' : 10, 'L' : 50, 'C' : 100, 'D' : 500, 'M' : 1000}
    value = 0
    i = 0
    length = len(str_roman)
    
    while i < length:
        if (i + 1 < length):
            if (letters.get(str_roman[i]) < letters.get(str_roman[i+1])):
                value = value + (letters.get(str_roman[i+1]) - letters.get(str_roman[i]))
                print(str_roman[i] + str_roman[i+1], letters.get(str_roman[i+1]) - letters.get(str_roman[i]))
                i += 1
            else:
                print(str_roman[i], letters.get(str_roman[i]))
                value = value + letters.get(str_roman[i])
        else:
            print(str_roman[i], letters.get(str_roman[i]))
            value = value + letters.get(str_roman[i])
        i += 1

    return value
