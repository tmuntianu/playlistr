# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import spotipy
import spotipy.util
import ml
# ---- example index page ----
def index():
    scope = 'user-top-read playlist-modify-public'
    client_id="22afe11d6c9a4302804622924738a872"
    client_secret="f6ab191a59de4b59af13dc44d7ec16c5"
    redirect_uri="http://127.0.0.1:8000/init/default/auth_success"
    oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
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
    if request.vars.code and not session.auth_success:
        code = request.vars.code
        scope = 'user-top-read playlist-modify-public'
        client_id="22afe11d6c9a4302804622924738a872"
        client_secret="f6ab191a59de4b59af13dc44d7ec16c5"
        redirect_uri="http://127.0.0.1:8000/init/default/auth_success"
        oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
        token_info = oauth.get_access_token(code)
        user = db.auth_user(id=auth.user_id)
        user.update_record(sp_auth_token=token_info['access_token'],sp_refresh_token=token_info['refresh_token'])
        session.auth_success = True

    user = db.auth_user(id=auth.user_id)
    owner_email = user.email
    form = SQLFORM(db.sp_group, labels = {'sp_member':'Emails'})

    if form.validate() and form.vars.sp_member:
        for row in db(db.sp_group.sp_owner == owner_email).select():
            row.delete_record()
        db.sp_group.insert(sp_owner=owner_email, sp_member=form.vars.sp_member)
        return redirect(URL('makelist'))

    return dict(form=form)

@auth.requires_login()
def makelist():
    owner_email = db.auth_user(id=auth.user_id).email
    emails = []
    for row in db(db.sp_group.sp_owner == owner_email).select():
        emails = (row.sp_member)
    emails.insert(0, owner_email)
    tokens = []
    for email in emails:
        acct_exists = False
        refr_token = ''
        for row in db(db.auth_user.email == email).select():
            refr_token = row.sp_refresh_token
            acct_exists = True
        if acct_exists:
            scope = 'user-top-read playlist-modify-public'
            client_id="22afe11d6c9a4302804622924738a872"
            client_secret="f6ab191a59de4b59af13dc44d7ec16c5"
            redirect_uri="http://127.0.0.1:8000/init/default/auth_success"
            oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
            new_token = oauth.refresh_access_token(refr_token)
            tokens.append(new_token['access_token'])
    sp_objs = ml.authSpotipy(tokens)
    url = ml.main(sp_objs)
    return dict(url = url)


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
