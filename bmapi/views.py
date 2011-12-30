from django.http import HttpResponse, Http404
from httpproxy import settings
from httpproxy.decorators import normalize_request
from httpproxy.exceptions import UnknownProxyMode
import httplib2
import logging
import urlparse

try:
    parse_qs = urlparse.parse_qs
except AttributeError:
    from cgi import parse_qs


log = logging.getLogger('bmapi.views')

@normalize_request
def smart_proxy(request, proxy_server=None, prefix=None, must_include='/api/'):
    url = request.path
    if must_include and must_include not in url:
        raise Http404('BM API only inludes API urls')

    if 'sig' not in request.GET and 'sig' not in request.POST:
        prefix = None
    else:
        log.debug('sending prefix of "%s" to proxy', prefix)

    return proxy(request, proxy_server=proxy_server, prefix=prefix)

PROXY_FORMAT = u'%s:%d%s'

def proxy(request, proxy_server = None, prefix=None):
    url = request.path
    user = None
    password = None
    if proxy_server is None:
        if hasattr(settings, 'PROXY_DOMAIN'):
            server = settings.PROXY_DOMAIN
            port = getattr(settings, 'PROXY_PORT', 80)
            user = getattr(settings, 'PROXY_USER', None)
            password = getattr(settings, 'PROXY_PASSWORD', None)
        else:
            raise UnknownProxyMode("You must specify the PROXY_DOMAIN in your settings")

    else:
        if hasattr(settings, 'PROXY_DOMAINS'):
            section = settings.PROXY_DOMAINS[proxy_server]
            server = section['server']
            port = section.get('port',80)
            user = section.get('user', None)
            password = section.get('password', None)
        else:
            raise UnknownProxyMode("You must specify the PROXY_DOMAINS in your settings if you are going to use multiple proxied servers.")


    if not server.startswith('http'):
        fmt = 'http://%s' % PROXY_FORMAT

    conn = httplib2.Http()

    # Optionally provide authentication for server
    if user is not None and password is not None:
        conn.add_credentials(user, password)

    if request.method == 'GET':
        ending = request.GET.urlencode()
        if prefix is not None:
            ending = "%s&prefix=%s" % (ending, prefix)
        if ending.startswith('&'):
            ending = ending[1:]
        if ending:
            ending = "?%s" % ending

        url_ending = '%s%s' % (url, ending)
        url = fmt % (server, port, url_ending)
        response, content = conn.request(url, request.method)

    elif request.method == 'DELETE':
        if prefix is not None:
            ending = "?prefix=%s" % (ending, prefix)
            url = "%s%s" % (url, ending)

        url = fmt % (server, port, url)
        response, content = conn.request(url, request.method)

    elif request.method in ('POST', 'PUT'):
        url = fmt % (server, port, url)
        if request.method == 'POST':
            data = request.POST.urlencode()
        else:
            data = request.PUT.urlencode()
        if prefix is not None:
            data = "%s&prefix=%s" % (data, prefix)
        response, content = conn.request(url, request.method, data)

    log.debug('returning proxy request: %s', url);
    return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])
