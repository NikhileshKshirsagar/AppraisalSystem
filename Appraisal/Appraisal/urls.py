from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns=patterns('',
                     url(r'^question/', include('Question.questionurls')),
                     url(r'^userprofile/', include('UserProfile.urls')),
                     url(r'^masters/', include('Masters.urls')),
                     url(r'', include('Login.loginurls')),
                     )



