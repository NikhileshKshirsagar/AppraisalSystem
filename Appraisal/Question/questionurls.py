from django.conf.urls import patterns, url

urlpatterns = patterns('Question',
                url(r'^questionCreation/$', 'views.questionCreateView', name='login'),
                url(r'^optionList/$', 'views.OptionList'),
                url(r'^optionDetails/$', 'views.OptionDetails'),
                url(r'^QuestionList/$', 'views.QuestionList'),
                url(r'^validateOptionHeader/$','views.validateOptionHeader'),
                url(r'^updateOption/$','views.updateOption'),
                        )
