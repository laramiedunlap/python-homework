import csv
import sys

# Define a function so that we don't have to lookup 
# the price and cost every time, while checking 
# for an update so we don't loop excessively:
def match_price_cost(item_sold, _menu, out_dict, user_keys):
    """extracts price/cost/profit data of a sold item from a menu,
        then creates a nested dictionary inside out_dict with
        user_keys """
    update_done = False
    # loop through the lists stored in _menu:
    for item in _menu:
        # check for matching item
        if item_sold == item[0] and not update_done:
            # create a nested dict in out_dict,
            # add price and cost to out_dict,
            out_dict[item_sold] = {}
            out_dict[item_sold]["--price"]= float(item[-2])
            out_dict[item_sold]["--cost"]= float(item[-1])
            out_dict[item_sold]["--profit"]= float(out_dict[item_sold]["--price"] - out_dict[item_sold]["--cost"])
            # add user defined keys:
            for key in user_keys:
                out_dict[item_sold][key]= 0
            update_done = True
    if update_done == False: 
        print(f"{item_sold} cannot be found in Menu! Update Menu!")
        sys.exit(1)
    return None

# Define a finction to remove keys used for calculating user_keys once we're done with them:
def remove_keys(dict,keys_to_remove):
    """Remove a list of keys from dict, return dict"""
    for key in keys_to_remove:
        dict.pop(key)
    return dict

# Aggregate data for report, print to summary file if requested:
def ramen_report(csv_menu_filename, csv_sales_filename, report_request):
    # Make empty lists for menu and sales:
    menu = []
    sales = []
    # Read in menu and sales data from .csv files,
    # skipping the headers, and store in memory:
    with open(csv_menu_filename, 'r') as menu_file, open(csv_sales_filename,'r') as sales_file:
        menu_reader = csv.reader(menu_file, delimiter =',')
        sales_reader = csv.reader(sales_file,delimiter =',')
        next(menu_reader,None)
        next(sales_reader,None)
        for row in menu_reader:
            menu.append(row)
        for row in sales_reader:
            sales.append(row)


    # Make report dict and keys for nested dict:
    report = {}
    user_keys = ["01-count","02-revenue","03-cogs","04-profit"]

    # Build Report dict: 
    for sale in sales:
        sale_item = sale[-1]
        quantity = int(sale[-2])
        if sale_item in report.keys():
            dict_pointer = report[sale_item]
            dict_pointer["01-count"] += quantity
            dict_pointer["02-revenue"] += dict_pointer["--price"] * quantity
            dict_pointer["03-cogs"] += dict_pointer["--cost"] * quantity
            dict_pointer["04-profit"] += dict_pointer["--profit"] * quantity
        else:
            match_price_cost(sale_item, menu, report, user_keys)

    for sales_items in report:
        remove_keys(report[sales_items],["--price","--cost","--profit"])
    
    if report_request:
        with open("report.txt","w") as report_file:
            print(f"Creating report file")
            # print("\n")
            print("...")
            report_file.write(f"-----REPORT-----")
            report_file.write("\n")
            for item in report: 
                report_file.write(f"{item} {report[item]}")
                report_file.write("\n")
            report_file.close()
            print("done")
    else: 
        for item in report:
            print(f"{item} {report[item]}")
            print("\n")

def main():
    # This is command-line parsing code.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--reportfile] menufile [.csv] salesfile [.csv]")
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    report_request = False
    if args[0] == "--reportfile":
        report_request = True
        del args[0]
    # Set the filenames variables to the user input files
    csv_menu_filename = args[0]
    csv_sales_filename = args[1]
    # Call the ramen_report function
    ramen_report(csv_menu_filename, csv_sales_filename, report_request)




if __name__ == '__main__':
  main()
 

