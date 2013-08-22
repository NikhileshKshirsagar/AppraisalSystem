from django.conf.urls import patterns, url

urlpatterns = patterns('Reports',
                url(r'^user/$', 'views.GenerateReports', name='login'),
                        )
