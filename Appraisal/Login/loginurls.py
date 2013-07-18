from django.conf.urls import patterns, url

urlpatterns = patterns('Login',
    # Examples:
    url(r'^login/$', 'views.login', name='login'),
    url(r'^welcome/$', 'views.homeScreen', name='login'),
     
     url(r'^logout/$', 'views.logout'),
    # url(r'^Appraisal/', include('Appraisal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)