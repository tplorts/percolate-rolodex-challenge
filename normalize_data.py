"""
Contact data normalizer
Ted Lorts
2015 April 14

Takes contact data conglomerated in various formats, and
saves a copy of the data in a uniform format.
"""

from __future__ import unicode_literals
import re
import json
from operator import itemgetter


####
# Extraction & Normalization functions
# Each one of these takes the original form of a single field of data
# (with whitespace already trimmed off), and returns an object mapping
# key(s) to normalized value(s)

def extract_fullname(name):
    """
    Split a full name (firstname lastname) into its two (first & last)
    parts. Condenses any groups of varied whitespace into a single
    space.  Allows for multiple names in the firstname.
    """
    names = re.split(r'\s+', name, re.UNICODE)
    return {
        'firstname': ' '.join(names[:-1]),
        'lastname': names[-1]
    }

def extract_phone_space(phone):
    phone = ''.join(phone.split())
    return {'phonenumber': phone[0:3]+'-'+phone[3:6]+'-'+phone[6:]}

EXTRACTION_FUNCTIONS = {
    'zip': lambda s: {'zipcode': s},
    'color': lambda s: {'color': s},
    'firstname': lambda s: {'firstname': s},
    'lastname': lambda s: {'lastname': s},
    'phone_dash': lambda s: {'phonenumber': s[1:4] + s[5:]},
    'fullname': extract_fullname,
    'phone_space': extract_phone_space,
}


####
# Partial Regular Expressions
# Regular expressions that can be chained together to form various
# contact entry format regexs. Each valid form of a field has its
# own key and regex.
PARTIAL_EXPRESSIONS = {
    # Whitespace around commas should be treated as valid
    'comma': r'\s*,\s*',
    'zip': r'\d{5}',
    'firstname': r'[\w \.\-]+',
    'lastname': r'[\w\-]+',
    'fullname': r'[\w \.\-]+ [\w\-]+',
    'phone_dash': r'\(\d{3}\)-\d{3}-\d{4}',
    'phone_space': r'\d{3}\s*\d{3}\s*\d{4}',
    'color': r'[\w ]+',
}





class ContactFormat(object):
    """
    Represents a format of a contact entry
    Create by passing in a list of field names in the order they will
    appear on each line of this particular format.  The field names
    should be one of the keys in PARTIAL_EXPRESSIONS (but not 'comma').
    """

    def __init__(self, *args):
        # Save this because it's used for both the regular expression
        # and the parsing functions
        self.field_names = tuple(args)

        # Make a pre-regex string of the form:
        # {lastname}{comma}{firstname}{comma}{etc}
        self.format_exp = '{' + '}{comma}{'.join(self.field_names) + '}'

        # Pull in the actually regex strings
        exp = self.format_exp.format(**PARTIAL_EXPRESSIONS)

        # Allow for leading & trailing whitespace on each line
        exp = r'^\s*' + exp + r'\s*$'

        # Prepare the regex object
        self.regex = re.compile(exp, re.UNICODE)

    def matches(self, contact_string):
        """whether contact_string fits this format"""
        return self.regex.match(contact_string) != None

    def objectify(self, contact_string):
        """
        Transforms contact_string into an object with values separated
        and normalized
        """
        values = contact_string.split(',')

        obj = {}
        # This loop assumes that self.field_names and values
        # will have equal lengths, since we only use objectify
        # after checking that the string matches this format.
        for i in range(len(self.field_names)):
            extractor = EXTRACTION_FUNCTIONS[self.field_names[i]]
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

    with open('data.in', 'r') as input_file:
        line_number = 0
        for line in input_file:
            # Ignore blank lines
            if len(line.strip()) > 0:
                found_match = False

                # Check each of the supported formats
                for fmt in VALID_FORMATS:
                    if fmt.matches(line):
                        # save the normalized form of this entry
                        entries.append(fmt.objectify(line))
                        # So that this line is not considered erroneous
                        found_match = True
                        # No need to check other formats
                        break

                # if the line matches none of the supported formats
                if not found_match:
                    errors.append(line_number)

            line_number = line_number + 1

    # Sort (in-place) by lastname, then by firstname
    entries.sort(key=itemgetter('lastname', 'firstname'))
    output_object = {
        'entries': entries,
        'errors': errors
    }

    with open('result.out', 'w') as output_file:
        json.dump(output_object, output_file, indent=2,
                  separators=(',', ': '), sort_keys=True)
