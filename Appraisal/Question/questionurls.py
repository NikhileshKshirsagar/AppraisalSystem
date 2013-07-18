from django.conf.urls import patterns, url

urlpatterns = patterns('Question',
                url(r'^questionCreation/$', 'views.questionCreateView', name='login'),
                        )
