"""hey"""
from __future__ import unicode_literals
import re
import json


def jsonify(data):
    return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))


class ExtractionFunctions:
    def zip(self, s):
        return {'zipcode': s}

    def firstname(self, s):
        return {'firstname': s}

    def lastname(self, s):
        return {'lastname': s}

    def fullname(self, s):
        names = s.rsplit(' ', 1)
        return {
            'firstname': names[0].rstrip(),
            'lastname': names[1].lstrip()
        }

    def phone_dash(self, s):
        return {'phonenumber': s[1:4] + s[5:]}

    def phone_space(self, s):
        s = ''.join(s.split())
        return {'phonenumber': s[0:3]+'-'+s[3:6]+'-'+s[6:]}

    def color(self, s):
        return {'color': s}

extraction_functions = ExtractionFunctions()


PARTIAL_EXPRESSIONS = {
    # Whitespace around commas should be treated as valid
    'comma': r'\s*,\s*',
    'zip': r'\d{5}',
    'firstname': r'[\w .\-]+',
    'lastname': r'[\w\-]+',
    'fullname': r'[\w .\-]+ [\w\-]+',
    'phone_dash': r'\(\d{3}\)-\d{3}-\d{4}',
    'phone_space': r'\d{3}\s*\d{3}\s*\d{4}',
    'color': r'[\w ]+',
}

class ContactFormat():
    def __init__(self, *args):
        # Save this because it's used for both the regular expression
        # and the parsing functions
        self.field_names = tuple(args)

        # Make a pre-regex string of the form:
        # {lastname}{comma}{firstname}{comma}{etc}
        exp = '{' + '}{comma}{'.join(self.field_names) + '}'

        # Pull in the actually regex strings
        exp = exp.format(**PARTIAL_EXPRESSIONS)

        # Allow for leading & trailing whitespace on each line
        exp = r'^\s*' + exp + r'\s*$'

        # Prepare the regex object
        self.regex = re.compile(exp)

    def match(self, contact_string):
        return self.regex.match(contact_string)

    def objectify(self, contact_string):
        values = contact_string.split(',')

        obj = {}
        for i in range(len(self.field_names)):
            extractor = getattr(extraction_functions, self.field_names[i])
            obj.update(extractor(values[i].strip()))

        return obj


VALID_FORMATS = (
    ContactFormat('lastname', 'firstname', 'phone_dash', 'color', 'zip'),
    ContactFormat('fullname', 'color', 'zip', 'phone_space'),
    ContactFormat('firstname', 'lastname', 'zip', 'phone_space', 'color'),
)


if __name__ == '__main__':
    entries = []
    errors = []
    f = open('data.in', 'r')
    line_number = 0
    for line in f:
        found_match = False
        for fmt in VALID_FORMATS:
            if fmt.match(line):
                found_match = True
                entries.append(fmt.objectify(line))
                break
        if not found_match:
            errors.append(line_number)
        line_number = line_number + 1
    print jsonify({
        'entries': entries,
        'errors': errors
    })
