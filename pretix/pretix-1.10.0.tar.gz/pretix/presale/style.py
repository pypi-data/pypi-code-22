import hashlib
import logging
import os
from urllib.parse import urljoin, urlsplit

import django_libsass
import sass
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.dispatch import Signal
from django.templatetags.static import static as _static

from pretix.base.models import Event, Event_SettingsStore, Organizer
from pretix.base.services.async import ProfiledTask
from pretix.celery_app import app
from pretix.multidomain.urlreverse import get_domain

logger = logging.getLogger('pretix.presale.style')
affected_keys = ['primary_font', 'primary_color']


def compile_scss(object, file="main.scss", fonts=True):
    sassdir = os.path.join(settings.STATIC_ROOT, 'pretixpresale/scss')

    def static(path):
        sp = _static(path)
        if not settings.MEDIA_URL.startswith("/") and sp.startswith("/"):
            domain = get_domain(object.organizer if isinstance(object, Event) else object)
            if domain:
                siteurlsplit = urlsplit(settings.SITE_URL)
                if siteurlsplit.port and siteurlsplit.port not in (80, 443):
                    domain = '%s:%d' % (domain, siteurlsplit.port)
                sp = urljoin('%s://%s' % (siteurlsplit.scheme, domain), sp)
            else:
                sp = urljoin(settings.SITE_URL, sp)
        return '"{}"'.format(sp)

    sassrules = []
    if object.settings.get('primary_color'):
        sassrules.append('$brand-primary: {};'.format(object.settings.get('primary_color')))

    font = object.settings.get('primary_font')
    if font != 'Open Sans' and fonts:
        sassrules.append(get_font_stylesheet(font))
        sassrules.append(
            '$font-family-sans-serif: "{}", "Open Sans", "OpenSans", "Helvetica Neue", Helvetica, Arial, sans-serif !default'.format(
                font
            ))

    sassrules.append('@import "{}";'.format(file))

    cf = dict(django_libsass.CUSTOM_FUNCTIONS)
    cf['static'] = static
    css = sass.compile(
        string="\n".join(sassrules),
        include_paths=[sassdir], output_style='compressed',
        custom_functions=cf
    )
    checksum = hashlib.sha1(css.encode('utf-8')).hexdigest()
    return css, checksum


@app.task(base=ProfiledTask)
def regenerate_css(event_id: int):
    event = Event.objects.select_related('organizer').get(pk=event_id)

    # main.scss
    css, checksum = compile_scss(event)
    fname = '{}/{}/presale.{}.css'.format(event.organizer.slug, event.slug, checksum[:16])

    if event.settings.get('presale_css_checksum', '') != checksum:
        newname = default_storage.save(fname, ContentFile(css.encode('utf-8')))
        event.settings.set('presale_css_file', newname)
        event.settings.set('presale_css_checksum', checksum)

    # widget.scss
    css, checksum = compile_scss(event, file='widget.scss', fonts=False)
    fname = '{}/{}/widget.{}.css'.format(event.organizer.slug, event.slug, checksum[:16])

    if event.settings.get('presale_widget_css_checksum', '') != checksum:
        newname = default_storage.save(fname, ContentFile(css.encode('utf-8')))
        event.settings.set('presale_widget_css_file', newname)
        event.settings.set('presale_widget_css_checksum', checksum)


@app.task(base=ProfiledTask)
def regenerate_organizer_css(organizer_id: int):
    organizer = Organizer.objects.get(pk=organizer_id)

    # main.scss
    css, checksum = compile_scss(organizer)
    fname = '{}/presale.{}.css'.format(organizer.slug, checksum[:16])
    if organizer.settings.get('presale_css_checksum', '') != checksum:
        newname = default_storage.save(fname, ContentFile(css.encode('utf-8')))
        organizer.settings.set('presale_css_file', newname)
        organizer.settings.set('presale_css_checksum', checksum)

    # widget.scss
    css, checksum = compile_scss(organizer)
    fname = '{}/widget.{}.css'.format(organizer.slug, checksum[:16])
    if organizer.settings.get('presale_widget_css_checksum', '') != checksum:
        newname = default_storage.save(fname, ContentFile(css.encode('utf-8')))
        organizer.settings.set('presale_widget_css_file', newname)
        organizer.settings.set('presale_widget_css_checksum', checksum)

    non_inherited_events = set(Event_SettingsStore.objects.filter(
        object__organizer=organizer, key__in=affected_keys
    ).values_list('object_id', flat=True))
    for event in organizer.events.all():
        if event.pk not in non_inherited_events:
            regenerate_css.apply_async(args=(event.pk,))


register_fonts = Signal()
"""
Return a dictionaries of the following structure. Paths should be relative to static root.

{
    "font name": {
        "regular": {
            "truetype": "….ttf",
            "woff": "…",
            "woff2": "…"
        },
        "bold": {
            ...
        },
        "italic": {
            ...
        },
        "bolditalic": {
            ...
        }
    }
}
"""


def get_fonts():
    f = {}
    for recv, value in register_fonts.send(0):
        f.update(value)
    return f


def get_font_stylesheet(font_name):
    stylesheet = []
    font = get_fonts()[font_name]
    for sty, formats in font.items():
        stylesheet.append('@font-face { ')
        stylesheet.append('font-family: "{}";'.format(font_name))
        if sty in ("italic", "bolditalic"):
            stylesheet.append("font-style: italic;")
        else:
            stylesheet.append("font-style: normal;")
        if sty in ("bold", "bolditalic"):
            stylesheet.append("font-weight: bold;")
        else:
            stylesheet.append("font-weight: normal;")

        srcs = []
        if "woff2" in formats:
            srcs.append("url(static('{}')) format('woff2')".format(formats['woff2']))
        if "woff" in formats:
            srcs.append("url(static('{}')) format('woff')".format(formats['woff']))
        if "truetype" in formats:
            srcs.append("url(static('{}')) format('truetype')".format(formats['truetype']))
        stylesheet.append("src: {};".format(", ".join(srcs)))
        stylesheet.append("}")
    return "\n".join(stylesheet)
