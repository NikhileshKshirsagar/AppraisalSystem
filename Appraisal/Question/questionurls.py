from django.conf.urls import patterns, url

urlpatterns = patterns('Question',
                url(r'^questionCreation/$', 'views.questionCreateView', name='login'),
                url(r'^optionList/$', 'views.OptionList'),
                url(r'^optionDetails/$', 'views.OptionDetails'),
                url(r'^QuestionList/$', 'views.QuestionList'),
                url(r'^validateOptionHeader/$','views.validateOptionHeader'),
                url(r'^updateOption/$','views.updateOption'),
                url(r'^deleteQuestion/$','views.deleteQuestion'),
                url(r'^editQuestion/([0-9]+)/$','views.editQuestion'),
                url(r'^([0-9]+)/([a-zA-Z]*?)$','views.QuestionAnswer'),
                url(r'^save/$','views.saveAnswer'),
                        )
