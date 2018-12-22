# Modules
import os
import csv

# Set path for file
csvpath = os.path.join("budget_data.csv")

# Open the CSV
with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    # Assign list to a variable
    my_list = list(csvreader)

    # Removing header row from my list
    my_list.remove(my_list[0])

    # Create Financial Analysis summary list
    analysis = []

    # Add title to Financial Analysis
    analysis.append("Financial Analysis")

    # Add separation lines to Financial Analysis
    analysis.append("----------------------------")

    # Count how many months are in the list
    months = len(my_list)

    # Add Total Months to Financial Analysis
    analysis.append("Total Months: " + str(months))

    # Sum the profits/losses
    total = 0
    for row in my_list:
        total += int(row[1])
    
    # Add Total to Financial Analysis
    analysis.append("Total: $" + str(total))

    # Calculate the month-to-month change
    for row in my_list:
        revenue = [int(i[1]) for i in my_list] 
    difference = [revenue[i+1]-revenue[i] for i in range(len(revenue)-1)]

    # Calculate the average change
    average = sum(difference) / float(len(difference))
    average = round(average,2)

    # Add Average Change to Financial Analysis
    analysis.append("Average Change: $" + str(average))

    # Combine lists
    difference = [0] + difference
    new_my_list = list(zip(my_list, difference))

    # Determine highest average change
    maximum = max(difference)

    # Determine cooresponding month/yeah of highest average change
    for row in new_my_list:
        if row[1] == maximum:
            maxmonth = row[0][0]
            
    # Add Greatest Increase in Profits to Financial Analysis
    analysis.append("Greatest Increase in Profits: " + maxmonth + " ($" + str(maximum) + ")")

    # Determine lowest average change
    minimum = min(difference)

    # Determine cooresponding month/yeah of lowest average change
    for row in new_my_list:
        if row[1] == minimum:
            minmonth = row[0][0]

    # Add Greatest Decrease in Profits to Financial Analysis
    analysis.append("Greatest Decrease in Profits: " + minmonth + " ($" + str(minimum) + ")")

    # Add Financial Analysis to text file
    with open('financialanalysis.txt', 'w') as filehandle:  
        for listitem in analysis:
            filehandle.write('%s\n' % listitem)

    # Print Election Results    
    print(*analysis, sep = "\n")