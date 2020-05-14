from django.utils.translation import ugettext_lazy as _


class Errors(object):
    SPORT_ALREADY_EXISTS = _("You have already added this sport")
    ACTION_NOT_ALLOWED = _("You are not allowed to perform this action")


class Success(object):
    UPDATED_SUCCESSFULLY = _("Successfully updated")
    DELETED_SUCCESSFULLY = _("Successfully deleted")
