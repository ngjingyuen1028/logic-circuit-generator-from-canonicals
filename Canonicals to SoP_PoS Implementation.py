# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:58:28 2025

@author: Jing Yuen Ng
email : jngg0200@student.monash.edu
Title : Canonicals to 2 Level Boolean Expressions
"""
import ast
import itertools
import schemdraw
import schemdraw.logic as logic
from schemdraw.parsing import logicparse


def binary_to_int(binary_str):
    value = 0
    width = len(binary_str)
    for i in range(width):
        if binary_str[i] == '1':
            value += 2**(width - i - 1)
    return value


def num_to_binary(num_list):   
    
    #convert list of decimals to binary list with sorted number of 1's
    #eg : [0,2,3,4,7,8,9] to [['0000'], ['0010', '0100', '1000'], ['0011', '1001'], ['0111']]

    binary_list = []   #empty list to hold the numbers converted into binarys
    num_list.sort()    #sort the inputs 

     #to find out minimum amount of bits required to represent the binary number
    max_num = max(num_list)
    n = 0
    while 2**n <= max_num:   
        n +=1
        
    
    for number in num_list:
        binary_str = bin(number)[2:].zfill(n)     #to convert the numbers into binary
        binary_list.append(binary_str)

    #to group the binary into different list based on the number of 1's in the number
    nested_list = []
    for i in range(n+1):
        temp_list = []
        for binary_str in binary_list:
            count_ones = binary_str.count('1')    
            if i == count_ones:
                temp_list.append(binary_str)
        
        if temp_list != []:
            nested_list.append(temp_list)
    
    return nested_list,n


def implicants_cleaning_func(list1, list2, digit_num):  
    #this function is to clean 2 list of numbers that differs by one bit
    
    
    #cleaned_list represents the number that can be joined into bigger implicants
    #answer represent number needed to be represented in a boolean expression
    cleaned_list = []    
    answer = []
    number_used = []
    
    #compare each number in list1 against each number in list2
    for number1 in list1:
        for number2 in list2:
            different_bits = []
            for i in range(digit_num):
                if number1[i] == number2[i]:
                    continue
                else:
                    different_bits.append(i)
                    
            if len(different_bits) == 1:    #if the 2 numbers differ by only 1 bits
                number1_temp_list = list(number1)
                number1_temp_list[different_bits[0]] = 'x'    #change that particular bits to x
                number = ''.join(number1_temp_list)
                
                if number not in cleaned_list:
                    cleaned_list.append(number)
                if number1 not in number_used:
                    number_used.append(number1)
                if number2 not in number_used:
                    number_used.append(number2)
                    
    #if the number in either list is not used, then it has to be expressed in Boolean
    for number1 in list1:
        if number1 not in number_used:
            answer.append(number1)
    for number2 in list2:
        if number2 not in number_used:
            answer.append(number2)
            
    return cleaned_list, answer



def canonical_to_prime_implicants(canonicals):
    #this function combines the previous 2 functions to convert a canonical expression into its prime implicants
    
    master_list,num_digit = num_to_binary(canonicals)   #obtain the sorted binary numbers and their width
    group_num = len(master_list)

    prime_implicants = []    #empty list to hold the prime implicants
    
    if group_num == 1:
        prime_implicants.extend(master_list[0])    #if there's only one group of implicants then they are the prime implicant
    
    while group_num > 1:
        output_holding_list = []   #hold the potential prime implicants
        next_stage_list = []      #hold the implicants that will enter the next round of implicants cleaning
        for i in range(group_num - 1):
            temp_list, temp_implicant = implicants_cleaning_func(master_list[i],master_list[i+1],num_digit)
            
            if temp_list != []:
                next_stage_list.append(temp_list)
                
            if temp_implicant != []: 
                #if the prime implicants originate from the edge group, then it only has to appear once to confirm its place as a prime implicants
                if i == 0:
                    for number in temp_implicant:
                        if number in master_list[i]:
                            prime_implicants.append(number)
                if i == (group_num - 2):
                    for number in temp_implicant:
                        if number in master_list[i+1]:
                            prime_implicants.append(number)
                
                output_holding_list.extend(temp_implicant)
        
        #for number groups that are not at the edge groups, the number has to appear twice to validate its place as a prime implicants
        for output in output_holding_list:
            if output_holding_list.count(output) == 2 and output not in prime_implicants:
                prime_implicants.append(output)
              
        master_list = next_stage_list
        group_num = len(master_list)
        
        if group_num ==1:
            prime_implicants.extend(master_list[0])
            
    return prime_implicants
        

def min_cover_set(groups,targets):
    
    #to calculate the minimum amount of prime implicants needed to cover all the leftover minterms
    #after the essential prime implicants are determined
    
    targets = set(targets)
    
    #brute force through all the potential combinations of remaining prime implicants
    #to determine the smallest possible combinations to cover all the remaining minterms
    
    for i in range(1,len(groups) + 1):
        for combo in itertools.combinations(groups,i):
            subset = set().union(*map(set,combo))
            if targets.issubset(subset):
                return list(combo)


def minimization(terms,doncares):
    canonicals = terms + doncares
    prime_implicants = canonical_to_prime_implicants(canonicals)

    decimal_list = []

    essential_prime_implicants = []
    minimized_prime_implicants = []
    
    #to convert all the prime implicants from binary strings to decimal for easier computation
    #eg : 0001 to 1 and x000 to [0,8]
    #will be represented by decimal lists
    
    for binary in prime_implicants:
        if 'x' in binary:
            seats = binary.count('x')    #number of x in the binary strings
            choices = [0,1]
            
            #to calculate all the potential combinations of arrangement
            #eg : if 3 x's are present, the potential arrangement are 
            # [000,001,010,011,100,101,110,111]
            possible_arrangement = list(itertools.product(choices,repeat = seats))
            result_string = []
            
            #change the combinations from a list of tuples to a list of strings
            for combinations in possible_arrangement:
                string = ''.join(map(str,combinations))
                result_string.append(string)
                
            holding_list = []   #to hold the possible binary represented by the prime implicants
            
            #to figure out the index of 'x' in the binary strings
            x_index = []
            for index,digit in enumerate(binary):
                if digit == 'x':
                    x_index.append(index)
                    
                    
            #implement all the possible arrangement onto the binary strings and calculate its decimal values
            #eg : 'x00x' to ['0000','1000']
            
            for combinations_string in result_string:
                temp = list(binary)
                count = 0
                while count < seats:
                    temp[x_index[count]] = combinations_string[count]
                    count += 1
                temp = ''.join(temp)
                value = binary_to_int(temp)
                holding_list.append(value)
            
            decimal_list.append(holding_list)               
        
        else:
            decimal = binary_to_int(binary)
            decimal_list.append(decimal)


    #find out the essential prime implicants 
    indexes = []
    for term in terms:
        index_record = []
        for index,item in enumerate(decimal_list):
            if isinstance(item,int):
                if term == item:
                    index_record.append(index)
            elif isinstance(item,list):
                if term in item:
                    index_record.append(index)
        
        if len(index_record) == 1:
            if prime_implicants[index_record[0]] not in essential_prime_implicants:
                essential_prime_implicants.append(prime_implicants[index_record[0]])
                indexes.append(index_record[0])



    #removing the terms that has been covered by the essential prime implicants 
    to_be_removed = []
    for index in indexes:
        if isinstance(decimal_list[index],int):
            to_be_removed.append(decimal_list[index])
        elif isinstance(decimal_list[index],list):
            to_be_removed.extend(decimal_list[index])

    terms = [x for x in terms if x not in to_be_removed]
    
    #if all the minterms are covered by the essential prime implicants, then the calculation has finished
    if terms == []:
        return essential_prime_implicants
    

    #to remove the essential prime implicants from any further calculations
    #and remove the decimals from the decimal lists from any further calculations
    for index,implicants in enumerate(prime_implicants):
        if implicants in essential_prime_implicants:
            prime_implicants.remove(implicants)
            decimal_list.pop(index)
            
    minimized_prime_implicants.extend(essential_prime_implicants)
    
    remaining_combo = min_cover_set(decimal_list,terms)
    
   #to include the answers calculated from the brute forcing method into the final answer 
    for item in remaining_combo:
        for i in range(len(decimal_list)):
            if decimal_list[i] == item:
                minimized_prime_implicants.append(prime_implicants[i])

        
    return minimized_prime_implicants

def string_generator(input_names,implicant,operand):
    #to generate string from implicant that can ba parsed to plot the logic circuit
    #operand is 1 if SoP and 2 if PoS

    no_variable = False    #only true if the answer is pure logic 0 or logic 1

    #split the literal in the implicant
    temp_list = list(implicant)

    if temp_list.count('x') == len(temp_list):   #check if the implicant only contain 'x' which then implies either pure logic 0 or 1
        no_variable = True
        string = None
    
    elif temp_list.count('x') == len(temp_list) - 1:    #the implicant only depends on one inputs which have a different string generation procedure
        for index, digit in enumerate(temp_list):
            if digit != 'x':
                if (digit == '0' and operand == '1') or (digit == '1' and operand == '2'):
                    string = input_names[index]
                elif (digit == '1' and operand == '1') or (digit == '0' and operand == '2'):
                    string = '~' + input_names[index]
    
    else:
        holding_list = []
        for index,digit in enumerate(temp_list):
            if digit != 'x':
                if (digit == '0' and operand == '1') or (digit == '1' and operand =='2'):
                    string_temp = '~' + input_names[index]
                    holding_list.append(string_temp)
                elif (digit == '1' and operand == '1') or (digit == '0' and operand == '2'):
                    string_temp = input_names[index]
                    holding_list.append(string_temp)
        
        #combine the string using nand or nor depending on the operand
        if operand == '1':
            string = ' nand '.join(holding_list)
        else:
            string = ' nor '.join(holding_list)

    return no_variable,string


def string_combined(input_names,implicants_list,operand):
    #to combine the string for each implicants into a final lo

    if len(implicants_list) == 1:
        no_variable, string = string_generator(input_names,implicants_list[0],operand)
        if no_variable:
            if operand == '1':
                answer = 'buf(1)'
            else:
                answer = 'buf(0)'
        else:
            if ('nand' or 'nor') in string:
                answer = '~('+ string + ')'
            else:
                if '~' in string:
                    string = string[1:]
                    answer = 'buf(' + string + ')'
                else:
                    answer = '~' + string
    
    else:
        answer_list = []
        for implicants in implicants_list:
            no_variable, string = string_generator(input_names,implicants,operand)
            string = '(' + string + ')'
            answer_list.append(string)
        
        if operand == '1':
            answer = ' nand '.join(answer_list)
        else:
            answer = ' nor '.join(answer_list)
    
    return answer

def is_list_integers(integer_list):
    output = True
    for element in integer_list:
        if not isinstance(element,int):
            output = False
            break
    return output



print("Welcome to the 2 Level Logic Minimization Machine")
print("Are you looking for SoP (Sum of Products) or PoS (Product of Sums) Implementation?")

while True:
    operands = input("Press 1 for SoP and Press 2 for PoS: ")
    if operands not in ['1','2']:
        print("Input Invalid. Please try again.")
        continue
    else:
        break

while True:
    if operands == '1':
        print("Please enter the minterms for the Sum of Products (SoP).")
        print("Format: a Python-style list of integers")
        print("Example: [1, 2, 3, 4, 5], MAKE SURE THERE's NO DECIMAL POINTS")
        response = input("Enter the minterms here: ")
        terms = ast.literal_eval(response)

        if not is_list_integers(terms):
            print("Non-Integer inputs detected. Please try again\n")
            continue

    elif operands == '2':
        print("Please enter the maxterms for the Product of Sums (PoS).")
        print("Format: a Python-style list of integers")
        print("Example: [1, 2, 3, 4, 5], MAKE SURE THERE's NO DECIMAL POINTS")
        response = input("Enter the maxterms here: ")
        terms = ast.literal_eval(response)

        if not is_list_integers(terms):
            print("Non-Integer inputs detected. Please try again\n")
            continue
    break

print()
print()
print("Thanks for inputting the terms correctly. Next, you will be required to input the don't care terms")

while True:
    print("Format: a Python-style list of integers")
    print("Example: [1, 2, 3, 4, 5], MAKE SURE THERE's NO DECIMAL POINTS")
    response = input("Enter the don't care terms here: ")
    doncare = ast.literal_eval(response)

    if not is_list_integers(doncare):
        print("Non-Integer inputs detected. Please try again\n")
        continue
    break

minimized_prime_implicants = minimization(terms,doncare)

num_inputs = len(minimized_prime_implicants[0])

count = 0
print()
print()
print("Now, you are required to input the names for each of the inputs for graphing purposes")
print(f"Based on the your previous inputs, your answer will consist of {num_inputs:.0f} inputs")
print("Starting from the Most Significant Bit (MSB) to the Least Significant Bit (LSB), (ie : input 1 is the MSB)\nPlease input the names accordingly")

input_names = []
while count < num_inputs:
    name = input(f"Please enter the name for input {(count + 1):.0f} :")
    input_names.append(name)
    count += 1

string = string_combined(input_names,minimized_prime_implicants,operands)
if 'buf(0)' in string:
    print("Output = Logic 0")
elif 'buf(1)' in string :
    print("output = Logic 1")
else:
    d = logicparse(string, outlabel='Output')
    d.draw()










        






                
            
            
    
        
         
                
            
    
            
        
                    
            


            
                
            
            
            
        
        
        
    
        
                    
                    
                
            
                
                
                    
                    
            
    
    


        
    