
def country_dictionary():
    print "in the function"
    """opening country text file with list of country names
    and mapping of where is is located on D3 map"""
    country_file = open("country_map_list.txt")
    print "open the file"
    # created empty dictionary
    d3_dict = {}
    # iterate over text file by line by line and split on empty space
    # add value at 0 index to dictionary and value at index 1 to dictionary
    # return dicitonary
    for line in country_file:
        d3 = line.rstrip()
        d3 = line.split(" ")

        print d3
        d3[d3[0]] = d3[1]

    return d3_dict




    #open the file and create the CSV after filtering the input file.
def openFile(filename, keyword): #defines the function to open the file. User to pass two variables.

    list = []
    string = ''

    f = open(filename, 'r') #opens the file as a read and places it into the variable 'f'.
    for line in f: #for each line in 'f'.
        if keyword in line: #check to see if the keyword is in the line.
            list.append(line) #add the line to the list.

    print(list) #test.

    for each in list: #filter and clean the info, format the info into a CSV format.
        choppy = each.partition(': ') #split to remove the prefix.
        chunk = choppy[2] #take the good string.
        choppy = chunk.partition(' :') #split to remove the suffix.
        chunk = choppy[0] #take the good string.
        strsplit = chunk.split(' ') #split the string by spaces ' '.
        line = strsplit[0] + ',' + strsplit[1] + ',' + strsplit[2] + ',' + strsplit[3] + ' ' + strsplit[4] + ' ' + strsplit[5] + '\n' #concatenate the strings.

        string = string + line #concatenate each line to create a single string.

    print(string) #test.

    f = open(keyword + '.csv', 'w') #open a file to write.
    f.write(string) #write the string to the file.
    f.close() #close the file.



openFile('russtest.txt', 'cat')
openFile('CRON ENROL LOG 200913.txt', 'field 4')