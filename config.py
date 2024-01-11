
# ConfigParser class for ini style configuration file
from configparser import ConfigParser

# function w/ filename and file section parameter
def config(filename='database.ini', section='postgresql'):
    # create parser object
    parser = ConfigParser()
    # read configuration file and load contents to memory
    parser.read(filename)
    
    
    # create empty dictionary
    db = {}
    # check section exist
    if parser.has_section(section):
        # parameters object
        params = parser.items(section)
        # loop parameter key (name) and value pairs 
        for param in params:
            # add parameter name and value pair to dictionary
            db[param[0]] = param[1]
    else:
        # exception handleing, print section missing
        raise Exception('Section {} not found in file: {}'.format(section, filename))
    
    #return dictionary with configuration settings    
    return db


