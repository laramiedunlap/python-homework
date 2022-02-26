### PyBank Program
* A simple program that goes through a .csv or .txt file and summarizes the profit/loss data along with the dates.
* The program tracks peak profit, lowest profit (i.e. biggest loss), the average change in profit from month-to-month, along with outputing a *summaryfile.txt*
* I also included code that checks for data entry errors. For example, if the program comes across a profit/loss = 14g569 -- it will return the line number and example to the user
* The program also handles empty lines, and empty lines with white space. I felt it was a nice feature to add, that way the program doesn't error out if someone in data entry pressed the enter key one too many times or they pressed it at the end of the file. 
* I've included a **budget_data_test.txt** document with data entry errors -- feel free to add mistakes to it and see if the program can handle it! 
* The user can choose whether or not they want a summary file when using *main.py* by using the '--summaryfile' flag before the input file:          

    <pre><code>'python main.py --summaryfile budget_data.csv'</code></pre>

* I use Juptyer Lab (.ipynb) notebook files to test code blocks then put it all together in a .py file that can be ran from the command line. Sometimes the two are not mirror matches of each other. I do not include command line parsing code in the .ipynb files as those are easiest to run inside the JupyterLab notebook or VS studio. However it could be easily copied over from the python file.

 


    
