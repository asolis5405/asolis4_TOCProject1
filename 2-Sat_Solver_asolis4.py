#!/usr/bin/env python3
import collections
import sys
import csv
from typing import List
import time
import matplotlib.pyplot as plt

#Functions
def dpll(clauses: List[List[int]], variables: list) -> bool:
    #check for unit prop
    while any(len(clause) == 1 for clause in clauses):
        unit_clause_prop(clauses, variables)
    
    #check for pure lit elim
    pure_literal(clauses, variables)
        
    #check if all clauses have been satisfied
    if not clauses:
        return True #satisfiable
    
    #check if any clauses are left empty, meaning they were not satisfied
    if any(len(clause) == 0 for clause in clauses):  
        return False #unsatisfiable

    #select a literal and pass to recursive step 
    #if dpll returns false with assigned literal then dpll with the negative literal will be called
    l = clauses[0][0]
    return dpll(clauses + [[l]], variables) if dpll(clauses + [[l]], variables) else dpll(clauses + [[-l]], variables)


def unit_clause_prop(clauses: List[List[int]], variables: list) -> bool:
    #find unit clauses by checking for len of 1
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
        
        
    if unit_clauses:   
        for unit in unit_clauses:
            var = abs(unit)
            if unit > 0: #if value is positive assign true, else assign false
                variables[var - 1] = True
            else:
                variables[var - 1] = False

            #if unit value in clause delete entire clause
            for clause in clauses:
                if unit in clause:
                    clauses.remove(clause)
            #if negated unit value in clause delete value from clause
            for c, clause in enumerate(clauses):
                clauses[c] = [l for l in clause if l != -(unit)]
        
    
def pure_literal(clauses: List[List[int]], variables: list) -> bool:
    literal_count = {} #keep counts of all literals
    
    #gather counts for all literals
    for clause in clauses:
        for literal in clause:
            if literal in literal_count:
                literal_count[literal] += 1
            else:
                literal_count[literal] = 1


    #add all pure literals to a pure_literals set if its negative is not present
    pure_literals = set()
    pure_literals = {literal: v for literal, v in literal_count.items() if -(literal) not in literal_count}
    
    #remove clauses containing pure literals
    for lit in pure_literals.keys():
        var = abs(lit)
        if lit > 0:
            variables[var - 1] = True
        else:
            variables[var - 1] = False
        clauses[:] = [clause for clause in clauses if lit not in clause]
    

#Main
def main():
    #initiate vars for creating graph
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
                variables = [None for _ in range(varNum)] #initiate variables to all be null
            else:
                clause = [int(num) for num in line[:-2]]  #ignore 0 at end 
                clauses.append(clause)
                c += 1
                if c == int(clauseNum):
                    # start time and call dpll function
                    start = time.time()
                    satisfiable = dpll(clauses, variables)  
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
                    
    #needed only for printing x and y values
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