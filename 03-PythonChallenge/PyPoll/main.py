# Modules
import os
import csv

# Set path for file
csvpath = os.path.join("election_data.csv")

# Open the CSV
with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    # Assign list to a variable
    my_list = list(csvreader)

    # Removing header row from my list
    my_list.remove(my_list[0])

    # Create Election Results summary list
    results = []

    # Add title to Election Results
    results.append("Election Results")

    # Add separation lines to Election Results
    results.append("-------------------------")

    # Count how many total votes there are
    votes = len(my_list)

    # Add Total Votes to Election Results
    results.append("Total Votes: " + str(votes))

    # Add separation lines to Election Results
    results.append("-------------------------")

    # Start vote counter for each candidate
    Khan = 0
    Correy = 0
    Li = 0
    OTooley = 0

    # Read each row and add 1 to counter for each candidate
    for row in my_list:
        if row[2] == 'Khan':
            Khan += 1
        if row[2] == 'Correy':
            Correy += 1
        if row[2] == 'Li':
            Li += 1
        if row[2] == 'O\'Tooley':
            OTooley += 1

    # Convert decimal to percentage
    kper = (Khan/votes)*100
    cper = (Correy/votes)*100
    lper = (Li/votes)*100
    oper = (OTooley/votes)*100

    # Round percentages to third decimal
    from decimal import Decimal
    kper = Decimal(kper).quantize(Decimal('1e-3'))
    cper = Decimal(cper).quantize(Decimal('1e-3'))
    lper = Decimal(lper).quantize(Decimal('1e-3'))
    oper = Decimal(oper).quantize(Decimal('1e-3'))

    # Add individual candidate results to Election Results
    results.append("Khan: " + str(kper) + "% (" + str(Khan) + ")")
    results.append("Correy: " + str(cper) + "% (" + str(Correy) + ")")
    results.append("Li: " + str(lper) + "% (" + str(Li) + ")")
    results.append("O'Tooley: " + str(oper) + "% (" + str(OTooley) + ")")

    # Add separation lines to Election Results
    results.append("-------------------------")

    # Determine winner
    comparison = [Khan, Correy, Li, OTooley]
    highest = max(comparison)
    if highest == Khan:
        winner = 'Khan'
    elif highest == Correy:
        winner = 'Correy'
    elif highest == Li:
        winner = 'Li'
    elif highest == OTooley:
        winner = 'O\'Tooley'  

    # Add winner to Election Results
    results.append("Winner: " + winner)

    # Add separation lines to Election Results
    results.append("-------------------------")

    # Add Election Results to text file
    with open('electionresults.txt', 'w') as filehandle:  
        for listitem in results:
            filehandle.write('%s\n' % listitem)

    # Print Election Results    
    print(*results, sep = "\n")