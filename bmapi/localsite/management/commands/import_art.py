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

    help = "Import a CSV file of art installations"
    option_list = BaseCommand.option_list + (
        make_option('--file', dest='fname',
                    default = '',
                    help='Read installations from file'),
        make_option('--year', dest='year', default=None)
        )

    def handle(self, *args, **options):
        if not 'fname' in options or options['fname'] == '':
            print "I need an art csv file to load"
            sys.exit(1)

        fname = options['fname']
        year = options['year']

        self.import_art(fname, year)

    def import_art(self, fname, default_year):
        reader = csv.reader(open(fname, 'r'))
        keys = {
            'year' : 0,
            'bm_fm_id' : 2,
            'artist' : 3,
            'name' : 6,
            'location' : 7,
            'description' : 9,
            'contact_email' : 10
            }

        artct = 0
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

                name = smart_unicode(row[1], errors='ignore')
                name = name.replace('"', '')
                data['slug'] = slugify(name)

                for key, val in keys.items():
                    data[key] = row[val]

                if 'description' in data:
                    data['description'] = data['description'].replace('', '\n')

                # art locations are "time" and "distance"
                loc = row[keys['location']]
                if loc:
                    loc = loc.replace(" o'clock", '')
                    loc = loc.replace(" o’clock", '')

                    data['location_string'] = loc
                    if ' ' in loc:
                        timestr, distance = row[keys['location']].split(' ',1)
                        if timestr[0] in ['0123456789']:
                            if not ':' in timestr:
                                timestr = '%s:00' % timestr
                            data['time_address'] = timestr
                            distance = distance.split(',')[0]
                        try:
                            data['distance'] = int(distance)
                        except ValueError:
                            pass
                artist = data.get('artist','')
                if len(artist) > 255:
                    suffix = " [and more]"
                    artist = artist[:(255-len(suffix))]
                    pos = artist.rfind(' ')
                    if pos > -1:
                        artist = artist[:pos]
                    artist = "%s%s" % (artist, suffix)
                    data['artist'] = artist




                url = '/api/0.2/%s/art/' % year
                url = sign_url(url, section['authuser'], section['authkey'], seed = "%s%i" % (seed, ix))
                print "Updating ID#%s, Name: %s, Loc: %s" % (data.get('bm_fm_id','---'), data['name'], loc)
                resp, content = remote_json(remote, url, data=data, method='PUT')
                if resp['status'] != '200':
                    print 'error #%s\n%s\ndata: %s' % (resp['status'], content, data)
                    errct += 1
                else:
                    artct += 1
                ix += 1

        print ("done, loaded %i art installations, %i errors" % (artct, errct))

