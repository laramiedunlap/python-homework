### PyBank Program
* A simple program that goes through a .csv or .txt file and summarizes the profit/loss data along with the dates.
* The program tracks peak profit, lowest profit (i.e. biggest loss), the average change in profit from month-to-month, along with outputing a summaryfile.txt
* I included modules that check for data entry errors, for instance, if the program comes across a profit/loss = 14g569 -- it will return the line number and example to the user:
     if budget_item_match:
                    <pre><code># Set a variable equal to our P/l as a string object, so that we can iterate through it real quick and make sure it fits the right format
                    check_pl_data = budget_item_match.group(2)
                    # Here we loop through each 'ch' character in the string check_data. If the ch is a negative sign or a digit, we pass. 
                    for ch in check_pl_data:
                        if ch == "-":
                            pass
                        elif ch.isdigit():
                            pass
                        else:
                            print(f"Error on line # {i}: {line}--' {ch} '  has caused an error")
                            print(f"File must include 1 header row in first line, date in first column (MON-YEAR, ex: JAN-2001), and profit/loss in 2nd colummn without $ (ex: -189000)")
                            print("Please remove or reformat line, save the file, and retry")
                            sys.exit(1)</code></pre>

* The user also can choose whether or not they want a summary file. To just run the output to the terminal, simply ommit the flag '--summaryfile' from the cmd line argument
    
