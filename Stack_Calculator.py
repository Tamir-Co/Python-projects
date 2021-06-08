def StackCalc(inp):
    """
    This function gets a string (e.g. "9 4 2 + 7 -") and does the calculations
    as if it was a stack calculater (for the ex above: 7-(2+4)=1.)
    This function returns the top of the stack (for the ex above: 1 because [9 1]).
    """
    inp = inp.split()
    leng = len(inp)
    st = [' '] * leng
    top = 0
    
    print("input:", inp)
    print("top:", top, ", st:", st)

    if leng == 0: return 0
    
    for c in inp:
        if c in ['+', '-', '*', '/']:
            st[top-2] = str(eval(st[top-1] + c + st[top-2]))
            st[top-1] = ' '
            top -= 1
        else:
            st[top] = c
            top += 1
        print("top:", top, ", st:", st)
    
    return float(st[top-1])

def Tests_StackCalc():  # Tests for the function StackCalc
    test1 = "5 6 - 7 +" # 7+(6-5) = 8
    print("result:", StackCalc(test1), "\n")
    
    test2 = "3 2 4 5 6 - 7 +" # 7+(6-5) = 8  # numbers 3,2,4 are ignored
    print("result:", StackCalc(test2), "\n")
    
    test3 = "2 3 + 7 - 1 -" # 1-(7-(3+2)) = -1
    print("result:", StackCalc(test3), "\n")
    
    test4 = "2 3 + 7 - 1 - -1 * 4 * 2 /" # 2/(4*(-1*(1-(7-(3+2))))) = 0.5
    print("result:", StackCalc(test4), "\n")
    
