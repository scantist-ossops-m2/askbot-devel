"""Spam checking functions.

NOTE: the main function akismet_check_spam is hotfixed to
use the Askbot spam checker instead

This branch is not meant to be merged anywhere. Use the master branch instead.
"""


import logging
import requests
from akismet import Akismet, APIKeyError, AkismetError
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings
from askbot.conf import settings as askbot_settings
from askbot.utils.html import site_url

def get_user(user, request): #pylint: disable=missing-docstring
    return user or request.user

def get_user_param(user, param_name):
    """Returns param from the user if user is not anonymous.
    Returns `None` otherwise.
    """
    if user.is_anonymous():
        return None
    return getattr(user, param_name)

def akismet_check_spam(text, **kwargs): # pylint: disable=unused-argument
    """A Hack: copy pasted from the master branch!
    Returns True if the text is spam, `kwargs` are ignored.
    If there is an error while calling the spam checker API, it returns False.
    The reason for the latter is that we don't want to block the user from posting.
    If the admin enables the moderation queue, the post will be sent to the queue.
    """
    try:
        api_key = django_settings.ASKBOT_SPAM_CHECKER_API_KEY
        api_url = django_settings.ASKBOT_SPAM_CHECKER_API_URL
        timeout = django_settings.ASKBOT_SPAM_CHECKER_TIMEOUT_SECONDS
        data = {"api_key": api_key, "text": text}
        response = requests.post(api_url, json=data, timeout=timeout)
    except Exception as error: # pylint: disable=broad-except
        logging.critical('Error while calling spam checker API %s', str(error))
        return False

    try:
        if response.status_code == 200:
            return response.json()["spam_score"] > 0.5
    except Exception as error: # pylint: disable=broad-except
        logging.critical('Error while parsing spam checker API response %s', str(error))
        return False

    return False

def akismet_submit_spam(text, request=None, author=None, ip_addr=None, user_agent=None):
    """Submits manually marked spam to Akismet"""
    return call_akismet(text,
                        request=request,
                        author=author,
                        ip_addr=ip_addr,
                        user_agent=user_agent,
                        command='submit_spam')

def call_akismet(text, request=None, author=None, #pylint: disable=too-many-arguments
                 ip_addr=None, user_agent=None, command='check_spam'):
    """Calls akismet apy with a command.
    Supports commands 'check_spam', 'submit_spam' and 'submit_ham'
    """
    if not askbot_settings.USE_AKISMET:
        return False
    try:
        if askbot_settings.AKISMET_API_KEY.strip() == "":
            raise ImproperlyConfigured('You have not set AKISMET_API_KEY')

        data = {'comment_content': text}
        user = get_user(author, request)
        username = get_user_param(user, 'username')
        if username:
            data['comment_author'] = smart_str(username)

        email = get_user_param(user, 'email')
        if email:
            data['comment_author_email'] = email

        api = Akismet(key=askbot_settings.AKISMET_API_KEY,
                      blog_url=smart_str(site_url(reverse('questions'))))

        user_ip = ip_addr or request.META.get('REMOTE_ADDR')
        user_agent = user_agent or request.environ['HTTP_USER_AGENT']
        if command == 'check_spam':
            return api.comment_check(user_ip, user_agent, **data)
        elif command == 'submit_spam':
            return api.submit_spam(user_ip, user_agent, **data)
        elif command == 'submit_ham':
            return api.submit_ham(user_ip, user_agent, **data)
        else:
            raise RuntimeError('unknown akismet method: "{}"'.format(command))

        return api.comment_check(user_ip, user_agent, **data)
    except APIKeyError:
        logging.critical('Akismet Key is missing')
    except AkismetError:
        logging.critical('Akismet error: Invalid Akismet key or Akismet account issue!')
    except Exception as error: # pylint: disable=broad-except
        logging.critical((u'Akismet error: %s' % unicode(error)).encode('utf-8'))
    return False
