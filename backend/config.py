from configparser import ConfigParser

def get_config_params(filename, section):
    parser = ConfigParser()
    parser.read(filename)
    data = {}
    if parser.has_section:
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
        return data
    else:
        raise Exception(f'Section {section} was not found in the {filename} file.')
    
