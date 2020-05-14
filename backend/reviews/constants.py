from django.utils.translation import ugettext_lazy as _


class Errors(object):
    RATING_OWNER_CANNOT_AUTHOR = _(
        "You cannot add a rating for your own Profile.")
    RATING_AUTHOR_EXISITS = _(
        "You have already rated this Profile.")
    RESPONSE_AUTHOR_EXISITS = _(
        "You have already replied to this Review.")
    RESPONSE_NOT_ALLOWED = _(
        "You are not allowed to Response to this Review"
    )


class Success(object):
    RESPONSE_NO_REVIEWS = _(
        "No Reviews yet."
    )
