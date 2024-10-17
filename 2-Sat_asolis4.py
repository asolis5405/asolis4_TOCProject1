#!/usr/bin/env python3
import collections
import sys
import csv
from typing import List
import copy
import time
import matplotlib.pyplot as plt

#Functions
def dpll(c: int, v: int, clauses: List[List[int]]) -> bool:
    variables = [None for _ in range(v)] #initiate variables to all be null
    decision_stack = [] #initiate stack to backtrack
    clauses_copy = copy.deepcopy(clauses)  #create a copy of clauses to avoid modifying original (for backtracking)

    while True:
        #if clauses_copy is empty then problem is satisfiable since all clauses have been satisfied
        if not clauses_copy:
            return True
        # if all(len(clause) == 0 for clause in clauses_copy):
        #     return True

        
        if any(len(clause) == 0 for clause in clauses_copy): #if clause length == 0 then we must backtrack since it means the clause could not be satisfied
            while decision_stack: #will continue as long as there are decisions left
                last_decision, last_value = decision_stack.pop() #returns most recent decision from the stack and saves to corresponding variables
                if last_value:  #if last value assigned was true then try assigning false
                    decision_stack.append((last_decision, False))
                    variables[last_decision - 1] = False
                    clauses_copy = reduce_clauses(clauses, -last_decision) #reduce clauses again with new truth assignment
                    break
                else:
                    #if false also fails continue backtracking
                    variables[last_decision - 1] = None
            if not decision_stack:
                return False  #if decision stack is empty the problem is unsatisfiable
            continue 

        #call unit propogation function
        unit_result = unit_clause_prop(clauses_copy, variables)
        if not unit_result:
            #call pure literal elimination if unit propagation returns false
            pure_result = pure_literal(clauses_copy, variables)
            if not pure_result:
                #if both unit prop and pure literal elimination fail assign variable with value
                var_to_assign = next((i + 1 for i in range(v) if variables[i] is None), None)
                if var_to_assign is None: #if no unassigned variables left return false since unsatisfiable
                    return False  
                decision_stack.append((var_to_assign, True))#assign variable with true
                variables[var_to_assign - 1] = True
                clauses_copy = reduce_clauses(clauses_copy, var_to_assign)#reduce clauses with new truth assignment


    

def unit_clause_prop(clauses: List[List[int]], variables: list) -> bool:
    changed = False #initiate changed variable to check if unit propogation was used
    while True:
        unit_clauses = [] #initiate list of unit clauses
        for c in clauses:
            if len(c) == 1: unit_clauses.append(c[0])
        if not unit_clauses:  #if no unit clauses
            return changed
        # unit_clauses = [c[0] for c in clauses if len(c) == 1]
        # if not unit_clauses:
        #     return changed
        
        changed = True #if unit clauses found
        for unit in unit_clauses:
            var = abs(unit)
            if unit > 0: #if value is positive assign true, else assign false
                value = True
            else:
                value = False

            if variables[var - 1] is not None and variables[var - 1] != value: #check if variable has already been assigned and if assigned value contradicts current value
                return False #conflict
            
            variables[var-1] = value #if no conflict, assign it value

            for clause in clauses: #if unit value in clause delete entire clause
                if unit in clause:
                    clauses.remove(clause)
            for clause in clauses: #if negated unit value in clause delete value from clause
                if -unit in clause:
                    clause.remove(-unit)
    

def pure_literal(clauses: List[List[int]], variables: list) -> bool:
    literal_count = {} #keep counts of all literals
    changed = False #check if pure literal found
    #gather counts for all literals
    for clause in clauses:
        for literal in clause:
            if literal in literal_count:
                literal_count[literal] += 1
            else:
                literal_count[literal] = 1


    #add all pure literals occuring more than once to a pure_literals set
    pure_literals = set()
    for literal in literal_count:
        if literal_count[literal] > 1 and -literal not in literal_count:
            pure_literals.add(literal)
    
    
    #remove clauses containing pure literals
    for pure in pure_literals:
        var = abs(pure)
        variables[var - 1] = pure > 0  #assign the pure literal
        clauses[:] = [clause for clause in clauses if pure not in clause] #create new list of clauses without pure literals
        changed = True
    
    return changed
    # literal_count = collections.defaultdict(int)
    # for clause in clauses:
    #     for literal in clause:
    #         literal_count[literal] += 1
    
    # pure_literals = set(literal for literal in literal_count if -literal not in literal_count)
    # if not pure_literals:
    #     return False
    
    # for pure in pure_literals:
    #     var = abs(pure)
    #     value = pure > 0
    #     variables[var - 1] = value
    #     clauses[:] = [clause for clause in clauses if pure not in clause]
    
    # return True

def reduce_clauses(clauses: List[List[int]], assignment: int) -> List[List[int]]:
    
    new_clauses = [] #initiate new clauses list
    for clause in clauses:
        if assignment in clause:
            continue  #clause is satisfied
        new_clause = [lit for lit in clause if lit != -assignment]  #remove the negated literal
        if not new_clause:
            return []  #clause is empty
        new_clauses.append(new_clause)
    return new_clauses

#Main
def main():
    x_satis = []
    x_unsatis = []
    y_satis = []
    y_unsatis= []


    file_name = "practice_test.csv"
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        clauses = []
        c = 0

        for line in csvFile:
            if line[0] == 'c':
                problemNum = int(line[1])
                print(f"Problem:{problemNum}") #print problem number
            elif line[0] == 'p':
                varNum = int(line[2])
                clauseNum = int(line[3])
            else:
                clause = [int(num) for num in line[:-2]]  #ignore 0 at end 
                clauses.append(clause)
                c += 1
                if c == int(clauseNum):
                    # start time and call dpll function
                    start = time.time()
                    satisfiable = dpll(clauseNum, varNum, clauses)  
                    exec_time = time.time() - start

                    #update x and y values
                    if satisfiable:
                        x_satis.append(clauseNum * 2)#number of literals
                        y_satis.append(exec_time)
                    if not satisfiable:
                        x_unsatis.append(clauseNum * 2)
                        y_unsatis.append(exec_time)

                    print("Satisfiable" if satisfiable else "Unsatisfiable")

                    c = 0  #restart clause count and clauses list
                    clauses = []
                    

    # for x in x_satis:
    #     print(x)
    # for y in y_satis:
    #     print(y)
    # for x in x_unsatis:
    #     print(x)
    # for y in y_unsatis:
    #     print(y)
    
    
                
if __name__ == '__main__':
    main()