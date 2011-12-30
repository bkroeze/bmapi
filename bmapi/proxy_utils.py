from django.conf import settings

def proxy_url(key):
    """Constructs and returns a fully formed url for the given server key,
    as specified in the PROXY_DOMAIN setting."""

    section = settings.PROXY_DOMAINS[key]
    port = section.get('port',80)

    if port != 80:
        remote = 'http://%s:%s' % (section['server'], port)
    else:
        remote = 'http://%s' % (section['server'],)

    return remote
