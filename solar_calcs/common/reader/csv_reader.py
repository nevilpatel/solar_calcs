import csv

_type_map = {
    'pge_electric': {'_nf': 8, '_hs': 'TYPE'},  # delimiter_char, quote_char, num_of_fields, header string
    'pge_gas': {4, 'NA'}
}


class Reader:
    def __init__(self, filename, map_key, delimiter_char=',', quote_char='"'):
        self._filename = filename
        self._delimiter = delimiter_char
        self._quote = quote_char
        self._mapkey = map_key

    def read(self):
        with open(self._filename, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=self._delimiter, quotechar=self._quote)
            return [row for row in reader if
                    len(row) == _type_map[self._mapkey]['_nf'] and row[0] != _type_map[self._mapkey]['_hs']]
