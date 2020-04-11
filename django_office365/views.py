from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, authenticate, login as auth_login)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import conf
import msal

flow = msal.ConfidentialClientApplication(
        conf.OFFICE365_CLIENT_ID, authority=conf.AUTHORITY,
        client_credential=conf.OFFICE365_CLIENT_SECRET)


def default_render_failure(request, message, status=403,
                           template_name='office365/failure.html'):
    """Render an error page to the user."""
    data = render_to_string(
        template_name, dict(message=message),
        context_instance=RequestContext(request))
    return HttpResponse(data, status=status)


@csrf_exempt
def login_begin(request, template_name='/login.html',
                domain=None,
                scopes=None,
                redirect_uri=None,
                redirect_field_name=REDIRECT_FIELD_NAME,
                state = None,
                render_failure=default_render_failure):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    request.session['next'] = redirect_to

    if 'error' in request.GET:
        return render_failure(request, 'access_denied')

    try:
        if flow.client_id is None:
            return render_failure(request, 'client_id required')
        if flow.client_credential is None:
            return render_failure(request, 'client_credential required')
        auth_url = flow.get_authorization_request_url(
            conf.SCOPES,
            redirect_uri=conf.OFFICE365_REDIRECT_URI)
        return HttpResponseRedirect(auth_url)
    except Exception:
        return render_failure(request, 'Error')


@csrf_exempt
def login_complete(request, redirect_field_name=REDIRECT_FIELD_NAME,
                   render_failure=default_render_failure):

    redirect_to = request.session.get('next')

    if 'error' in request.GET:
        return render_failure(request, 'access_denied')

    if 'code' not in request.GET:
        return render_failure(request, 'access_denied')

    try:
        code = request.GET.get('code')
        result = flow.acquire_token_by_authorization_code(code, scopes=conf.SCOPES, redirect_uri=conf.OFFICE365_REDIRECT_URI)
        if "error" in result:
            return render_failure(request, 'Error')
        user = authenticate(user_details=result.get("id_token_claims"))
    except Exception:
        return render_failure(request, 'Error')
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            return render_failure(request, 'Disabled account')
    else:
        return render_failure(request, 'Unknown user')


@csrf_exempt
def welcome(request, template_name='office365/welcome.html'):
    c = RequestContext(request, {})
    return render_to_response(template_name, context_instance=c)
