
# def country_dictionary():
#     print "in the function"
#     """opening country text file with list of country names
#     and mapping of where is is located on D3 map"""
#     country_file = open("country_map_list.txt")
#     print "open the file"
#     # created empty dictionary
#     d3_dict = {}
#     # iterate over text file by line by line and split on empty space
#     # add value at 0 index to dictionary and value at index 1 to dictionary
#     # return dicitonary
#     for line in country_file:
#         d3 = line.rstrip()
#         d3 = line.split(" ")

#         print d3
#         d3[d3[0]] = d3[1]

#     return d3_dict



def country_dictionary():
    print "in the function"
    """opening country text file with list of country names
    and mapping of where is is located on D3 map"""
    country_file = open("d3states.txt")
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

    return d3_dict