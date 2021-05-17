import sys
from Block import Block

# c: is a symbol
def is_char(c):
    return type(c) == Block or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9')

def is_operation(c):
    return c == '|' or c == '+' or c == '*' 

# regex: string of symbols
def is_valid(regex):
    # symbol validation
    for symbol in regex:
        if not is_char(symbol) and not is_operation(symbol) and symbol != '(' and symbol != ')':
            print("Not Valid Input: unvalid symbol", symbol)
            return False
    
    # two consecutive operations 
    for i in range(len(regex)-1):
        if (regex[i] == '*' and regex[i+1] == '*') or \
            ((regex[i] == '|' or regex[i] == '+') and \
                (regex[i+1] == '|' or regex[i+1] == '+')):
            print("Not Valid Input: Two consecutive operations", regex[i], regex[i+1])
            return False
    
    # or with 1 operand
    if regex[0] == '|' or regex[0] == '+' or regex[-1] == '|' or regex[-1] == '+' :
        print("Not Valid Input: OR operation with 1 operand")
        return False
    
    # parentheses  balancing
    stack = 0
    for symbol in regex:
        if symbol == '(':
            stack += 1
        elif symbol == ')':
            stack -= 1
            if stack < 0:
                print("Not Valid Input: parentheses are unbalanced")
                return False
    if stack != 0:
        print("Not Valid Input: parentheses  are unbalanced")
        return False
    
    return True

# regex_list: list of symbols
def base_solver(regex_list):
    # solve Repetition
    i = 0
    while(i < len(regex_list)-1):
        if regex_list[i+1] == '*':
            regex_list[i:i+2] = [Block(a = regex_list[i], operator = '*')]
        else:
            i += 1
    
    # solve Concatenation
    i = 0
    while(i < len(regex_list)-1):
        if  is_char(regex_list[i]) and is_char(regex_list[i+1]):
            regex_list[i:i+2] = [Block(a = regex_list[i], b = regex_list[i+1], operator = '.')]
        else:
            i += 1
    
    # solve ORing
    i = 0
    while(i < len(regex_list)-2):
        if  is_char(regex_list[i]) and (regex_list[i+1] == '|' or regex_list[i+1] == '+') and \
            is_char(regex_list[i+2]):
            regex_list[i:i+3] = [Block(a = regex_list[i], b = regex_list[i+2], operator = '+')]
        else:
            i += 1

    return regex_list

# regex_list: list of symbols
# start: the start index of the list
def solver_helper(regex_list, start = 0):
    end = start
    while(end < len(regex_list) and regex_list[end] != ')'):
        if regex_list[end] == '(':
            solver_helper(regex_list, end+1)
        end += 1
    # solving the part that doesn't contain parentheses
    # and # replacing the solved part with the solution
    if regex_list[start] == '(': # this is a special case
        output = base_solver(regex_list[start+1:end])
        regex_list[start:end+1] = output
    else:
        output = base_solver(regex_list[start:end])
        regex_list[start:end] = output

def solver(regex_list):
    i = 0
    while(i < len(regex_list)):
        if regex_list[i] == '(':
            solver_helper(regex_list, i)
        i +=1
    base_solver(regex_list)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Unvalid number of arguments")
    else:
        regex = sys.argv[1]
        if is_valid(regex):
            regex_list = [Block(symbol) if is_char(symbol) else str(symbol) for symbol in regex]
            solver(regex_list)
            print("_____________________________________________")
            print(regex_list[0].json()[1])