from django.utils.translation import ugettext as _


STATUS_CHOICES = ( (0, _('Unknown')),
                   (1, _('Learning')),
                   (100, _('Well-known')),
                   (101, _('Ignored')))

# Number of words where an alert is trigger to archive some texts
MAX_WORDS = 1000