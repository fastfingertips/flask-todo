from flask import request, url_for

def get_referer_or_default(default='main.index'):
    """
    Returns the Referer URL if available, otherwise redirects to a default URL.
    :param default: The default route to redirect to if Referer is not available.
    :return: The Referer URL or the default route URL.
    """
    referer = request.headers.get("Referer")
    if referer:
        return referer
    else:
        return url_for(default)
