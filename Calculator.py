import re

# Priority list of operators
operators = ['^', '/', '*', '-', '+']

# Changes user input to match calculation properties for...
def purify_input(string):
    """
    Changes user input to match calculation properties. In detail it removes 
    spaces, changes all brackets to parentheses, changes float presentation 
    from ',' to '.', strips unnecessary '+' at start of sequences.
    
    
    Args:
        string (str): Raw user input.
        
    Returns:
        str: Purified input with no spaces, parentheses and '.' only, without
        starting '+' on sequnce.
    """
    # Checks for empty string
    if not string:
        return string
    # Strips spaces
    string = string.replace(" ", '')
    # Replaces all type of brackets with appropriate parentheses
    string = string.replace('[', '(')
    string = string.replace('{', '(')
    string = string.replace(']', ')')
    string = string.replace('}', ')')
    # Replaces commas ',' with periods '.' for float points
    string = string.replace(',', '.')
    # Strips unnecessary starting '+'
    if string[0] == '+':
        string = string[1:]
    return string


def check_input(string):
    """
    Checks if input follows basic rules of mathematical expressions. 
    Checks for 0 length input, non permitted characters/symbols, operators,
    parentheses and float points being used correctly, division by 0.
    
    
    Args:
        string (str): String that has been purified (see purify_input() for 
        more info as to what that entails).
    
    Returns:
        boolean: True if no problems were detected.
    """
    # Enter pressed with nothing entered
    if len(string) == 0:
        print('Please, enter a mathematical expression')
        return False
    # String contains something other than digits and permitted symbols
    # Note: []{} are already exchanged with () when this check is done
    if re.search('[^0-9+\-*/^().]', string):
        print("Please, enter a valid mathematical expression using only 0-9, +, -, *, ^, /, (, ) and , . .")
        return False
    # String contains two operators in succession
    if re.search('[+\-*/^.]{2}', string):
        print("There's an issue with your operators. Please check your sequence and try again.")
        return False
    # Parentheses close immdediately after opening
    if re.search('[(][)]', string):
        print('Your parentheses do not contain a number or unary operator. Please check your sequence and try again.')
        return False
    # Parentheses close without operator afterwards
    if re.search('[)][^+\-*/^)(]', string):
        print("Your parentheses close and are not followed by an operator.\nIf you wanted to multiply, please specify with operator '*'.\nPlease check your sequence and try again.")
        return False
    # Parentheses open without operator before
    if re.search('[^+\-*/^())][(]', string):
        print("Your parentheses open and are not preceded by an operator.\nIf you wanted to multiply, please specify with operator '*'.\nPlease check your sequence and try again.")
        return False
    
    digit_flag = False
    float_point_flag = False
    # Runs string in reverse
    for char in string[-1::-1]:
        if re.search('\d',char):
            digit_flag = True
        if char in '+-^*/.':
            if digit_flag:
                # Checks if there's a double float point, flag resets on operator found
                if char in '.':
                    if float_point_flag:
                        print("There's multiple float points on a single number. Please check your sequence and try again.")
                        return False
                    float_point_flag = True
                else:
                    float_point_flag = False
                # To allow sequential +- like 5-(-(-5)) and 5/(-5)
                if char in '+-':
                    continue
                digit_flag = False
            else:
                print("There's a stray operator with no second part. Please check your sequence and try again.")
                return False
    # String starts with / * ^ , or .
    if string[0] in '/*^.':
        print("Your sequence starts with operator '", string[0], "'. Please check your sequence and try again.")
        return False
    if check_zero_division(string):
        print('Division by 0 not allowed. Please check your sequence and try again.')
        return False
    # Checks if there are parentheses
    opening_match = re.findall('[(]', string)
    closing_match = re.findall('[)]', string)
    # Checks if closing and opening parentheses match
    if (opening_match or closing_match) and len(opening_match) != len(closing_match):
        print("There's an issue with your parentheses. Please check your sequence and try again.")
        return False
    if not check_parentheses_sequence(string):
        return False
    return True


def check_parentheses_sequence(my_string):
    """
    Helper function for check_input(). Checks if parentheses close correctly 
    after opening.
    
    
    Args:
        my_string (str): Purified user input (see purify_input() for more info
        as to what that entails).
        
    Returns:
        boolean: True if parentheses close correctly.
    """
    current_open_parentheses = 0
    for char in my_string:
        if char == ')':
            if current_open_parentheses == 0:            
                print('Parentheses close without ever opening. Please check your sequence and try again.')
                return False
            current_open_parentheses -= 1
        if char == '(':
            current_open_parentheses += 1
    if current_open_parentheses == 0:
        return True
    # This means that parentheses are open
    else:
        print('Parentheses open without ever closing. Please check your sequence and try again.')
        return False


