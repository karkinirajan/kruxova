# ********************
# imports python
# ********************
import json

# *****************************************
# IMPORTs django
# *****************************************

# *****************************************
# IMPORTs app
# *****************************************
from apps.event_trail import models as event_trail_models

# Request headers worth keeping in the audit trail. Everything else in request.META (notably the
# Authorization token and Cookie headers, and the whole WSGI environment) is deliberately dropped so
# credentials never end up in the database.
SAFE_META_KEYS = (
    "REMOTE_ADDR",
    "REQUEST_METHOD",
    "PATH_INFO",
    "QUERY_STRING",
    "CONTENT_TYPE",
    "CONTENT_LENGTH",
    "SERVER_NAME",
    "HTTP_HOST",
    "HTTP_USER_AGENT",
    "HTTP_REFERER",
    "HTTP_ORIGIN",
    "HTTP_X_FORWARDED_FOR",
)


def safe_meta(meta):
    return {key: meta[key] for key in SAFE_META_KEYS if key in meta}


class TrailRequests(object):
    def __init__(self, get_response):

        self.get_response = get_response

        # =================================================
        # One-time configuration and initialization.
        # =================================================

    def __call__(self, request):

        # =================================================
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # =================================================

        response = self.get_response(request)

        # =================================================
        # Code to be executed for each request/response after
        # the view is called.
        # =================================================

        if response.streaming:
            """
            not handling streaming
            """
            return response

        if request.method in ["DELETE", "POST", "PUT", "PATCH"]:
            if request.user.is_authenticated:
                # =====================================
                # COMPOSE REQUEST SAVE OBJ
                # =====================================
                new_req = {}
                new_req["route"] = request.get_full_path()
                new_req["method"] = request.method
                new_req["meta"] = safe_meta(request.META)

                # only the names of submitted form fields, never their values (they may be
                # passwords);
                # the query string is already part of "route"
                new_req["form_fields"] = sorted(request.POST.keys())

                # =====================================
                # COMPOSE RESPONSE SAVE OBJ
                # =====================================
                new_res = {}
                new_res["status_code"] = response.status_code

                # =====================================
                # SAVE TRAIL
                # =====================================
                new_trail = event_trail_models.TrailRequest()
                new_trail.user = request.user
                new_trail.method = request.method
                new_trail.request = json.dumps(new_req, default=str)
                new_trail.response = json.dumps(new_res, default=str)
                new_trail.save()

        return response
