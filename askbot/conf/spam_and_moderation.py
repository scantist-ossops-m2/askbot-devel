"""Settings for content moderation and spam control"""
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from askbot import const
from livesettings import values as livesettings
from askbot.conf.settings_wrapper import settings
from askbot.conf.super_groups import EXTERNAL_SERVICES

SPAM_AND_MODERATION = livesettings.ConfigurationGroup(
    'SPAM_AND_MODERATION',
    _('Akismet spam protection'),
    super_group=EXTERNAL_SERVICES
)

settings.register(
    livesettings.BooleanValue(
        SPAM_AND_MODERATION,
        'SPAM_FILTER_ENABLED',
        description=_('Enable spam filtering'),
        help_text=_('If enabled, posts classified as spam will be ignored.'),
        default=False
    )
)

if django_settings.ASKBOT_SPAM_CLASSIFIER_FUNCTION == 'askbot.spam_classifiers.akismet_spam_classifier.check_spam':

    # keep this for a while, to allow migration to SPAM_FILTER_ENABLED
    settings.register(
        livesettings.BooleanValue(
            SPAM_AND_MODERATION,
            'USE_AKISMET',
            description=_('Enable Akismet spam detection(keys below are required)'),
            default=False,
            hidden=True,
        )
    )

    settings.register(
        livesettings.StringValue(
            SPAM_AND_MODERATION,
            'AKISMET_API_KEY',
            description=_('Akismet key for spam detection'),
            help_text=_(
                'To get an Akismet key please visit '
                '<a href="%(url)s">Akismet site</a>'
            ) % {'url': const.DEPENDENCY_URLS['akismet']}
        )
    )
