#!/usr/bin/env python3
import collections
import sys
import csv
from typing import List, Dict

#Functions
def dpll(c: int, v: int, clauses: List[List[int]]) -> bool:
    variables = [None for _ in range(v)] #initiate variables to all be null
    run = True
    run2 = True

    while run:
        run = unit_clause_prop(clauses, variables)


    while run2:
        run2 = pure_literal(clauses, variables)
    

    print(variables)
    
    if not clauses:
         return True
    

def unit_clause_prop(clauses: List[List[int]], variables: list) -> bool:

    unit_clauses = []
    for c in clauses:
        if len(c) == 1: unit_clauses.append(c[0])
    if not unit_clauses: 
        return False

    for unit in unit_clauses:
        var = abs(unit)
        if unit > 0:
            value = True
        else:
            value = False
        variables[var-1] = value

        for clause in clauses:
            if unit in clause:
                clauses.remove(clause)
        for clause in clauses:
            if -unit in clause:
                clause.remove(-unit)
        
    return True

def pure_literal(clauses: List[List[int]], variables: list) -> bool:

    literal_count = {}

    # Step 1: Count occurrences of each literal
    for clause in clauses:
        for literal in clause:
            if literal in literal_count:
                literal_count[literal] += 1
            else:
                literal_count[literal] = 1


    # Step 2: Identify pure literals that appear more than once
    pure_literals = set()
    for literal in literal_count:
        if literal_count[literal] > 1 and -literal not in literal_count:
            pure_literals.add(literal)
    

    # Step 3: Remove clauses containing pure literals
    for pure in pure_literals:
        clauses[:] = [clause for clause in clauses if pure not in clause]
    
    return False

    


#Main
def main():

    file_name = "practice_test.csv"
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        clauses = []
        c = 0

        for line in csvFile:
            if line[0] == 'c':
                problemNum = line[1]
                print(f"Problem:{problemNum}")
            elif line[0] == 'p':
                varNum = int(line[2])
                clauseNum = int(line[3])
            else:
                clause = [int(num) for num in line[:-2]]  #ignore 0 at end CHANGE FOR TEST CASES
                clauses.append(clause)
                c += 1
                if c == int(clauseNum):
                    #call dpll function
                    if dpll(clauseNum, varNum, clauses):
                        print("Satisfiable")
                    else:
                        print("Unsatisfiable")
                    c = 0
                    clauses = []
                
                    
if __name__ == '__main__':
    main()