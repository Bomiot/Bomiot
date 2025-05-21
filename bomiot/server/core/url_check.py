

def url_ignore():
    """
    return a list of urls that should be ignored by the middleware
    """
    admin_urls = [
        '/admin/', '/admin/login/', '/admin/logout/', '/admin/password_change/', '/admin/password_change/done/',
        '/admin/autocomplete/', '/admin/jsi18n/', '/admin/r/<int:content_type_id>/<path:object_id>/',
        '/admin/auth/group/', '/admin/auth/group/add/', '/admin/auth/group/<path:object_id>/history/',
        '/admin/auth/group/<path:object_id>/delete/', '/admin/auth/group/<path:object_id>/change/',
        '/admin/auth/group/<path:object_id>/', '/admin/django_apscheduler/djangojob/',
        '/admin/django_apscheduler/djangojob/add/', '/admin/django_apscheduler/djangojob/<path:object_id>/history/',
        '/admin/django_apscheduler/djangojob/<path:object_id>/delete/', '/admin/django_apscheduler/djangojob/<path:object_id>/change/',
        '/admin/django_apscheduler/djangojob/<path:object_id>/', '/admin/django_apscheduler/djangojobexecution/',
        '/admin/django_apscheduler/djangojobexecution/add/', '/admin/django_apscheduler/djangojobexecution/<path:object_id>/history/',
        '/admin/django_apscheduler/djangojobexecution/<path:object_id>/delete/', '/admin/django_apscheduler/djangojobexecution/<path:object_id>/change/',
        '/admin/django_apscheduler/djangojobexecution/<path:object_id>/', '/admin/core/user/<id>/password/',
        '/admin/core/user/', '/admin/core/user/add/', '/admin/core/user/<path:object_id>/history/',
        '/admin/core/user/<path:object_id>/delete/', '/admin/core/user/<path:object_id>/change/',
        '/admin/core/user/<path:object_id>/', '/admin/(?P<app_label>auth|django_apscheduler|core)/', '/admin/(?P<url>.*)'
    ]

    public_urls = [
        '/', '/login/', '/logout/', '/register/', '/checktoken/', '/favicon.ico'
    ]

    static_urls = [
        '/css/.*', '/js/.*', '/assets/.*', '/statics/.*', '/fonts/.*', '/icons/.*',
        '/static/(?P<path>.*)', '/media/(?P<path>.*)'
    ]

    # Add any other URLs that should be ignored by the middleware
    return admin_urls + public_urls + static_urls