#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import datetime
import os.path
import _mysql


IGNORE = ('at', 'on', 'in', 'for', 'by', 'and', 'from', 'of', 'to')
SPACES = map(unicode, (', ', '&', '!', '#', '?', '\'', '%', '$', u'£', '+', '=', '(', ')', '[', ']', '{', '}', '@', '<', '>', '/'))  # . and - must be because of the longitude/latitude
HEADER = ('ORD', 'ORC', 'SBN', 'BNA', 'POB', 'NUM', 'DST', 'STM', 'DDL', 'DLO', 'PTN', 'PCD', 'CTA', 'CTP', 'CTT', 'SCD', 'CAT', 'NDP', 'DPX', 'URN', 'GME', 'GMN', 'LTO', 'LGO', 'LTE', 'LGE', 'WCD', 'WNW', 'WNA', 'NHS', 'NNH', 'PCG', 'PNH', 'PNP')


def main():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'ACPC4517P2.csv'))
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'out.txt'))
    import_csv(path, out)


def import_csv(path, out):
    db = _mysql.connect(
        host="localhost", user="root",
        passwd="", db="locationer")

    db.query('''
        CREATE TABLE IF NOT EXISTS `location_london` (
         id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
         postcode VARCHAR(100) NOT NULL,
         content BLOB NOT NULL,
         INDEX `postcode` (`postcode` ASC)
       ) engine = MyISAM ;
    ''')

    with open(path, 'rb') as fp:
        reader = csv.reader(fp)
        now = datetime.datetime.now()

        query_values = []
        for number, row in enumerate(reader):
            if number == 0:
                continue

            info = dict(zip(HEADER, row))

            if not info['LTE'] or not info['LGE'] or not info['LTO'] or not info['LGO']:
                continue

            # Detect location type
            if info['CAT'] == 'N' and ('hotel' in info['BNA'].lower().split() or 'hotel' in info['ORC'].lower().split()):
                location_type = 'hotel'
            #elif info['CAT'] == 'N' and 'station' in info['BNA'].lower().split():
            #    location_type = 'station'
            elif info['CAT'] == 'N' and 'airport' in info['BNA'].lower().split()[1:]:
                location_type = 'airport'
            else:
                location_type = 'place'

            # Name
            if info['BNA']:
                name = '%s %s' % (info['BNA'], info['SBN'])
            elif info['ORC']:
                name = '%s %s' % (info['ORC'], info['ORD'])
            else:
                name = ''

            # Creates location if it doesn't exist
            data = {
                'name': name.strip(),
                'type': location_type,
                'latitude': float(info['LTE']),
                'longitude': float(info['LGE']),
                'door_number': info['NUM'],
                'street_address': info['STM'],
                'postcode_search': ('%s %s' % (info['PCD'].split()[0], info['PCD'].replace(' ', ''))).lower(),
                'postcode': info['PCD'],
                'town': info['PTN'].capitalize(),
                'last_modified': now.strftime('%Y-%m-%d %H:%M:%S'),
            }

            data['sortable_address'] = ("%s - %s, %s, %s" % (data['name'], data['street_address'], data['door_number'], data['town'])).lower()

            query_values.append('("%s", "%s@@%s@@%s")' % (data['postcode'], data['sortable_address'], data['latitude'], data['longitude']))

            # Output a dot
            if number % 10000 == 0:
                #output.write("".join(locations))
                #locations = []
                query = 'INSERT INTO `location_london` (postcode, content) VALUES %s;' % (','.join(query_values))
                db.query(query)
                query_values = []
                sys.stdout.write("%d (%.2f%%)\n" % (number, (number / 29000000.0 * 100.0)))

        query = 'INSERT INTO `location_london` (postcode, content) VALUES %s;' % (','.join(query_values))
        db.query(query)


if __name__ == '__main__':
    main()
