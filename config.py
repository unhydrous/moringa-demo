import ConfigParser

def parseSection(section, dict1):
    options = parser.options(section)
    for option in options:
        try:
            dict1[option] = parser.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None

def ConfigSectionMap():
    section = parser.get('Global', 'section')
    dict1   = {'section' : section}
    
    if section == 'Development':
	parseSection('Production', dict1)
	parseSection('Staging', dict1)
        parseSection('Development', dict1)

    elif section == 'Staging':
	parseSection('Production', dict1)
	parseSection('Staging', dict1)
    
    elif section == 'Production':
	parseSection('Production', dict1)
    else:
	raise Exception('Unknown config section %s' % section)

    return dict1

parser = ConfigParser.ConfigParser()
parser.optionxform=str
parser.read("/opt/domains/demo.africastalking.com/config.ini")

Config = ConfigSectionMap()
