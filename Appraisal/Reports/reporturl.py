from django.conf.urls import patterns, url

urlpatterns = patterns('Reports',
                url(r'^user/$', 'views.GenerateReports', name='login'),
                url(r'^employee/$', 'views.adminGenerateEmployeeReports', name='login'),
                url(r'^IndividualQuestion/$','views.IndividualQuestionDetails'),
                        )
