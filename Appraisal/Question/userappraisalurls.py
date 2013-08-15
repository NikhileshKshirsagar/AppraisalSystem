from django.conf.urls import patterns, url

urlpatterns = patterns('Question',
                url(r'^appraise/([0-9]+)/$','views.userwiseQuestionList'),
                        )
