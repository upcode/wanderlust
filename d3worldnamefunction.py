
def country_dictionary():
    print "in the function"
    """opening country text file with list of country names
    and mapping of where is is located on D3 map"""
    country_file = open("country_map_list.txt")
    print "open the file"
    # created empty dictionary
    countries_name_dictionary = {}
    # iterate over text file by line by line and split on empty space
    # add value at 0 index to dictionary and value at index 1 to dictionary
    # return dicitonary
    for line in country_file:
        line = line.rstrip()
        country = line.split(" ")

        print country
        countries_name_dictionary[country[0]] = country[1]

    return country_dictionary
