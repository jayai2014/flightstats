# -*- coding: utf-8 -*-
"""
^_^ The first program for Phase 3

Task distribution:
   member | functions to implement
   ----------------------
   Jay     load_routes_data,
           load_airport_city_dict,
           filter_routes
   Lizzy   count_routes_by_city, 
           count_codeshare
   Zerun   load_airline_id_name_dict, 
           count_routes_by_airline,
           count_plane_types
    
"""
##############################################################################
# Library used


##############################################################################
# Constants
AIRPORTS_FILENAME = "airports.dat"
ROUTES_FILENAME = "routes.dat"
AIRLINES_FILENAME = "airlines.dat"

LINE_SEPARATOR = ","
EQUIP_SEPARATOR = " "
USELESS_QUOTE = '"'
BLANK = ''
YES_CODESHARE = 'Y'

TOTAL_ROUTES = 59036 # Statistics from http://openflights.org/
TOTAL_AIRPORTS = 3209
TOTAL_AIRLINES = 531

LOCAL_COUNTRY = "New Zealand"

NO_DEST = 0
YES_SOURCE = 1

##############################################################################
def basic_stats():
    # Filter the data (keep what we need)
    local_airports = load_airport_city_dict(LOCAL_COUNTRY, AIRPORTS_FILENAME)
    n_local_airports = len(local_airports)
    
    routes_data = load_routes_data(ROUTES_FILENAME)
    airlines_dict = load_airline_id_name_dict(AIRLINES_FILENAME)
    
    # Get incoming routes to LOCAL_COUNTRY
    routes_incoming = filter_routes(routes_data, local_airports, NO_DEST)
    # Get outcoming routes from LOCAL_COUNTRY
    routes_outcoming = filter_routes(routes_data, local_airports, YES_SOURCE)

    # Combined together
    all_related_routes = routes_incoming + routes_outcoming
    
    # Number of routes from/to LOCAL_COUNTRY
    n_routes_country = (len(routes_incoming), len(routes_outcoming))
    # Total number of routes from/to LOCAL_COUNTRY
    total_routes_country = n_routes_country[0] + n_routes_country[1]
    
    # Number of routes from/to cities in LOCAL_COUNTRY
    n_routes_cities = count_routes_by_city(all_related_routes, local_airports)
    n_routes_airlines = count_routes_by_airline(all_related_routes, airlines_dict)
    n_codeshare = count_codeshare(all_related_routes)
    # Get plane types with frequencies
    plane_types = count_plane_types(all_related_routes)
    
      
    
    # Preview some results for testing
    print "\nStastistics ======================================================= "
    print "  *AS OF JANUARY 2012"
    print "  Number of airports in %s = %d" % (LOCAL_COUNTRY, n_local_airports)
    print "  Number of air routes from %s to overseas = %d" % (LOCAL_COUNTRY , n_routes_country[0])
    print "  Number of air routes from overseas to %s = %d" % (LOCAL_COUNTRY , n_routes_country[1])
    print "  Number of international air routes from/to %s = %d" % (LOCAL_COUNTRY, total_routes_country)
    print "  Number of codeshare routes among all international routes from/to %s = %d"  % (LOCAL_COUNTRY, n_codeshare)   

    top_show = 15 # Ajust number of results to show here
    print "  Number of international routes from/to %s city (top %d):" % (LOCAL_COUNTRY, top_show)
    print "      %-35s %5s %-5s" % ("CITY", "OUT","IN")
    text_format = "      %-35s %5d %-5d"
    temp = sorted(n_routes_cities.items(), key=lambda x:x[1], reverse=True)
    for i in range(0,min(top_show,len(temp))):
        city = temp[i][0]
        n_out = temp[i][1][0]
        n_in = temp[i][1][1]
        print text_format % (city, n_out, n_in)

    top_show = 10 # Ajust number of results to show here
    print "  Airlines operating most number of routes from/to %s (top %d):" % (LOCAL_COUNTRY, top_show)
    print "      %-35s %5s" % ("AIRLINE", "COUNT")
    text_format = "      %-35s %5d"
    i = 0
    temp = sorted(n_routes_airlines.items(), key=lambda x:x[1], reverse=True)
    for i in range(0,min(top_show,len(temp))):
        print text_format % (temp[i][0], temp[i][1])
   
    top_show = 10 # Ajust number of results to show here
    print "  Aircraft types used for routes from/to %s (top %d):" % (LOCAL_COUNTRY, top_show) 
    print "      %-35s %5s" % ("AIRCRAT TYPE", "COUNT")
    text_format = "      %-35s %5d"
    temp = sorted(plane_types.items(), key=lambda x:x[1], reverse=True)
    for i in range(0,min(top_show,len(temp))):
        print text_format % (temp[i][0], temp[i][1])
        
    print "===================================================================\n "
    return
    
##############################################################################
def load_routes_data(file_name):
# Returns routes data as a list of lines
    f = open(ROUTES_FILENAME, "r")
    routes_data = f.readlines()
    f.close()
    return routes_data
    
