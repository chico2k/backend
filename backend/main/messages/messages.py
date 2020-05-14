from django.utils.translation import ugettext_lazy as _


class Errors(object):
    ACTION_NOT_ALLOWED = _("You are not allowed to perform this action")
    EXPERIENCES_TO_DATE_NOT_LATER_FROM_DATE = _("To Date should be equal or smaller than From Date")


class Success(object):
    UPDATED_SUCCESSFULLY = _("Successfully updated")
    DELETED_SUCCESSFULLY = _("Successfully deleted")
