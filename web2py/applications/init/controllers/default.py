# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import spotipy
import spotipy.util

# ---- example index page ----
def index():
    # TODO add scope?
    client_id="22afe11d6c9a4302804622924738a872"
    client_secret="f6ab191a59de4b59af13dc44d7ec16c5"
    redirect_uri="http://127.0.0.1:8000/init/default/auth_success"
    oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri)
    auth_url = oauth.get_authorize_url()
    return dict(auth_url=auth_url, title='Playlistr', message='Welcome to Playlistr!')

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@auth.requires_login()
def auth_success():
    success = 'unsuccessful!'
    if request.vars.code:
        code = request.vars.code
        success = 'successful!'
    return dict(success = success)

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