def find_innermost_parentheses_sequence(initial_list):
    """
    Finds start and end of deepest parentheses.
    
    
    Args:
        initial_list (list): List of entire mathematical expression.
    
    Returns:
        list: 
            [0] (int) = index after deepest '('
            [1] (int) = index before deepest ')'.
    """
    current_depth = 0
    max_depth = 0
    for i in range(0, len(initial_list)):
        if initial_list[i] == '(':
            current_depth += 1
            start_index = i + 1
            # New index if depth is bigger (or same for the case of same depth parentheses)
            if max_depth <= current_depth:
                max_depth = current_depth
                max_depth_open = start_index
        if initial_list[i] == ')':
            end_index = i - 1
            # If this is the end of the deepest parentheses found
            if max_depth == current_depth:
                max_depth_close = end_index
            current_depth -= 1
    return [max_depth_open, max_depth_close]


def check_zero_division(string):
    """
    Helper function for check_input(). Checks initial input string for a 
    division by zero, raw like 6/0 not 6/(3-3).
    
    
    Args:
        string (str): Purified user input (see purify_input() for more info as
        to what that entails).
        
    Returns:
        boolean: True if zero division has been detected.
    """
    flag = False
    # Checks if there are divisions to be checked
    while '/' in string:
        
        start_index = string.index('/')+1
        # If there's a parentheses, result is checked later by calculate
        if string[start_index] == '(':
            # Checks the rest of the string for raw division by 0
            string = string[start_index:]
            continue
        
        # This exists in case there's no operator after the division
        end_index = len(string)-1
        
        for i in range(start_index, len(string)):
            if string[i] in '+-/*^)':
                # String slice ends before new operator appears
                end_index = i-1
                break

        # This works for slices that include only one character
        if start_index == end_index:
            if float(string[start_index]) == 0.0:
                flag = True
                return flag
            else:
                # If the checked part was a single char, string gets reduced
                string = string[end_index:]
                continue
        if float(string[start_index:end_index+1]) == 0.0:
            flag = True
            return flag
        # Reduces string by the part that has already been checked
        string = string[end_index:]
    return flag




def update_list(my_list, result, start_index, end_index):
    """
    Modifies list to reflect result on position where two-part operation was.
    
    
    Args:
        my_list (list): List of entire mathematical expression.
        result (int/float): Result of two-part operation calculated.
        start_index (int): Index where two-part operation begins and needs to 
        be popped.
        end_index (int): Index where two-part operation ends. End index needs
        to be popped as well.
        
    Returns:
        list (str): List of mathematical expression where distance between start
        and end index have been popped and replaced with result.
    """
    # Removes parts of two-part calculation 
    # Starts from the end because indexes after pop index will change...
    for index in range(end_index, start_index-1, -1):
        my_list.pop(index)
    # ...and inserts result
    my_list.insert(start_index, str(result))
    return my_list



