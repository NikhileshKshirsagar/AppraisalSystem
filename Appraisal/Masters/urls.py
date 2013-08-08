from django.conf.urls import patterns, include, url

urlpatterns = patterns('Masters',
    # Examples:
    
    url(r'^DataInput/$', 'views.MasterInput', name='CreateUser'),
    url(r'^ProjectMasterInput/$', 'views.ProjectMasterInput', name='CreateUser'),
    url(r'^DesignationMasterInput/$', 'views.DesignationMasterInput', name='CreateUser'),
    url(r'^LanguageMasterInput/$', 'views.LanguageMasterInput', name='CreateUser'),
    url(r'^EventMasterInput/$', 'views.EventMasterInput', name='CreateUser'),
    url(r'^ProjectInformation/$', 'views.projectInfo', name='projectInfo'),
    # url(r'^Appraisal/', include('Appraisal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)