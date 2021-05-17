import sys

#TODO
# c: is a symbol
def is_char(c):
    return True if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9') else False

def is_operation(c):
    return True if c == '|' or c == '+' or c == '*' else False 

# regex_list: list of symbols
def is_valid(regex_list):
    # symbol validation
    for symbol in regex_list:
        if not is_char(symbol) and not is_operation(symbol) and symbol != '(' and symbol != ')':
            print("Not Valid Input: unvalid symbol", symbol)
            return False
    
    # two consecutive operations 
    for i in range(len(regex_list)-1):
        if is_operation(regex_list[i]) and is_operation(regex_list[i+1]):
            print("Not Valid Input: Two consecutive operations", regex_list[i], regex_list[i+1])
            return False
    
    # or with 1 operand
    if regex_list[0] == '|' or regex_list[0] == '+' or regex_list[-1] == '|' or regex_list[-1] == '+' :
        print("Not Valid Input: OR operation with 1 operand")
        return False
    
    # parentheses  balancing
    stack = 0
    for symbol in regex_list:
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
            regex_list[i:i+2] = regex_list[i] #TODO
        else:
            i += 1
    
    # solve Concatenation
    i = 0
    while(i < len(regex_list)-1):
        if  is_char(regex_list[i]) and is_char(regex_list[i+1]):
            regex_list[i:i+2] = regex_list[i] #TODO
        else:
            i += 1
    
    # solve ORing
    i = 0
    while(i < len(regex_list)-2):
        if  is_char(regex_list[i]) and (regex_list[i+1] == '|' or regex_list[i+1] == '+') and \
            is_char(regex_list[i+2]):
            regex_list[i:i+3] = regex_list[i] #TODO
        else:
            i += 1

    return regex_list

# regex_list: list of symbols
# start: the start index of the list
def solver(regex_list, start = 0):
    end = start
    while(end < len(regex_list) and regex_list[end] != ')'):
        if regex_list[end] == '(':
            solver(regex_list, end+1)
        else:
            end += 1
    
    # solving the part that doesn't contain parentheses
    if regex_list[start] == '(': # this is a special case
        output = base_solver(regex_list[start+1:end])
    else:
        output = base_solver(regex_list[start:end])

    # replacing the solved part with the solution
    regex_list[start:end] = output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Unvalid number of arguments")
    else:
        regex = sys.argv[1]
        regex_list = [str(symbol) for symbol in regex]
        if is_valid(regex_list):
            solver(regex_list)
            print(regex_list)