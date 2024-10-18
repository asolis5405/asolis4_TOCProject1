Readme_asolis4
Version 1 8/22/24

A copy of this file should be included in the github repository with your project. Change the teamname above to your own
Team name: 
    asolis4

Names of all team members: 
    Anaregina Solis

Link to github repository: 
    https://github.com/asolis5405/asolis4_TOCProject1.git

Which project options were attempted: 
    2-SAT Solver using DPLL algorithm

Approximately total time spent on project: 
    15hrs

The language you used, and a list of libraries you invoked.: 
    Language: Python;
    Libraries: csv, time, typing: List

How would a TA run your program (did you provide a script to run a test case?):
    To run on terminal after making executable: ./2-Sat_Solver_asolis4.py 
    Currently the script reads in the file of test cases provided in the Resources page (test_cases_asolis4) and outputs the results in the output file (output_asolis4). 

A brief description of the key data structures you used, and how the program functioned.: 

    Key data structures used were lists, dictionaries, and sets. I used lists to hold the x and y values containing number of literals and execution time for each case. The most important list of my program is the list containing the clauses of each case. This is the list that gets passed to the dpll function, the unit propogation function, and the pure literal elimination function. Throughout these functions, the  clauses list gets modified with the purpose of finding the truth assignments that will cause each clause to return True. Another important list I used was the variables list which also gets passed to all three functions and contains the assignment (truth value) for each variable. The assignemnts get modified with the goal of satisfying a clause (making it True). Sets are introduced in the pure_literal function with the literal_count set containing the occurances of each literal as well as the pure_literals set which later becomes a dictionary containing the literals as keys and their assigned values as values. This dictionary is used to find pure literals in order to eliminate clauses. In the end, the dpll algorithm will return True (satisfiable) if all clauses have been satisfied (clauses list returns empty). If however, one of the clauses is not satisfied (a clause has no literals left) then the dpll algorithm will return False (unsatisfiable).

A discussion as to what test cases you added and why you decided to add them (what did they tell you about the correctness of your code). Where did the data come from? (course website, handcrafted, a data generator, other): 

    I added the test casess found on the course's Resources page called 
    2SAT.cnf.csv (saved as test_cases_asolis4 in my repository). I decided to add them since they would evaluate whether my code was capable of reading in multiple entries at a time. Furthermore, the large amount of test cases in this file ensured that my program would be tested with a variety of different cases that could present challenges I had not considered beforehand. I also knew that these test cases contained 50 satisfiable cases and 50 unsatisfiable cases, therefore, I would be able to test the correctness of my code by testing if it identified those exact numbers of satisfiable and unsatisfiable test cases, which it did. 

An analysis of the results, such as if timings were called for, which plots showed what? What was the approximate complexity of your program?:

    To analyze my results I created a scatter plot comparing the number of literals to the execution time for each case. The number of literals was computed my multiplying the number of clauses by 2 since there are 2 literals per clause. Execution time (s) was recorded by using .time() from the time library. The plot of this data created an exponential function, however, because of the 2-SAT solver's efficiency, the exponential curve was more of linear line. The line gave the formula y = 4E-05e^(0.029x). The approximate time complexity of my program was O(n) since the plot could produce a linear graph.
    
A description of how you managed the code development and testing.
Did you do any extra programs, or attempted any extra test cases:

    I attempted an extra program where I did not implement recursion (old_draft_asolis4.py). This program ultimately ended up not working since I had to use the stack to backtrack whenever a clause was not satisfied. This program classified 70 cases as satisfiable, which is not correct. After working on this program for almost 2 days I decided to start from scratch on my new program 2-Sat_Solver_asolis4.py. In this program I implement recursion and use parts of my functions from the previous program to create a working dpll algorithm that calls on the functions unit_clause_prop and pure_literal. This program returns 50 satisfiable and 50 unsatisfiable cases from the test_cases_asolis4.csv file, which I was told was the correct output. Furthermore, after solving 10 cases by hand, I was able to verify that the program gave the correct output for the 10 cases. This, along with the 50/50 split between satisfiable and unsatisfiable, makes me beleive that my program is correct.

