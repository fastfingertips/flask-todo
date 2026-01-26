from flask import request, url_for, redirect

def get_referer_or_default(default='main.index'):
    """Returns the HTTP referer or a default URL."""
    return request.referrer or url_for(default)

def redirect_back(default='main.index'):
    """Redirects back to the previous page or a default route."""
    return redirect(get_referer_or_default(default))
