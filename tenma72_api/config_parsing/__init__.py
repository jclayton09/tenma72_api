import configparser


class ConfigParsing:
    def __init__(self, file):
        self.config = configparser.ConfigParser()
        self.file_loc = file
        self.config.read(self.file_loc)

    def create_template(self):
        with open(self.file_loc, 'w') as configfile:
            configfile.write("[Settings]\ncom_port = COM3")

    def return_all_headers(self):
        return self.config.sections()

    def return_headers_names(self, header):
        return [name for name in self.config[header]]

    def return_value(self, header, name):
        return self.config[header][name]

    def update_value(self, header, name, value):
        """
        Function to update an existing value
        """
        tmp = {}

        for names in self.config[header]:
            if names != name:
                tmp[names] = self.config[header][names]
            elif names == name:
                tmp[names] = value

        self.config[header] = tmp
        with open(self.file_loc, 'w') as configfile:
            self.config.write(configfile)
