from actionkit.models import EventCampaign
import chardet
import csv
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from djangohelpers import (rendered_with,
                           allow_http)
from event_uploader.forms import EventForm
from event_uploader.tasks import create_actionkit_event
import io


@allow_http("POST")
def _import_events(request):
    events = []
    has_errors = False

    campaign = None
    if "campaign" in request.POST and request.POST['campaign']:
        try:
            campaign = EventCampaign.objects.using("ak").get(name=request.POST['campaign'].strip())
        except EventCampaign.DoesNotExist:
            messages.error(
                request, 
                _("Campaign %(campaign)s does not exist.") % {
                    'campaign': request.POST['campaign'].strip()})
            has_errors = True
    else:
            messages.error(request, _("You must pick a campaign."))
            has_errors = True
        
        
    for key in request.POST.keys():
        if key.startswith("confirm_"):
            counter = key[len("confirm_"):]
            event_data = dict([
                    (i, request.POST.get("%s_%s" % (i, counter)))
                    for i in
                    "title date time venue address city state zip max_attendees host public_description directions".split()
                    ])
            form = EventForm(data=event_data)
            if form.is_valid():
                event_data['event_struct'] = form.event_struct
                events.append(event_data)
            else:
                has_errors = True
                event_data['errors'] = errors = {}
                errors.update(form.errors)
                events.append(event_data)

    if has_errors:
        campaigns = EventCampaign.objects.using("ak").all()
        return _import_events_preview(request, locals())
        
    for event in events:
        data = event['event_struct']
        data['campaign_id'] = campaign.id

        method = settings.ACTIONKIT_EVENT_UPLOADER_PROCESSING_METHOD
        if method == "sync":
            result = create_actionkit_event(data)
        elif method == "celery-async":
            result = create_actionkit_event.delay(data)
        else:
            raise NotImplementedError("No processing method %s exists." % method)

    if method == "sync":
        messages.success(
            request, 
            _("Successfully imported %(num_events)s events to campaign %(campaign)s -- you can check on the newly created events at %(url)s") % {
                'num_events': len(events),
                'campaign': campaign.name,
                'url': "%s/dash/events/%s" % (settings.ACTIONKIT_API_HOST, campaign.name)})
        return redirect(".")
    elif method == "celery-async":
        messages.info(
            request, 
            _("Now importing %(num_events)s events to campaign %(campaign)s -- check in the Actionkit admin panel at %(url)s to confirm that the import succeeded.") % {
                'num_events': len(events),
                'campaign': campaign.name,
                'url': "%s/dash/events/%s" % (settings.ACTIONKIT_API_HOST, campaign.name)})
        return redirect(".")

@allow_http("GET", "POST")
@rendered_with("event_uploader/import_spreadsheet.html")
def import_events_spreadsheet(request):
    if request.method == "GET":
        return locals()

    if request.POST.get("confirm", None) == "true":
        return _import_events(request)

    events = request.FILES['events']
    contents = events.read()
    try:
        contents = contents.decode("utf8")
        events = io.StringIO(contents, newline=None)
    except UnicodeDecodeError, e:
        messages.warning(request, _('We had some trouble reading the spreadsheet -- be sure to check all values carefully before uploading; some of the text might be mangled.'))
        events = io.StringIO(contents.decode(chardet.detect(contents)['encoding']), newline=None)
    
    reader = csv.reader(events)
    lines = [i for i in reader]
    header_row = lines.pop(0)
    
    events = []
    lineno = 0
    for line in lines:
        lineno += 1
        try:
            events.append(dict(zip(
                        (i.lower().strip().replace(" ", "_") for i in header_row),
                        (i.strip() for i in line)
                        )))
        except Exception, e:
            messages.error(
                request, 
                _('Error reading line %(lineno)s of the spreadsheet: %(error)s') % {
                    'lineno': lineno,
                    'error': str(e)})
            raise
            return redirect(".")

    campaigns = EventCampaign.objects.using("ak").all()
    return _import_events_preview(request, locals())

@rendered_with("event_uploader/import_spreadsheet_preview.html")
def _import_events_preview(request, ctx):
    return ctx
