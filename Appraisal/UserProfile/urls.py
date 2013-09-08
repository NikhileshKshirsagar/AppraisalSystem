from django.conf.urls import patterns, include, url

urlpatterns = patterns('UserProfile',
    # Examples:
    
    url(r'^CreateUser/$', 'views.CreateUser', name='CreateUser'),
    url(r'^userSearch/$', 'views.userSearch', name='userSerach'),
    url(r'^userInfo/$', 'views.userInfo', name='userInfo'),
    url(r'^UserList/$', 'views.UserList', name='UserList'),
    
    # User(Employee) profile 
    url(r'^profile/$', 'views.userProfile', name='userProfile'),
    
    url(r'^Authenticate/$', 'views.userWelcome', name='userProfile'),
    url(r'^submitAppraisal/$', 'views.submitAppraisal', name='submitAppraisal'),
    url(r'^AppraisalStatus/$', 'views.AppraisalStatus', name='AppraisalStatus'),
    # url(r'^Appraisal/', include('Appraisal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)