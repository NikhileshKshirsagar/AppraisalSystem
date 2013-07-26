from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns=patterns('',
                     url(r'^question/', include('Question.questionurls')),
                     url(r'', include('Login.loginurls')),
                     )

urlpatterns += patterns('UserProfile',
    # Examples:
    url(r'^CreateUser/$', 'views.CreateUser', name='CreateUser'),
    url(r'^userSearch/$', 'views.userSearch', name='userSerach'),
    url(r'^userInfo/$', 'views.userInfo', name='userInfo'),
    url(r'^UserList/$', 'views.UserList', name='UserList'),
    url(r'^logout/$', 'views.logout'),
    # url(r'^Appraisal/', include('Appraisal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

