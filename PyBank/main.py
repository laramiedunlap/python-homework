import os
import sys
import re
from pathlib import Path
# Create some data structures and variables for our program


def fin_analysis(filename,summary):
    """Given a filename and directions whether or not to create a summary file,
        return the summary data and summaryfile.txt if requested """
    budget = {}
    profit_loss_total = 0
    profit_loss_high = []
    profit_loss_low = []

    
    with open(filename, mode = 'r') as f:

    # Creates an iterable "i" that we will use for error references.
        i = 0
        empty_lines = []
        error_dict = {}
        error_condition = False
    # Starts the main loop:
        for line in f:
            i += 1 
            if i > 0:
                
                # Checks for a specific concantenation of 3 letters for month, 4 digits for year, a comma,
                # Then everything after that in the line (which SHOULD only be numbers, but we'll double check later). 
                budget_item_match = re.search(r'(\w\w\w-\d\d\d\d),(.+)', line)

                # The above is simple to work with but creates one issue. In the second group (.+), we just grab everything after the comma because
                # Some numbers have a negative sign. We need to make certain that our second item is actually a number (imagine someone typed in "n/a" 
                # or accidently entered a "Q" instead of "1").
                if budget_item_match:
                    # Set a variable equal to our P/l as a string object, so that we can iterate through it real quick and make sure it fits the right format
                    check_pl_data = budget_item_match.group(2)
                    error_condition = False
                    # Here we loop through each 'ch' character in the string check_data. If the ch is a negative sign or a digit, we pass. 
                    for ch in check_pl_data:
                        if ch == "-":
                            pass
                        elif ch.isdigit():
                            pass
                        # Here we know there is an error, but there could be multiple errors on the same line
                        elif error_condition == False:
                            error_condition = True
                            error_character = ch 
                            error_dict[i] = [line, error_character]
                        # Now we know there are multiple errors, so we can just add them to the "ch" string
                        else:
                            error_character += ch
                            error_dict[i] = [line, error_character]

                    # Now we want to start tracking some P/L data as it's coming in:
                    if profit_loss_total == 0:
                        profit_loss_total = int(budget_item_match.group(2))
                        profit_loss_high = [budget_item_match.group(1) ,int(budget_item_match.group(2))]
                        profit_loss_low = [budget_item_match.group(1) ,int(budget_item_match.group(2))]
                        new_key = 1
                        budget[new_key] = (budget_item_match.group(1),int(budget_item_match.group(2)))
                    elif error_condition == False:
                        # At this point, I want to force our budget{} keys to be sequential regardless of how many blank lines there are:
                        new_key += 1 
                        budget[new_key] = (budget_item_match.group(1),int(budget_item_match.group(2)))
                        profit_loss_total = profit_loss_total + int(budget_item_match.group(2))
                        #Tracks the most recent high mark for monthly p/l
                        if profit_loss_high[-1] <= int(budget_item_match.group(2)):
                            profit_loss_high = [budget_item_match.group(1) ,int(budget_item_match.group(2))]
                        #Tracks the most recent low mark for monthly p/l
                        elif profit_loss_low[-1] >= int(budget_item_match.group(2)):
                            profit_loss_low = [budget_item_match.group(1) ,int(budget_item_match.group(2))]

                # Now we're checking for a line we don't know what to do with:    
                if not budget_item_match:
                    # Next we skip the first row, where the header is expected.
                    if i == 1:
                        pass
                    # Next we check for an empty line OR an empty line with whitespaces 
                    # (which is why using line == '\n' would not comprehensively solve the issue).
                    elif len(line.strip()) == 0:
                        empty_lines.append(i)
                        
                    # Finally if there is still an issue, we error out and print the line with an issue, formatting instructions, and directions to user.
                    else:
                        error_dict[i] = [line, 'multiple errors']

                        

    #Now we need to calculate the proper average. A dictionary isn't sorted inherently, but since we iterated new_key, all the key-value pairs match up with the 
    #monthly progression of the data. So step 1) grab all the values and turn them into a list:
    budget_items_object = budget.values()
    budget_tuples_list = list(budget_items_object)
    p_l_list = []
    deltas = []
    #step 2) loop through all the tuples and grab the profit from each month, creating a list of all the SEQUENTIAL CHANGES:
    for v in range(len(budget_tuples_list)):
        budget_tup = budget_tuples_list[v]
        p_l_list.append(budget_tup[1])
    #step 3) build a list of all the month-to-month deltas in p/l:
        if v >= 1:
            deltas.append(p_l_list[v] - p_l_list[v-1])
    average_deltas = (sum(deltas)/len(deltas))

    if empty_lines:
        print("\n")
        print(f"Empty Line(s) #: {empty_lines}\n")
    
    if error_dict.keys():
        for i in error_dict:
            print(f"Error on line # {i}: {error_dict[i]}' {error_dict[i][1]} ' caused an error")
        print(f"File must include 1 header row in first line")
        print(f"Date in first column (MON-YEAR, ex: JAN-2001)")
        print(f"Profit/loss in 2nd colummn without $ (ex: -189000)")
        print("Please remove or reformat line(s), save the file, and retry\n")
    
    print("Financial Analysis")
    print("----------------------------")
    print(f"Total Months: {new_key}")
    print(f"Total: {profit_loss_total}")
    print(f"Average Change: ${round(average_deltas,2)}")
    print(f"Greatest Increase in Profits: {profit_loss_high[0]} (${profit_loss_high[1]})")
    print(f"Greatest Decrease in Profits: {profit_loss_low[0]} (${profit_loss_low[1]})")

    if summary:
        print("----------------------------")
        print("\ncreating summary file\n...")
        with open("summaryfile.txt", "w") as summary_f:
            summary_f.write("Financial Analysis\n----------------------------\n")
            summary_f.write(f"Total Months: {new_key}\n")
            summary_f.write(f"Total: {profit_loss_total}\n")
            summary_f.write(f"Average Change: ${round(average_deltas,2)}\n")
            summary_f.write(f"Greatest Increase in Profits: {profit_loss_high[0]} (${profit_loss_high[1]})\n")
            summary_f.write(f"Greatest Decrease in Profits: {profit_loss_low[0]} (${profit_loss_low[1]})\n")
        summary_f.close()
        print("done")
    return None 

def main():
    # This is command-line parsing code.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--summaryfile] file [file...]")
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == "--summaryfile":
        summary = True
        
    # Set the filename variable to the user input file
    filename = args[1]
    # Call the fin_analysis function
    fin_analysis(filename,summary)
    
    

if __name__ == '__main__':
  main()