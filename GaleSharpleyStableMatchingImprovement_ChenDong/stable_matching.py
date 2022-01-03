import sys


def read_prefs(pref_1_filename, pref_2_filename):
    # This function reads preferences from two files
    # and returns two-dimensional preference lists and the length of a list.
    with open(pref_1_filename, 'r') as f:
        hospital_raw = f.read().splitlines()
    with open(pref_2_filename, 'r') as f:
        student_raw = f.read().splitlines()
    N = int(student_raw[0])
    hospital_prefs = [[int(id) for id in  x.split(',')] for x in hospital_raw[1:]]
    student_prefs = [[int(id) for id in  x.split(',')] for x in student_raw[1:]]
    return N,  hospital_prefs, student_prefs

def inverse_prefs(N, prefs):    
    ranks = N*[0] 
    for i in range(N):
        ranks[prefs[i]]=i
    return ranks

def run_GS(N, hospital_prefs, student_prefs, out_name):
    current = match_GS(N,hospital_prefs,student_prefs)
    # write out matches
    with open(out_name, 'w') as f:
        for student, hospital in enumerate(current):
            f.write(str(hospital)+','+str(student)+'\n')

def match_GS(N, hospital_prefs, student_prefs):
    free_hospital = list(range(N))
    count = N*[0]               # stores a pointer to each hospital's next unproposed student, going from the left of hospital's preference list 
    current = N*[None]          # stores current assignment; index -> student, value -> hospital
    # print('--------')
    # print(student_prefs)
    student_inverse_prefs = [inverse_prefs(N, student_pref) for student_pref in student_prefs]
    # print(student_inverse_prefs)
    # print(hospital_prefs)
    # algorithm - Hospital giving offer to student
    while free_hospital:  # returns True if list is nonempty
        # print('--------')
        # print('current:', current)
        # print('free hospital', free_hospital)
        hospital = free_hospital.pop(0)
        student = hospital_prefs[hospital][count[hospital]]
        # print(hospital, 'proposing to', student)
        count[hospital] += 1
        if current[student] is None:   # student is not paired 
            current[student] = hospital
            # print('student is not paired')
        else:
            # slow way to compute 
            if student_inverse_prefs[student][current[student]] < student_inverse_prefs[student][hospital]:
                ############################################################
                # The code in the if statement runs in linear time!
                # Fix that...
                ############################################################
                free_hospital.append(hospital)
            else:
                # student switches to new hospital, old hospital becomes free
                # print('student prefers', hospital)
                free_hospital.append(current[student])
                current[student] = hospital
    return current;

############################################################
############################################################

def check_stable(N, hospital_prefs, student_prefs, match_file):
    # Implement checking of stable matches from output
    # ...
    with open(match_file, 'r') as f:
        match_raw = f.read().splitlines()
    match = [[int(id) for id in  x.split(',')] for x in match_raw]
    hospital_inverse_prefs = [inverse_prefs(N, hospital_pref) for hospital_pref in hospital_prefs]
    student_inverse_prefs = [inverse_prefs(N, student_pref) for student_pref in student_prefs]
    for hospital,student in match:

        for student_index in range(hospital_inverse_prefs[hospital][student]):

            preferred_student = hospital_prefs[hospital][student_index]
            
            if student_inverse_prefs[preferred_student][hospital] < student_inverse_prefs[preferred_student][match[preferred_student][0]]:
                # print("testing match",hospital,student)
                # print("h",hospital," rank s",student," ",hospital_inverse_prefs[hospital][student],sep="")
                # print("h",hospital," rank s",preferred_student," ",hospital_inverse_prefs[hospital][preferred_student],sep="")
                # print("s",preferred_student," rank current h",hospital," ",student_inverse_prefs[preferred_student][hospital],sep="")
                # print("s",preferred_student," rank matched h",match[preferred_student][0]," ",student_inverse_prefs[preferred_student][match[preferred_student][0]],sep="")
                # print("s",preferred_student," perfers h",hospital," to h",match[preferred_student][0],sep="")
                print(0)     # if not stable
                return
    print(1)     # if stable
    # Note: Make the printing of stableness be the only print statement for submission!
    
############################################################
############################################################

def check_unique(N, hospital_prefs, student_prefs):
    # Implement checking of a unique stable matching for given preferences
    # ...
    sh = match_GS(N,hospital_prefs,student_prefs)
    hs = match_GS(N,student_prefs,hospital_prefs)
    for s,h in enumerate(sh):
        if(hs[h]!=s):
            print(0)     # if not unique
            return
    print(1)     # if unique
        
############################################################
# Main function. 
############################################################

def main():
    # Do not modify main() other than using the commented code snippet for printing 
    # running time for Q1, if needed
    if(len(sys.argv) < 5):
        return "Error: the program should be called with four arguments"
    hospital_prefs_raw = sys.argv[1] 
    student_prefs_raw = sys.argv[2]
    match_file = sys.argv[3]
    # NB: For part 1, match_file is the file to which the *output* is wrtten
    #     For part 2, match_file contains a candidate matching to be tested.
    #     For part 3, match_file is ignored.
    question = sys.argv[4]
    N, hospital_prefs, student_prefs = read_prefs(hospital_prefs_raw, student_prefs_raw)
    if question=='Q1':
        # start = time.time()
        run_GS(N, hospital_prefs,student_prefs,match_file)
        # end = time.time()
        # print(end-start)
    elif question=='Q2':
        check_stable(N, hospital_prefs, student_prefs, match_file)
    elif question=='Q3':
        check_unique(N, hospital_prefs, student_prefs)
    else:
        print("Missing or incorrect question identifier (it should be the fourth argument).")
    return

if __name__ == "__main__":
    # example command: python stable_matching.py pref_file_1 pref_file_2 out_name Q1
    
    # stable_matching.py: filename; do not change this
    # pref_file_1: filename of the first preference list (proposing side)
    # pref_file_2: filename of the second preference list (proposed side)
    # out_name: desired filename for output matching file
    # Q1: desired question for testing 
    main()
