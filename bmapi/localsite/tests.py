from django.conf import settings
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.utils import simplejson
from unittest import skipIf
from bmapi.proxy_utils import proxy_url
from urllib2 import Request, urlopen, URLError, HTTPError
from signedauth.models import sign_url
import imghdr
import logging
import random

log = logging.getLogger('bmapi.tests')

SETUP_MESSAGE = """
In order to test the BM API, you need to be running a %s server.
This can either be the live server, or a development one.
Configure the server you want to use in settings_local under "PROXY_DOMAINS".
"""

ACTIVES = {}
AUTHS = {}
APIS = {
    'playaevents' : '0.2',
    }


def check_active(key):
    """Check that the server named by the key is running"""
    global ACTIVES, AUTHS

    active = False
    domains = settings.PROXY_DOMAINS
    if not key in domains:
        log.warn('No server configured in PROXY_DOMAINS for %s', key)
        active = False

    else:
        section = domains[key]
        if 'authuser' in section and 'authkey' in section:
            AUTHS[key] = (section['authuser'], section['authkey'])
        url = proxy_url(key)
        req = Request(url)
        try:
            urlopen(req)
            active = True
            log.info('Successfully tested connectivity to: %s', url)
        except HTTPError, e:
            log.error('Could not open "%s", got error: %s', url, e.code)
        except URLError, e:
            log.error('Could not open "%s", got error: %s', url, e.reason)

    if not active:
        print SETUP_MESSAGE % key

    ACTIVES[key] = active
    return active

@skipIf(not check_active('playaevents'), "No Playaevents server")
class TestPlayaevents(TestCase):
    def setUp(self):
        self.client = Client()

    def testOne(self):
        log.info('Playaevents active')

    def testCampListNoAuth(self):
        """Test getting an unauthenticated camp list"""
        url = '/events/api/%s/2011/camp/' % APIS['playaevents']
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # use one of the camps to get details
        camps = simplejson.loads(response.content)
        self.assert_(len(camps) > 0)

        camp = random.choice(camps)
        response = self.client.get('%s%i/' % (url, camp['id']))
        self.assertEqual(response.status_code, 200)

        camp2 = simplejson.loads(response.content)

        self.assert_(len(camp2) > 0)
        camp2 = camp2[0]

        keys1 = camp.keys()
        keys2 = camp.keys()
        keys1.sort()
        keys2.sort()

        self.assertEqual(keys1, keys2)

        for key in keys1:
            self.assertEqual(camp[key], camp2[key])

    @skipIf('playaevents' not in AUTHS, 'No authentication key for PlayaEvents')
    def testCampListAuth(self):
        user, key = AUTHS['playaevents']
        seed = random.randint(0,1000000000)
        url = sign_url('/events/api/%s/2011/camp/' % APIS['playaevents'], user, key, seed=str(seed))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # use one of the camps to get details
        camps = simplejson.loads(response.content)
        self.assert_(len(camps) > 0)

        camp = random.choice(camps)
        seed += 1
        url = sign_url('/events/api/%s/2011/camp/%i/' % (APIS['playaevents'], camp['id']), user, key, seed=str(seed))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        camp2 = simplejson.loads(response.content)

        self.assert_(len(camp2) > 0)
        camp2 = camp2[0]

        keys1 = camp.keys()
        keys2 = camp.keys()
        keys1.sort()
        keys2.sort()

        self.assertEqual(keys1, keys2)

        for key in keys1:
            self.assertEqual(camp[key], camp2[key])

@skipIf(not check_active('mediagallery'), "No Media Gallery server")
class TestMediagallery(TestCase):
    def setUp(self):
        self.client = Client()

    def testOne(self):
        log.info('Gallery active')

    def testGetImageNoAuth(self):
        url = '/gallery/api/photos/alesp/alesp.43340/image'

        response = self.client.get(url)
        # 401 = forbidden
        self.assertEqual(response.status_code, 401)

    @skipIf('mediagallery' not in AUTHS, 'No authentication key for MediaGallery')
    def testGetImageAuth(self):
        url = '/gallery/api/photos/alesp/alesp.43340/image'
        user, key = AUTHS['mediagallery']
        seed = random.randint(0,1000000000)

        url = sign_url(url, user, key, seed=str(seed))

        response = self.client.get(url)
        if response.status_code == 401:
            print """Got a forbidden response from the Gallery server, are you sure that you are using the right user & key?
This is set in PROXY_DOMAINS with "authuser" and "authkey".  Currently you have:
user=%s and key=%s""" % (user, key)

        self.assertEqual(response.status_code, 200)
        imgtype = imghdr.what('',response.content)
        self.assertEqual(imgtype, 'jpeg')

    @skipIf('mediagallery' not in AUTHS, 'No authentication key for MediaGallery')
    def testGetImageDetl(self):
        url = '/gallery/api/photos/alesp/alesp.43340/json'
        user, key = AUTHS['mediagallery']
        seed = random.randint(0,1000000000)

        url = sign_url(url, user, key, seed=str(seed))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = simplejson.loads(response.content)
        self.assertEqual(data['status'], 'approved')
        self.assertEqual(data['year'], 2011)
        self.assertEqual(data['title'], 'Gold and Silver Duo')

    @skipIf('mediagallery' not in AUTHS, 'No authentication key for MediaGallery')
    def testGetImageCaption(self):
        url = '/gallery/api/photos/alesp/alesp.43340/caption'
        user, key = AUTHS['mediagallery']
        seed = random.randint(0,1000000000)

        url = sign_url(url, user, key, seed=str(seed))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Gold and Silver Duo')


@skipIf(not check_active('rideshare'), "No Rideshare server")
class TestRideshare(TestCase):
    def setUp(self):
        pass

    def testOne(self):
        log.info('Rideshare active')


