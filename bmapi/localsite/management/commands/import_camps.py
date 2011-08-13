# -*- coding: utf-8 -*-
"""
 Command to load art from a CSV
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.encoding import smart_unicode
from optparse import make_option
from playaevents.utilities.unique_id import slugify
from signedauth.models import sign_url
from signedauth.utils import remote_json
import csv
import datetime
import sys
import time

class Command(BaseCommand):

    help = "Import a CSV file of Theme Camps"
    option_list = BaseCommand.option_list + (
        make_option('--file', dest='fname',
                    default = '',
                    help='Read installations from file'),
        make_option('--year', dest='year', default=None),
        make_option('--max', dest='max', default=0,
                    help='Maximum rows to load, 0 = all')
        )

    def handle(self, *args, **options):
        if not 'fname' in options or options['fname'] == '':
            print "I need an art csv file to load"
            sys.exit(1)

        fname = options['fname']
        year = options['year']
        maxct = options['max']

        self.import_camps(fname, year, maxct)

    def import_camps(self, fname, year, maxrows):
        reader = csv.reader(open(fname, 'r'))
        keys = {
            'bm_fm_id' : 0,
            'year' : 1,
            'name' : 3,
            'location' : 4,
            'url' : 5,
            'description' : 8,
            'contact_email' : 14,
            'hometown' : (11,12,13),
            }

        common_misspellings = {
            'Engadgment' : 'Engagement',
            'Engagment' : 'Engagement',
            'Coming out' : 'Coming Out',
            'Inititation' : 'Initiation'
            }

        campct = 0
        errct = 0
        timestamp = datetime.datetime.now()
        timestamp = time.mktime(timestamp.timetuple())
        seed = str(int(timestamp))
        ix = 0
        section = settings.PROXY_DOMAINS['playaevents']
        remote = 'http://%s:%s' % (section['server'], section.get('port',80))

        for row in reader:
            if row:
                data = {}

                year = row[keys['year']]

                name = smart_unicode(row[keys['name']], errors='ignore')
                name = name.replace('"', '')
                data['slug'] = slugify(name)

                for key, val in keys.items():
                    if not key == 'hometown':
                        data[key] = row[val]

                city, state, country = keys['hometown']
                city, state, country = row[city], row[state], row[country]
                home = ""
                for e in (city, state, country):
                    e = e.strip()
                    if e:
                        if home:
                            home = "%s, " % e
                        else:
                            home = e

                if home.endswith(', '):
                    home = home[:-2]
                data['hometown'] = home

                if 'description' in data:
                    data['description'] = data['description'].replace('', '\n')

                # camp locations are "Street" and "Time"
                loc = row[keys['location']]
                if loc:
                    loc = loc.replace(" o'clock", '')
                    loc = loc.replace(" o’clock", '')
                    loc = loc.replace('14','15')

                    data['location_string'] = loc
                    if '&' in loc:
                        street, timestr = loc.split('&',1)

                        street = street.strip()
                        timestr = timestr.strip()
                        if street[0] in '0123456789':
                            # probably reversed
                            t = timestr
                            timestr = street
                            street = t
                        print ('Street = %s Time = %s' % (street, timestr))
                        if str(timestr[0]) in '0123456789':
                            if not ':' in timestr:
                                timestr = '%s:00' % timestr
                            data['time_street_name'] = timestr.split(' ')[0]
                        else:
                            print 'bad time: %s [%s]' % (timestr, timestr[0])
                        for bad, good in common_misspellings.items():
                            if street == bad:
                                street = good
                                loc.replace(bad,good)
                                data['location_string'] = loc
                        data['circular_street_name'] = street

                url = '/api/0.2/%s/camp/' % year
                url = sign_url(url, section['authuser'], section['authkey'], seed = "%s%i" % (seed, ix))
                print "Updating ID#%s, Name: %s, Loc: %s" % (data.get('bm_fm_id','---'), data['name'], loc)
                resp, content = remote_json(remote, url, data=data, method='PUT')
                if resp['status'] != '200':
                    print 'error #%s\n%s\ndata: %s' % (resp['status'], content, data)
                    errct += 1
                else:
                    campct += 1
                ix += 1

            if maxrows > 0 and ix >= maxrows:
                break

        print ("done, loaded %i Camps, %i errors" % (campct, errct))

