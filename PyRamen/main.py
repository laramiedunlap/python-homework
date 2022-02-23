import csv
import sys

# Top down, we need to make INDIVIDUAL DICTIONAIRIES for each sold item, then send a REPORT DICTIONARY with all those INDIVIDUAL DICTIOINARIES inside of it...
# To the output... also the user can request a report.txt file.. and we need to be able to make that, too...
# Woof.

# Now let's think bottom-up. We have a time-series of sold items. When we loop through the things we sold,
# We need to create INDIVIDUAL DICTIONARIES the FIRST TIME
# We come across a NOVEL item (something we haven't sold before). 

# If the item sold is NOT something we sell, then the user needs to update the menu (or fire a waiter)

# Because the MENU could be large (think Applebee's), we don't need to loop through the entire menu to find a sold item;
# As soon as we find a sold item that EQUALS(==) a menu item, we can stop searching.

# So for the first time an item is sold, we're going to run a function called 'match_price_cost_profit' -- tedious but descriptive. 
# After running the function, the next time that same item is sold, our program remembers the PRICE, COST, and PROFIT -- helpful!

# Additionally, this function creates the INDIVIDUAL (nested) DICTIONARY inside of the REPORT DICTIONARY, with the USER-KEYS we'll define later  

def match_price_cost_profit(item_sold, _menu, out_dict, user_keys):
    """extracts price/cost/profit data of a sold item from a menu,
        then creates a nested dictionary inside out_dict with
        user_keys """
    # Adding this boolean keeps us from looping through the whole list if we find a matching item:
    update_done = False    
    # loop through the lists stored in _menu:
    for item in _menu:
        # Find a menu item name that matches the sold item name (the item name on the menu is the first element in the row):
        if item_sold == item[0] and not update_done:
            # create a nested dict in out_dict (the report we will end up printing),
            # add price, cost, and profit to make report calculations easier:
            out_dict[item_sold] = {}
            out_dict[item_sold]["--price"]= float(item[-2]) #The second to last element in the item list is the PRICE
            out_dict[item_sold]["--cost"]= float(item[-1]) #The last item in the item list is the COST
            out_dict[item_sold]["--profit"]= float(out_dict[item_sold]["--price"] - out_dict[item_sold]["--cost"]) #PRICE-COST = PROFIT
            # create the LIST OF USER KEYS (count,revenue,cogs,profit) inside the INDIVIDUAL DICTIONARY for this item:
            for key in user_keys:
                out_dict[item_sold][key]= 0
            update_done = True # Now we know this NOVEL item is part of the MENU, and we can stop looking for it.

    if update_done == False: # This only happens if the item sold is not on the menu!

        print(f"{item_sold} cannot be found in Menu! Update Menu!")
        sys.exit(1)
    return None

# So now we have containers for all the data we need, IN THE RIGHT PLACE, and we have {price, cost, profit} data for each item.
# However, our REPORT should only include TOTAL revenue, cost, and profit. So we'll use this function to remove those per item values 
# From our INDIVIDUAL DICTIONARY:

def remove_keys(dict,keys_to_remove):
    """Remove a list of keys from dict, return dict"""
    for key in keys_to_remove:
        dict.pop(key)
    return dict

# Aggregate data from CSV files:
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
        # The name of the sale item is the last element in the sale receipt:
        sale_item = sale[-1]
        # The quantity sold is the second to last element in the sale receipt:
        quantity = int(sale[-2])
        # If we've already sold this item, we want to track some data for our REPORT
        if sale_item in report.keys():
            #dict_pointer just points to the correct dictionary (which is a key inside REPORT) inside of this dictionary... very meta
            dict_pointer = report[sale_item]
            dict_pointer["01-count"] += quantity
            dict_pointer["02-revenue"] += dict_pointer["--price"] * quantity
            dict_pointer["03-cogs"] += dict_pointer["--cost"] * quantity
            dict_pointer["04-profit"] += dict_pointer["--profit"] * quantity
        
        else:
            # If we're here, then we haven't sold this item before.
            match_price_cost_profit(sale_item, menu, report, user_keys)

    # Now that we've gathered our report, we can remove the intermediary variables we used for calculation:
    for sales_items in report:
        remove_keys(report[sales_items],["--price","--cost","--profit"])
    
    # If the user wants a report file, we make it for them:
    if report_request:
        with open("report.txt","w") as report_file:
            print(f"Creating report file")
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
 

