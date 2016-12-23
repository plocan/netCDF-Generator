class Reader_dictionary(object):
    def __init__(self):
        self.dimensions_dictionary = {}
        self.dimensions_dictionary_plane_text = open("dimensions_dictionary", "r")

    def get_dimensions_dictionary(self):
        for line in self.dimensions_dictionary_plane_text:
            line = line.replace('\n', "")
            (key, value) = line.split(':')
            if value.find(',') != -1:
                value = value.split(',')
            self.dimensions_dictionary[key] = value
        self.dimensions_dictionary_plane_text.close()
        return self.dimensions_dictionary
