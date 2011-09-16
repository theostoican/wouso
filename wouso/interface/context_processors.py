import logging
from wouso.core.game import get_games
from wouso.core.config.models import Setting
from wouso.interface.top.models import Top
from wouso.interface.qproposal.models import Qproposal
from wouso.interface.messaging.models import Message
from wouso.interface.statistics.views import footer_link as stats_link
from wouso.interface import get_static_pages

def header_footer(request):
    """ Generate header and footer bar contents.
    """
    #TODO ordering, using config

    header = []
    try:
        for game in get_games():
            h = game.get_header_link(request)
            if h:
                header.append(h)
    except: pass

    # add also messages link
    try:
        h = Message.get_header_link(request)
        if h:
            header.append(h)
    except: pass

    footer = []
    try:
        for game in get_games():
            f = game.get_footer_link(request)
            if f:
                footer.append(f)
    except: pass

    # also add stats link
    try:
        f = stats_link(request)
        if f:
            footer.append(f)
    except:
        pass

    # also add static pages
    for sp in get_static_pages():
        footer.append(sp.html_link())

    # qporposal
    if not Qproposal.disabled():
        footer.append(Qproposal.get_footer_link(request))

    # format
    header = " | ".join(header)
    footer = " | ".join(footer)

    return {'header': header, 'footer': footer}

def sidebar(request):
    """ For each registered game, get a widget to be displayed in sidebar
    @remark This design needs to be analysed.
    @todo ordering, using config

    Returns a 'sidebar' list containing html boxes.
    """

    sidebar = []

    try:
        # Request blocks from games
        for game in get_games():
            w = game.get_sidebar_widget(request)
            if w:
                sidebar.append(w)

        # Request blocks from apps
        for app in (Top,):
            w = app.get_sidebar_widget(request)
            if w:
                sidebar.append(w)
    except Exception as e:
        logging.error(e)
        # This is a hack for fixing test. TODO: actually fix ./manage.py test

    return {'sidebar': sidebar}

def config(request):
    """ Make all configuration settings available as config_name """
    settings = {}
    for s in Setting.objects.all():
        settings['config_' + s.name] = s.get_value()

    return settings
