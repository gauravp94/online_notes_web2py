# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(SPAN('Home',_style="color:blue"),
                  _class="brand",_href=URL('default','index'))

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
a='Notes'
if auth.user:
	response.menu = [
		(SPAN('Notes',_style="color:white"), False, URL('default', 'nshow',args=1), [
		[CAT(I(_class='icon-pencil'),SPAN(' Create')),False,URL('default','create')],
		[CAT(I(_class='icon-edit'),T(' Edit')),False,URL('default','edshow')],
		[CAT(I(_class='icon-remove'),T(' Delete')),False,URL('default','eddel')],
    		[CAT(I(_class='icon-th-list'),SPAN(' View by Tags',_style="color:black")),False,URL('default','litetag')]]),
   		(SPAN('Tasks',_style="color:white"),False,URL('default','tshow',args=1),[
   	 	[CAT(I(_class='icon-pencil'),T(' Create')),False,URL('default','crtask')],
		[CAT(I(_class='icon-edit'),T(' Edit')),False,URL('default','taskedshow')],
		[CAT(I(_class='icon-remove'),T(' Delete')),False,URL('default','taskshdel')],
		[CAT(I(_class='icon-search'),T(' Search Tasks')),False,URL('default','searchtask')]]),
    		(SPAN('Search Notes',_style="color:white"),False,URL('default','searchinp'),[
    		[CAT(I(_class='icon-font'),T(' By Title')),False,URL('default','asearchtit')],
    		[CAT(I(_class='icon-search'),T(' By Tags')),False,URL('default','asearchtag')],
    		[CAT(I(_class='icon-calendar'),T(' By Date')),False,URL('default','asearchdate')]]),
    		(SPAN('My Friends',_style="color:#9963ff"),False,URL('default','myfr')),
    		(SPAN('Friend Search',_style="color:#9933ff"),False,URL('default','sfriends'))
		]
	x="Friend Requests"
	response.menu+=[
	(SPAN(x,_style="color:#9933ff"),False,URL('default','noti')),
    	(SPAN('Help',_style="color:yellow"),False,URL('default','help'))
	]
else:
	response.menu = [	
    	(SPAN('Help',_style="color:yellow"),False,URL('default','help'))
	]
	a='Notes'



#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

