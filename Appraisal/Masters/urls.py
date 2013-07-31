from django.conf.urls import patterns, include, url

urlpatterns = patterns('Masters',
    # Examples:
    
    url(r'^DataInput/$', 'views.MasterInput', name='CreateUser'),
    url(r'^DataInput/$', 'views.ProjectMasterInput', name='CreateUser'),
    url(r'^DataInput/$', 'views.DesignationMasterInput', name='CreateUser'),
    url(r'^DataInput/$', 'views.LanguageMasterInput', name='CreateUser'),
    url(r'^DataInput/$', 'views.EventMasterInput', name='CreateUser'),
    # url(r'^Appraisal/', include('Appraisal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)