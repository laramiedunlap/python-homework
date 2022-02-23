### PyBank Program
* A simple program that goes through a .csv or .txt file and summarizes the profit/loss data along with the dates.
* The program tracks peak profit, lowest profit (i.e. biggest loss), the average change in profit from month-to-month, along with outputing a summaryfile.txt
* I included code that check for data entry errors. For instance, if the program comes across a profit/loss = 14g569 -- it will return the line number and example to the user
* The program also handles empty lines, and empty lines with white space. I felt it was a nice feature to add, that way the program doesn't error out if someone in data entry pressed the enter key one too many times or they pressed it at the end of the file. 
* I've included a budget_data_test.txt document with data entry errors -- feel free to add mistakes to it and see if the program can handle it 
* The user can choose whether or not they want a summary file when using main.py by using the '--summaryfile' flag before the input file:          

    <pre><code>'python main.py --summaryfile budget_data.csv'</code></pre>



    