def sequence_to_string(sequence_list, start, end):
    """
    Checks a specified part of mathematical expression, e.g. start-end of 
    parentheses for two-part operations, returns parts that need to be popped 
    and result of operation.
    
    
    Args:
        sequence_list (list): List of entire mathematical expression.
        start (int): Index where the search for two-part operations begins.
        end (int): Index where the search for two-part operations ends.
        
    Returns:
        list: A list of 3 elements:
            [0] (str) = Two-part operation (without parentheses).
            [1] (int) = Start of two-part operation (may be opening parentheses)
            [2] (int) = end of two-part operation (may be closing parentheses)
            
    """
    flag_operator_found = False
    
    # Runs through operators
    for operator_0 in operators:
        # Checks if current operator is in list that is being checked
        if operator_0 in sequence_list[start:end + 1]:
            # Checks if first part contains unary - operator
            if '-' == sequence_list[start] or '+' == sequence_list[start]:
                # Converts to unary
                sequence_list[start] = sequence_list[start] + sequence_list[start+1]
                sequence_list.pop(start+1)
                # End changes as the list becomes smaller
                end -= 1
                
                # This makes sure that calculation doesn't proceed if
                # now there's no longer a '-'in sequence_list
                if operator_0 not in sequence_list[start:end+1]:
                    # Continue to find next operation to be calculated
                    continue
            
            # Keeps location of operator, adds start in case it's a slice
            operator_index  = sequence_list[start:end+1].index(operator_0) + start
            
            start_index = start
            # Starting from operator_index, moving 'backwards' to find 
            # previous operator, hence the start of two-part calculation
            for i in range(operator_index-1,start-1, -1):
                for operator_1 in operators:
                    # If we reached the first sequence index, we stop 
                    # despite not finding an operator
                    if i == start:
                        start_index = i
                        flag_operator_found = True
                        break
                    # If we found an operator on this index, two-part 
                    # calculation starts from next index
                    if sequence_list[i] == operator_1:
                        start_index = i+1
                        flag_operator_found = True
                        break
                # Stops trying to find start of sequence
                if flag_operator_found == True:
                    break
            flag_operator_found = False
            
            # Maximum end_index is end of sequence
            end_index = end
            # Runs through sequence starting from operator moving forwards
            for i in range(operator_index+1, end):
                for operator_1 in operators:
                    if sequence_list[i] == operator_1:
                        # If operator on i index, two-part calculation ends
                        # on previous index
                        end_index = i-1
                        flag_operator_found = True
                        break
                if flag_operator_found == True:
                    break
            input_string = ''
            # Creates the input string based on start/end index for 
            # two-part calculation
            input_string = input_string.join(sequence_list[start_index:end_index+1])
            if sequence_list[start_index-1] == '(' and sequence_list[end_index+1] == ')':
                start_index -= 1
                end_index +=1
            return [input_string, start_index, end_index]
        
    # This exists for the case where the is no operator in sequence 
    # e.g. 5+(5) inside parentheses
    if sequence_list[start-1] == '(' and sequence_list[end+1] == ')':
        # To correctly return multi-digit numbers
        output_string = ''
        output_string = output_string.join(sequence_list[start:end+1])
        return [output_string, start-1,end+1]


def calculate(string):
    """
    Checks what operation needs to be done and returns result.
    
    
    Args:
        string (str): Two-part operation, without parentheses.
        
    Returns:
        int/float/str: Returns result of two-part operation, will be a float only 
        if the result is a float. Returns as str "infinity" if a division by 0
        came up.
    """
    # Initially works with floats to cover all scenarios
    if '^' in string:
        parts_to_calculate = string.split('^')
        result = pow(float(parts_to_calculate[0]), float(parts_to_calculate[1]))
    elif '/' in string:
        parts_to_calculate = string.split('/')
        if float(parts_to_calculate[1]) == 0.0:
            # This is the case of 6/(3-3) that is not handled by check_zero_division
            return 'infinity'
        result = float(parts_to_calculate[0]) / float(parts_to_calculate[1])
    elif '*' in string:
        parts_to_calculate = string.split('*')
        result = float(parts_to_calculate[0]) * float(parts_to_calculate[1])
    # string[1:] makes sure to ignore unary operators 
    # and find actual two-part operation
    elif '+' in string[1:]:
        # Check for unary operator + for first part
        if string[0] == '+':
            # Try to split the rest in case there is also two-part operator
            parts_to_calculate = string[1:].split('+')
            # Makes it unary
            parts_to_calculate[0] = '+' + parts_to_calculate[0]
        # If there isn't an unary operator for first part, split into two parts
        else:
            parts_to_calculate = string.split('+')
        # If the operator found was just the string[0] unary operator
        if len(parts_to_calculate) == 1:
            result = float(parts_to_calculate[0])
        # If whether there was or not unary operator for first part, 
        # there is also a 2nd part
        else:
            result = float(parts_to_calculate[0]) + float(parts_to_calculate[1])
    # Ignores unary operation via string[1:]
    elif '-' in string[1:]:
        # Mandatory for operations that result in first part being negative 
        # also unary 
        if string[0] == '-':
            parts_to_calculate = string[1:].split('-')
            parts_to_calculate[0] = '-' + parts_to_calculate[0]
        else:
            parts_to_calculate = string.split('-')
        if len(parts_to_calculate) == 1:
            result = float(parts_to_calculate[0])
        else:
            result = float(parts_to_calculate[0]) - float(parts_to_calculate[1])
    # Sequence doesn't contain an operator, e.g. 5+(5)
    else:
        result = float(string)
        
    # If result is non-decimal, returns int result 
    # to avoid unnecessary, innacurate floats
    if result % 1 == 0:
        return int(result)
    else:
        return result
     
# Self explainable termination that takes ExIt, EXIT etc
def check_termination(string):
    if string.lower() == 'exit':
        print('Program will now exit...')
        return True


