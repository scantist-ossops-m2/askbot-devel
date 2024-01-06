"""Askbot analytics views"""
from django.conf import settings as django_settings
from django.shortcuts import render
from askbot.models import User

def analytics_index(request):
    """analytics home page"""
    return render(request, 'analytics/index.html')


def analytics_users(request):
    """User analytics page"""
    data = {'all_users_count': User.objects.exclude(askbot_profile__status='b').count(),
            'non_admins_count': 10, #get_non_admins_count(),
            'non_admins_slice_name': django_settings.ANALYTICS_NON_ADMINS_SLICE_NAME,
            'non_admins_slice_description': django_settings.ANALYTICS_NON_ADMINS_SLICE_DESCRIPTION}
    if django_settings.ANALYTICS_EMAIL_DOMAIN_ORGANIZATIONS_ENABLED:
        data['orgs_count'] = 15 #get_organizations_count()
        data['orgs_enabled'] = True
    return render(request, 'analytics/users.html', data)
