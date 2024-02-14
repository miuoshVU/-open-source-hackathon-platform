
from django.http import HttpResponse
from django.shortcuts import render
from hacker.models import HackerInfo
from default.models import CustomUser, Referer
from django.db.models import Q
from .helper import get_permissions

from .utils import download_csv

import csv
from io import StringIO

from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Create your views here.
def dash(request):
    head_org = request.user.groups.filter(name='head-organizer').exists()

    context = {'head_org': head_org, 'permissions':get_permissions(request.user)}
    return render(request, 'organizers/dashboard.html', context)

def generate_pdf(request, pk):
    user = CustomUser.objects.get(pk=pk)

    data = {
       'first_name': user.first_name,
       'last_name': user.last_name,
       'email': user.email,
       'phone': user.country_code + " " + user.phone,
       'location': user.country + ", " + user.city,
       'project_url': user.project_url,
       'issue_desc': user.issue_desc, 
       'project_info': user.project_info, 
       'project_impact': user.project_impact,
       'contribution_url': user.contribution_url, 
       'feedback': user.feedback, 
       'expertise': user.expertise,
       'interest': user.interest, 
       'team': user.team, 
       'profile_url': user.profile_url, 
       'hackathon': user.hackathon
    }

    template = get_template('organizers/pdf.html')
    html_content = template.render(data)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)

    if not pdf.err:
        result.seek(0)

        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}-{}.pdf"'.format(data['first_name'], data['last_name'])
        return response

    return HttpResponse('Error generating PDF: {}'.format(pdf.err))

# All organizers can see hackers
def display_hackers(request):

    url_parameter = request.GET.get("q")
    if url_parameter:
        checked_in_hackers = HackerInfo.objects.exclude(user__groups__name='checked-in').filter(
            Q(user__first_name__icontains=url_parameter) | Q(user__last_name__icontains=url_parameter) |
            Q(user__email__icontains=url_parameter) | Q(user__is_submitted__icontains=url_parameter) 
        )
    else:
        checked_in_hackers = HackerInfo.objects.exclude(
            user__groups__name='checked-in')

    context = { 
                'checked_in_hackers': checked_in_hackers,
                'permissions':get_permissions(request.user)
               }
    return render(request, 'organizers/hackersdisplay.html', context)


def export_hacker_csv(request):
    data = download_csv(request, CustomUser.objects.only(
                  'first_name', 'last_name', 'email', 'country_code',
                  'phone', 'city', 'country', 'project_url',
                  'issue_desc', 'project_info', 'project_impact',
                  'contribution_url', 'feedback', 'expertise',
                  'interest', 'team', 'profile_url', 'hackathon', 
                  'is_email_verified', 'is_phone_verified', 'joined_discord',
                  'is_submitted'))

    attrs = ['first_name', 'last_name', 'email', 'country_code',
                  'phone', 'city', 'country', 'project_url',
                  'issue_desc', 'project_info', 'project_impact',
                  'contribution_url', 'feedback', 'expertise',
                  'interest', 'team', 'profile_url', 'hackathon', 
                  'is_email_verified', 'is_phone_verified', 'joined_discord',
                  'is_submitted', 'date_joined', 'last_login']
    csv_content = data.content.decode('utf-8') 
    csv_stream = StringIO(csv_content)
    reader = csv.DictReader(csv_stream, delimiter=';')

    selected_data = [{key: row[key] for key in row if key in attrs} for row in reader]

    csv_stream.seek(0)
    reader = csv.reader(csv_stream, delimiter=';')
    header = next(reader)

    new_csv_stream = StringIO()
    writer = csv.DictWriter(new_csv_stream, fieldnames=attrs, delimiter=';')
    writer.writeheader()
    for row in selected_data:
        writer.writerow(row)

    new_csv_stream.seek(0)
    final_csv = new_csv_stream.getvalue()
    final_csv_lines = final_csv.split("\n")
    final_csv = final_csv_lines[0] + "\n" + "\n".join(final_csv_lines[2:])

    response = HttpResponse(final_csv, content_type='text/csv')
    return response

def stats_page(request):
    submission_count = CustomUser.objects.all().filter(is_submitted=True).count()
    register_count = HackerInfo.objects.all().count()

    # -----------------------------------------------------------
    empty = False
    for i in CustomUser.objects.values('country').distinct():
        if i['country'] == '':
            empty = True

    if empty:
        nationalities_count = CustomUser.objects.values('country').distinct().count()-1
    else:
        nationalities_count = CustomUser.objects.values('country').distinct().count()
    
    # -----------------------------------------------------------

    country_counts = {}

    for i in CustomUser.objects.values('country'):
        country_name = i.get('country')
        if country_name:
            if country_name not in country_counts:
                country_counts[country_name] = 1
            else:
                country_counts[country_name] += 1
            
    # -----------------------------------------------------------

    group_by_nationalities = {}
    for country, count in country_counts.items():
        group_by_nationalities[country] = count

    # -----------------------------------------------------------

    source_counts = {}

    for i in Referer.objects.values('click_source'):
        source = i.get('click_source')
        if source:
            if source not in source_counts:
                source_counts[source] = 1
            else:
                source_counts[source] += 1

    # -----------------------------------------------------------

    group_by_sources = {}
    for source, count in source_counts.items():
        group_by_sources[source] = count

    # -----------------------------------------------------------

    source_counts = {}

    for i in CustomUser.objects.values('source'):
        source = i.get('source')
        if source:
            if source not in source_counts:
                source_counts[source] = 1
            else:
                source_counts[source] += 1

    # -----------------------------------------------------------

    group_by_registered_sources = {}
    for source, count in source_counts.items():
        group_by_registered_sources[source] = count

    # -----------------------------------------------------------

    reference_counts = {}

    for i in Referer.objects.values('referer'):
        reference = i.get('referer')
        if reference:
            if reference not in reference_counts:
                reference_counts[reference] = 1
            else:
                reference_counts[reference] += 1

    # -----------------------------------------------------------

    group_by_references = {}
    for reference, count in reference_counts.items():
        group_by_references[reference] = count

    # -----------------------------------------------------------

    group_by_nationalities = dict(sorted(group_by_nationalities.items(), key=lambda x: x[1], reverse=True))
    group_by_sources = dict(sorted(group_by_sources.items(), key=lambda x: x[1], reverse=True))
    group_by_registered_sources = dict(sorted(group_by_registered_sources.items(), key=lambda x: x[1], reverse=True))
    group_by_references = dict(sorted(group_by_references.items(), key=lambda x: x[1], reverse=True))
    # -----------------------------------------------------------

    context = { 
                'submission_count':submission_count,
                'register_count':register_count,
                'nationalities_count':nationalities_count,
                'group_by_nationalities': group_by_nationalities,
                'group_by_sources': group_by_sources,
                'group_by_registered_sources': group_by_registered_sources,
                'group_by_references': group_by_references,
                'permissions':get_permissions(request.user)
    }
    return render(request, 'organizers/statspage.html', context)