##############################################################################
def load_airport_city_dict(country, file_name):
# Returns a airline-id to city name dictionary
# output format = [(Airport ID, City),(...), ...]

    # Load airport data
    f = open(file_name, "r")
    content = f.readlines()
    airports_dict = {}
    for line in content: 
        if country in line:
            vals = line.split(LINE_SEPARATOR) # Split the columns first
            airport_id = vals[0]
            city_name = vals[2].replace(USELESS_QUOTE, BLANK) # Delete quote
            airports_dict[airport_id] = city_name

    f.close()    
    return airports_dict   

##############################################################################
def filter_routes(routes, airports_dict, is_source):
# This function can be called two ways: is_source = YES_SOURCE or NO_DEST

# (1) For is_source = YES_SOURCE:
# Return the filtered routes with condition: 
#  destination airport in country 
#  && source airport NOT in country (i.e. NOT domestic route)

# (2) For is_source = NO_DEST:
# Return the filtered routes with condition: 
#  source airport in country 
#  && destination airport NOT in country (i.e. NOT domestic route)

    if (is_source == YES_SOURCE):
        target_index = 3 # destination airport ID
        check_index = 5 # used to check if the route is internatonal / domestic
    elif (is_source == NO_DEST):
        target_index = 5 # source airport ID
        check_index = 3
        
    output = []
    for route in routes:
        vals = route.split(LINE_SEPARATOR) # Split the columns first
        # Get all Australian airport ids
        airport_ids = airports_dict.keys()
        if (vals[target_index] in airport_ids) and (vals[check_index] not in airport_ids):
            # Current route fullfills the requirement as stated on the top            
            output.append(vals)

    # output format = [['2B','410',AER,2965,KZN,2990,,0,CR2], ...]
    return output
    
##############################################################################
def count_routes_by_city(routes, airports_dict):
# Return a dicationary as in the following format
    # output = {"Melbourne": [15,16], "Sydney": [18,19]}
    # Note: 
    #   This is just an example
    #   15 => number of outcoming routes (from a city in LOCAL_COUNTRY)
    #   16 => number of incoming routes (to a city in LOCAL_COUNTRY)
    
    count_source = 0
    count_destination = 0
    output = {}
    
    for airport_id in airports_dict.keys():
        # Reset counts for current airport
        count_destination = 0
        count_source = 0
        
        for route in routes:
            source_id = route[3] # Source airport id of the current route
            dest_id = route[5] # Destination airport id of the current route
            if airport_id == source_id:
                count_destination += 1        
            if airport_id == dest_id:
                count_source += 1

        city_name = airports_dict.get(airport_id)
        
        # Add count to output
        if city_name in output:
            output[city_name][0] += count_source
            output[city_name][1] += count_destination
        elif count_source > 0 or count_destination > 0:
            output[city_name] = [count_source, count_destination]
            
    return output

##############################################################################
def count_codeshare(routes):
# Return a integer => number of codeshare airlines from/to LOCAL_COUNTRY
    airlines_list = []
    count = 0
    for route in routes:
        # route[6] is codeshare
        # routes[1] is airline ID
        if route[6] == YES_CODESHARE and route[1] not in airlines_list:
            # A codeshare route is found
            airlines_list.append(routes[1])
            count += 1
    return count

##############################################################################
def load_airline_id_name_dict(file_name):
# Returns a airline-id to airline-name dictionary
    # output format = {"airline id":"number", ...}   
    
    airlines_dict = {}
    
    f = open(file_name)
    content = f.readlines()
    for line in content:
        line_split = line.split(LINE_SEPARATOR)
        airline_id = line_split[0]
        airline_name = line_split[1].replace(USELESS_QUOTE, BLANK)
        airlines_dict[airline_id] = airline_name
    f.close()
    
    return airlines_dict

##############################################################################
def count_routes_by_airline(routes, airlines_dict):
# Return a dicationary as in the following format  
    # output = {"Qantas Airways": 25, "Virgin Australia": 18}
    # Note: 
    #   This is just an example
    #   Qantas Airways => name of the airline
    #   25 => number of routes from/to Australia opearated by this airline
    
    # airlineid={"id":"number"......}
           
    output = {}

    for route in routes:
        # Get name for the current airline
        airline_id = route[1]   
        airline_name = airlines_dict.get(airline_id)

        # Add count to output
        if airline_name in output:
            output[airline_name] += 1
        else:
            output[airline_name] = 1
    
    return output
    
##############################################################################
def count_plane_types(routes):
# Return a dictionry as in the following format
    # output = {"777": 10, "320": 22}
    # Note:
    #   This is just an example
    #   If there are more than one plane type for one route, count both of them
    
    routes_equips = [] # List of equipment used for each route
    for route in routes:
        curr_equips = route[-1] # Plane types used for current route
        if EQUIP_SEPARATOR not in curr_equips:
            # Only one type of plane
            to_append = [curr_equips]         
        else:
            # More than one type of planes
            to_append = curr_equips.split(EQUIP_SEPARATOR)
        routes_equips.append(to_append)

    spread = []
    # Spread all equips in routes_equips into one single list
    for equips in routes_equips:
         for equip in equips:
             # Remove newline char of the string if there is
             spread.append(equip.rstrip())
                            
    output = {}
    # Count frequency of the plane types
    for curr_equip in spread:
        if curr_equip in output:
           output[curr_equip] += 1
        else:
           output[curr_equip] = 1

    return output

##############################################################################


basic_stats()