def check_if_calculation_done(my_list):
    """
    Checks if there are operators in list to signal end of calculation. Unary
    operators don't trigger a continuation of calculation.
    
    
    Args:
        my_list (list): List of entire mathematical expression to be examined.
        
    Returns:
        boolean: True if calculation is done.
    """
    flag = True
    for operator_0 in operators:
        if operator_0 in my_list[1:]:
            flag = False
    return flag


def check_signs(my_list):
    """
    Checks if parentheses have resulted in a double sign calculation, an two-part
    operator and a unary operator from a result:
    e.g. 2-(3-4) = 2--1 = 2 + 1 = 3
    
    
    Args:
        my_list (list): List of entire mathematical expression to be examined.
        
    Returns:
        list: Mathematical expression without double operators.
    """
    for i in range(0,len(my_list)-1):
        # Because result is on unary operator, we need to check index[0] of string
        if my_list[i] in '+-' and my_list[i+1][0] in '+-':
            # If they're the same, result is positive, either ++ or --
            if my_list[i] == my_list[i+1][0]:
                my_list[i] = '+'
                my_list[i+1] = my_list[i+1][1:]
            # If they're different, result is negative, either -+ or +-
            else:
                my_list[i] = '-'
                my_list[i+1] = my_list[i+1][1:]
    return my_list
    


def refine_result(my_list):
    """
    Function mainly for handling returning no-operator strings e.g 53 = 53.
    Without it, result would be a list.
    
    
    Args: 
        my_list (list): List of entire mathematical expression.
        
    Returns:
        str: Joined parts of given list.
    """
    string = ''
    for part in my_list:
        string += part
    return string
            

def is_result_infinity(result):
    """
    Checks if the result was an "infinity" result of division, a division by 0.
    
    
    Args:
        result (int/float/str): The result of calculate().
        
    Returns:
        boolean: True if division by 0 has been detected.
    """
    flag = False
    if result == 'infinity':
        print('Calculations result in division by 0, which is notallowed.\nPlease check your sequence and try again.')
        flag = True
    return flag


def solve_parentheses(my_list, zero_div_flag):
    """
    Solves parentheses in sequence by altering the list.
    
    
    Args:
        my_list (list): List of entire mathematical expression.
        zero_div_flag (boolean): Flag detecting division by 0.
        
    Returns:
        boolean: Flag detecting division by 0, True if there is one.
    """
    flag_parentheses_present = '(' in my_list
    while flag_parentheses_present:
    
        sub_part = find_innermost_parentheses_sequence(my_list)
        info = sequence_to_string(my_list, sub_part[0], sub_part[1])
        result = calculate(info[0])
        zero_div_flag = is_result_infinity(result)
        if zero_div_flag:
            break
        my_list = update_list(my_list, result, info[1], info[2])
        my_list = check_signs(my_list)
        flag_parentheses_present = '(' in my_list
    return zero_div_flag


def solve_sequence(my_list, zero_div_flag):
    """
    Solves sequence that is free of parentheses by altering the list.
    
    
    Args:
        my_list (list): List of entire mathematical expression.
        zero_div_flag (boolean): Flag detecting division by 0.
        
    Returns:
        boolean: Flag detecting division by 0, True if there is one.
    """
    
    flag_done_calculating = check_if_calculation_done(my_list)
    
    while not flag_done_calculating and not zero_div_flag:
            
        # info contains [string_to_calculate, start_index, end_index]
        info = sequence_to_string(my_list, 0, (len(my_list)-1))
        result = calculate(info[0])
        my_list = update_list(my_list, result, info[1], info[2])
        zero_div_flag = is_result_infinity(result)
        if zero_div_flag:
            break
        flag_done_calculating = check_if_calculation_done(my_list)
    
    return zero_div_flag

while __name__ == '__main__':
    user_input = input("Give me a mathematical expression to solve or 'exit' to terminate: \n")
    
    # Check for exit
    if check_termination(user_input):
        break
    
    # Purify input of spaces, [] etc
    user_input = purify_input(user_input)
    
    # Creates a list with input for better handling
    input_list = list(user_input)
    
    # Checks list for issues
    if not check_input(user_input):
        continue
    
    # Creates a flag for division by zero
    zero_div_flag = False
    
    # Solves parentheses sequences, gets zero div flag
    zero_div_flag = solve_parentheses(input_list, zero_div_flag)
    
    # Solves rest of sequences, gets zero div flag
    zero_div_flag = solve_sequence(input_list, zero_div_flag)
    
    # Checks zero div flag
    if zero_div_flag:
        continue
    
    # Gets refined result, mainly for single number cases
    final_result = refine_result(input_list)
    print(user_input,'=', final_result)