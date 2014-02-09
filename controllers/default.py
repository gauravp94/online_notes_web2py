#text editor(if possible)
import datetime
import os
import re
# -*- coding: utf-8 -*-
import time
# this file is released under public domain and you can use without limitations
########################################################################
#								       #
#	    		****Gaurav Parida*******		       #
#			****Aniruddh Kanojia****		       #
#								       #
########################################################################
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


import gluon.contrib.simplejson
@auth.requires_login()
def index():
    """
    example action using the internationalization operator t and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    a=b.split('@')
    d=[]
    for i in range(len(a)):
   	 c=db((db.note.authoris==auth.user.email)&(db.note.title==a[i])).select()
   	 if len(c):
		    d.append(c[0])

    d=sorted(d,key=lambda x: x['title'] )
    e=d
    p=0
    q=0
    r=0
    q1=[]
    r1=[]
    c=db(db.task.authoris==auth.user.email).select()
    d=db(db.friends.tom==auth.user.email).select()
    for i in range(0,len(c)):
	    if c[i]['done']:
	    	p=1
	    else:
	    	if(c[i]['pending'].date()>=datetime.date.today()):
	    		q=1
			q1.append(c[i])
	    	else:
	    		r=1
			r1.append(c[i])
    q1=sorted(q1,key=lambda x: x['tit'] )
    r1=sorted(r1,key=lambda x: x['tit'] )
    response.flash ="Welcome to Notes!"
    return dict(d=d,b=b,a=e,c=c,p=p,q=q,r=r,q1=q1,r1=r1)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/ushowidoprofile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
@auth.requires_login()
def create():
	response.flash='Create Your Notes Here !'
	if session.msg=='NO':
		response.flash='Invalid Title!'
		session.msg='Yes'
	if session.msg=='E':
		response.flash='Please Choose a priority'
		session.msg='Yes'
	form=SQLFORM.factory(
		Field('title','string',label='Title'),
		Field('description','string',label="Short description",requires=IS_NOT_EMPTY()),
		Field('val','text',label='Note',requires=IS_NOT_EMPTY()),
		Field('tags','string',label="Tags"),
		Field('priority',requires=IS_IN_SET(['Private','Public'])))
	if form.process().accepted:
		a=db(db.auth_user.id==auth.user.id).select()
		if form.vars.title in a[0]['notes'].split('@'):
			session.msg='NO'
			redirect(URL('create'))
		if form.vars.priority !='Private' and form.vars.priority !='Public':
		 	session.msg='E'
		 	redirect(URL('create'))
		b=a[0]['notes']+'@'+form.vars.title
		c=form.vars.tags.split(',')
		db(db.auth_user.id==auth.user.id).update(notes=b)
		session.title=form.vars.title
		db.note.insert(priority=form.vars.priority,title=form.vars.title,cd=request.now,md=request.now,description=form.vars.description,val=form.vars.val,tags=form.vars.tags,authoris=auth.user.email)
		for i in range(len(c)):	
		 	db.tags.insert(word=c[i],title=form.vars.title,authoris=auth.user.email)	
		redirect(URL('cr'))
	return dict(form=form)

@auth.requires_login()
def cr():
	message='Want to add Attachments ?'
	return dict(message=message)

@auth.requires_login()
def cratt():
	if session.msg=='A':
		response.flash='Change File Name'
		session.msg='Y'
	title=session.title
	message='Hi'
	a=db((db.att.title==title)&(db.att.usr==auth.user.email)).select()
	form=SQLFORM(db.att,deletable=True,upload=os.path.join(request.folder,'/pic'))
	if request.vars.fil!=None:
		form.vars.nm=request.vars.fil.filename
	if form.process().accepted:
		a=db((db.att.nm==form.vars.nm)&(db.att.usr==auth.user.email)&(db.att.title==session.title)).select()
		if len(a)>0:
			session.msg='A'
			redirect(URL('cratt'))
		db(db.att.fil==form.vars.fil).update(usr=auth.user.email,title=title,nm=form.vars.nm)
		redirect(URL('cratt'))
	return dict(a=a,form=form)
@auth.requires_login()
def show():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	session.title=title
	a=db((db.note.title==title)& (auth.user.email==db.note.authoris)).select()
	tit=a[0]['title']
	val=a[0]['val']
	des=a[0]['description']
	tags=a[0]['tags']
	ct=a[0]['cd']
	mt=a[0]['md']
	pr=a[0]['priority']
	em=a[0]['authoris']
	l=db((db.att.title==title)&(db.att.usr==auth.user.email)).select()
	return dict(title=tit,val=val,des=des,tags=tags,ct=ct,mt=mt,a=a,l=l,pr=pr,em=em)
@auth.requires_login()
def edit():
	if session.message=='NOT':
		response.flash='Invalid Username'
		session.message='Yes'
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	c=db((db.note.title==title)&(db.note.authoris==auth.user.email)).select()
	form=SQLFORM.factory(
		Field('title','string',label='Title',default=c[0]['title']),
		Field('description','string',label='Description',default=c[0]['description']),
		Field('val','text',label='Note',default=c[0]['val'],requires=IS_NOT_EMPTY()),
		Field('tags','string',label='Tags',default=c[0]['tags']),
		Field('priority',requires=IS_IN_SET(['Public','Private'])))
	if form.process().accepted:
		c=form.vars.tags.split(',')
		a=db(db.note.title==form.vars.title).select()
		if len(a)==1 and a[0]['title']!=title:
			session.message='NOT'
			redirect(URL('edit',args=title))
		db((db.tags.title==title)&(db.tags.authoris==auth.user.email)).delete()
		for i in range(len(c)):	
		 	db.tags.insert(word=c[i],title=form.vars.title,authoris=auth.user.email)	
		
		db((db.note.title==title)&(auth.user.email==db.note.authoris)).update(title=form.vars.title,md=request.now,description=form.vars.description,val=form.vars.val,tags=form.vars.tags,priority=form.vars.priority)
		a=db(db.auth_user.id==auth.user.id).select()
		a=a[0]['notes']
		b=a.split('@')
		a=''
		for i in range(1,len(b)):
			if b[i].strip()==title.strip():
				b[i]=form.vars.title
			a+='@'+b[i]
		db(db.auth_user.id==auth.user.id).update(notes=a)
		redirect(URL('show',args=form.vars.title))
	return dict(form=form)
@auth.requires_login()
def edshow():
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    response.flash = "You can edit notes here!"
    return dict(b=b,a=[])
@auth.requires_login()
def eddel():
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    response.flash = "Are you sure ?"
    return dict(b=b,a=[])
@auth.requires_login()
def shdel():
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	return dict(title=title)
@auth.requires_login()
def delet():
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	db((db.note.title==title)&(db.note.authoris==auth.user.email)).delete()
	db((db.tags.title==title)&(db.tags.authoris==auth.user.email)).delete()
	db((db.att.usr==auth.user.email)&(db.att.title==title)).delete()
	a=db(db.auth_user.id==auth.user.id).select()
	a=a[0]['notes']
	b=a.split('@')
	a=''
	for i in range(1,len(b)):
		if b[i].strip()==title.strip():
			continue
		a+='@'+b[i]
	db(db.auth_user.id==auth.user.id).update(notes=a)
	redirect(URL('index'))
	return dict(form=form)
@auth.requires_login()
def searchinp():
	form1=SQLFORM.factory(Field('stime','date',requires=IS_NOT_EMPTY(),label="Start Time"),
			Field('endtime','date',label="End Time"),table_name="1000")
	form2=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()),table_name="2")
	form3=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()),table_name="3")
	d=['Search By Title','Search By Tags','Search By Date']
	a=[form2,form3,form1]  
	if form1.accepts(request.vars,session):
		st=form1.vars.stime
		et=form1.vars.endtime
		if et!=None:
			redirect(URL('sdate2',args=(form1.vars.stime,form1.vars.endtime)))
		else:
			redirect(URL('sdate',args=(form1.vars.stime)))
	if form2.accepts(request.vars,session):
		redirect(URL('searchtit',args=form2.vars.Name))
	if form3.accepts(request.vars,session):
		redirect(URL('searchtag',args=form3.vars.Name))
	return dict(a=a,d=d,form2=form2)
@auth.requires_login()
def searchtag():
	a=request.args(0,cast=str).replace('_',' ')
	a=a.replace('_',' ')
        nam=[]
	tit=[]
        name=db(db.tags.id>0).select(db.tags.ALL)
	l=len(name)
	for i in range(len(name)):
		mat=re.search(a,name[i]['word'])
		if mat and name[i]['authoris']==auth.user.email:
			nam.append(name[i])
	return dict(nam=nam)
@auth.requires_login()
def litetag():
	tagname=[]
	notest=[]
	a=db(auth.user.email==db.tags.authoris).select(db.tags.ALL)
	for i in range(len(a)):#if len(a) is zero then tell that there is no tags attached
		if a[i]['word'] not in tagname:
			tagname.append(a[i]['word'])
			tmp=[];
			for j in range(len(a)):
				if a[i]['word']==a[j]['word']:
					tmp.append(a[j]['title'])
			notest.append(tmp)
	return dict(tagname=tagname,notest=notest)

@auth.requires_login()
def searchtit():
	a=request.args(0,cast=str).replace('_',' ')
	a=a.replace('_',' ')
        nam=[]
        name=db(db.note.title>0).select(db.note.ALL)
	l=len(name)
	for i in range(0,l):
		mat=re.search(a,name[i]['title'])
		if mat and name[i]['authoris']==auth.user.email:
			nam.append(name[i])
	return dict(nam=nam)
@auth.requires_login()
def crtask():
	a={}
	response.flash='Create Tasks Here'
	if session.msg=='N':
		response.flash='Invalid Title'
		session.msg='Y'
	elif session.msg=='T':
		response.flash='Invalid Date'
		session.msg='Y'
	form=SQLFORM.factory(
			Field('title','string',label='Title',requires=IS_NOT_EMPTY()),
			Field('des','text',label='Description'),
			Field('pen','date',label='Date'))
	if form.process().accepted:
		a=db((db.task.tit==form.vars.title)&(auth.user.email==db.task.authoris)).select()
		if len(a)>0:
			session.msg='N'
			redirect(URL('crtask'))
		if form.vars.pen<datetime.date.today():
			session.msg='T'
			redirect(URL('crtask'))
		db.task.insert(tit=form.vars.title,description=form.vars.des,pending=form.vars.pen,done=False,authoris=auth.user.email)
#		Inserting For scheduler
		a={}
		a=[auth.user.email,form.vars.title]
		db.scheduler_task.insert(
		application_name='asd/appadmin',
		task_name=form.vars.title+'+'+auth.user.email,
		group_name='main',
		start_time=form.vars.pen+datetime.timedelta(-1),
		stop_time=form.vars.pen,
		status='QUEUED',
		function_name='f',
		enabled=True,
		period=60,
		args=gluon.contrib.simplejson.dumps(a))

		redirect(URL('index'))
	return dict(form=form,a=a)
@auth.requires_login()
def shtask():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	a=db((db.task.tit==title)& (auth.user.email==db.task.authoris)).select()
	tit=a[0]['tit']
	des=a[0]['description']
	return dict(title=tit,description=des,a=a,pending=a[0]['pending'])
@auth.requires_login()
def taskde():
	response.flash='Are You Sure ??'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	return dict(title=title)
@auth.requires_login()
def taskde1():
	response.flash='Are You Sure ??'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	return dict(title=title)

@auth.requires_login()
def taskdel():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db((db.task.tit==title)&(db.task.authoris==auth.user.email)).delete()
	db(db.scheduler_task.task_name==title+'+'+auth.user.email).delete()
	message='Done'
	redirect(URL('index'))
	return (message)
@auth.requires_login()
def taskdel1():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db((db.task.tit==title)&(db.task.authoris==auth.user.email)).delete()
	db(db.scheduler_task.task_name==title+'+'+auth.user.email).delete()
	message='Done'
	redirect(URL('taskshdel'))
	return (message)

@auth.requires_login()
def taskshdel():
	a=db(db.task.authoris==auth.user.email).select()
	return dict(a=a)

def help():
	response.flash='Hi'
	message='In case of doubts contact the developers'
	return dict(message=message)
@auth.requires_login()
def taskedit():
	if session.message=='NOT':
		response.flash='Invalid Username'
		session.message='Yes'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	c=db(db.task.tit==title).select()
	form=SQLFORM.factory(
		Field('title','string',label='Title',default=c[0]['tit']),
		Field('description','text',label='Description',default=c[0]['description'],length=255),
		Field('time','date',default=c[0]['pending']),
		Field('done','boolean',default=c[0]['done']))
	if form.process().accepted:
		a=db(db.task.tit==form.vars.title).select()
		if len(a)==1 and a[0]['tit']!=title:
			session.message='NOT'
			redirect(URL('taskedit',args=title))
		db((db.task.tit==title)&(auth.user.email==db.task.authoris)).update(tit=form.vars.title,description=form.vars.description,pending=form.vars.time,done=form.vars.done)
		
		db(db.scheduler_task.task_name==title+'+'+auth.user.email).delete()
		if(form.vars.done==False):
			a={}
			a=[auth.user.email,form.vars.title]
			db.scheduler_task.insert(
			application_name='asd/appadmin',
			task_name=form.vars.title+'+'+auth.user.email,
			group_name='main',
			start_time=form.vars.time+datetime.timedelta(-1),
			stop_time=form.vars.pen,
			status='QUEUED',
			function_name='f',
			enabled=True,
			period=60,
			args=gluon.contrib.simplejson.dumps(a))


		redirect(URL('shtask',args=form.vars.title))
	return dict(form=form,title=title)
@auth.requires_login()
def taskedit1():
	if session.message=='NOT':
		response.flash='Invalid Username'
		session.message='Yes'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	c=db(db.task.tit==title).select()
	form=SQLFORM.factory(
		Field('title','string',label='Title',default=c[0]['tit']),
		Field('description','string',label='Description',default=c[0]['description']),
		Field('time','date',default=c[0]['pending']),
		Field('done','boolean',default=c[0]['done']))
	if form.process().accepted:
		a=db(db.task.tit==form.vars.title).select()
		if len(a)==1 and a[0]['tit']!=title:
			session.message='NOT'
			redirect(URL('taskedit',args=title))
		db((db.task.tit==title)&(auth.user.email==db.task.authoris)).update(tit=form.vars.title,description=form.vars.description,pending=form.vars.time,done=form.vars.done)
		
		db(db.scheduler_task.task_name==title+'+'+auth.user.email).delete()
		if(form.vars.done==False):
			a={}
			a=[auth.user.email,form.vars.title]
			db.scheduler_task.insert(
			application_name='asd/appadmin',
			task_name=form.vars.title+'+'+auth.user.email,
			group_name='main',
			start_time=form.vars.time+datetime.timedelta(-1),
			stop_time=form.vars.pen,
			status='QUEUED',
			function_name='f',
			enabled=True,
			period=60,
			args=gluon.contrib.simplejson.dumps(a))


		redirect(URL('taskedshow',args=form.vars.title))
	return dict(form=form,title=title)
@auth.requires_login()
def taskedshow():
    a=db(db.task.authoris==auth.user.email).select()
    response.flash = "You can edit tasks here!"
    return dict(a=a)
@auth.requires_login()
def asearchtit():
	form=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()))
	if form.process().accepted:
		redirect(URL('searchtit',args=form.vars.Name))
	return dict(form=form)
@auth.requires_login()
def asearchtag():
	form=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()))
	if form.process().accepted:
		redirect(URL('searchtag',args=form.vars.Name))
	return dict(form=form)

@auth.requires_login()
def today():
	form=SQLFORM.factory(Field('Between','date'))
	a=db(db.task.authoris==auth.user.email).select()
	b=[]
	c=datetime.date.today()
	x='No'
	for i in range(0,len(a)):
		if a[i]['pending'].date()==c:
			b.append(a[i])
			x='Yes'
	return dict(x=x,b=b)
@auth.requires_login()
def attdel():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db(db.att.fil==title).delete()
	redirect(URL('cratt'))
	return()
@auth.requires_login()
def attdel1():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db(db.att.fil==title).delete()
	redirect(URL('show',args=session.title))
	return()
@auth.requires_login()
def asearchdate():
	form=SQLFORM.factory(Field('stime','date',requires=IS_NOT_EMPTY(),label="Start Time"),
			Field('endtime','date',label="End Time"))
	if form.process().accepted:
		st=form.vars.stime
		et=form.vars.endtime
		if et!=None:
			redirect(URL('sdate2',args=(form.vars.stime,form.vars.endtime)))
		else:
			redirect(URL('sdate',args=(form.vars.stime)))
	return dict(form=form)
@auth.requires_login()
def sdate2():
	a=request.args(0,cast=str)
	b=request.args(1,cast=str)
	nam=[]
	nam2=[]
	d=[]
	name=db(db.note.authoris==auth.user.email).select()
	l=len(name)
	for i in range(l):
		if str(name[i]['cd'].date())>=a and str(name[i]['cd'].date())<=b:
			nam.append(name[i])
		if str(name[i]['md'].date())>=a and str(name[i]['md'].date())<=b:
			nam2.append(name[i])
	return dict(nam=nam,nam2=nam2,a=a,b=b)

@auth.requires_login()
def sdate():
	a=request.args(0,cast=str)
	nam=[]
	nam2=[]
	d=[]
	name=db(db.note.authoris==auth.user.email).select()
	l=len(name)
	for i in range(l):
		if str(name[i]['cd'].date())==a:
			nam.append(name[i])
		if str(name[i]['md'].date())==a:
			nam2.append(name[i])
	return dict(nam=nam,nam2=nam2,a=a)
@auth.requires_login()
def ma():
	titl=request.args(0,cast=str).strip()
	titl=titl.replace('_',' ')
	a=db((db.note.authoris==auth.user.email)&(db.note.title==titl)).select()
	mail.send(to=auth.user.email,subject=titl,message='Description : '+str(a[0]['description'])+'\r\n'+'Content : '+str(a[0]['val'])+'\r\n'+'Creation Date : '+str(a[0]['cd'].date())+'\r\n'+'Modification Date : '+str(a[0]['md'].date())+'\r\n'+'Author Is : '+str(auth.user.email))
	redirect(URL('show',args=titl))
	return dict()
def aaa():
	a={}
	a=['aniruddh.kanojia@students.iiit.ac.in']
	db.scheduler_task.insert(
			application_name='notes/appadmin',
			task_name='Task 1',
			group_name='main',
			status='QUEUED',
			function_name='f',
			enabled=True,
			period=60,
			start_time=request.now,
			args=gluon.contrib.simplejson.dumps(a))
@auth.requires_login()
def do_down(filename,content):
	response.headers['Content-Disposition']='attachment;filename='+filename
	response.headers['Content-Type']='txt/csv'
	return content.getvalue()
@auth.requires_login()
def crnote():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	a=db((db.note.title==title)&(db.note.authoris==auth.user.email)).select()
	import cStringIO
	content=cStringIO.StringIO()
	content.write('Title : '+str(title)+'\r\n'+'Description :'+str(a[0]['description'])+'\r\n\n'+str(a[0]['val'])+'\r\n')
	filename=str(request.args(0)+'+'+auth.user.email)
	return do_down(filename,content)
@auth.requires_login()
def crnote2():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	ti=request.args(1,cast=str).strip()
	ti=ti.replace('_',' ')
	a=db((db.note.title==title)&(db.note.authoris==ti)).select()
	import cStringIO
	content=cStringIO.StringIO()
	content.write('Title : '+str(title)+'\r\n'+'Description :'+str(a[0]['description'])+'\r\n\n'+str(a[0]['val'])+'\r\n')
	filename=str(request.args(0)+'+'+auth.user.email)
	return do_down(filename,content)
@auth.requires_login()
def sfriends():#searching for friends
	form=SQLFORM.factory(Field('name','string',label="Name of friend",requires=IS_NOT_EMPTY()))
	if form.process().accepted:
		redirect(URL('friendsearch',args=form.vars.name))
	return dict(form=form)
@auth.requires_login()
def friendsearch():#takes the input from the other function sfriends
	inpname=request.args(0,cast=str).replace('_',' ')
	fin=[]
	p=[]
	q=[]
	a=db(db.auth_user.id>0).select()
	s=db((db.friends.frm==auth.user.email)|(db.friends.tom==auth.user.email)).select()
	for i in range(len(a)):
		mat=re.search(inpname,a[i]['first_name'])
		if mat and a[i]['email']!=auth.user.email and a[i]['email']:
			fin.append(a[i])
			x=db((db.fr.fr1==auth.user.email)&(db.fr.fr2==a[i]['email'])).select()
			if len(x)>0:
				p.append(1)
			else:
				p.append(0)
			y=db((db.fr.fr2==auth.user.email)&(db.fr.fr1==a[i]['email'])).select()
			if len(y)>0:
				q.append(1)
			else:
				q.append(0)
	

	return dict(fin=fin,em=session.email,a=p,b=q,s=s)

@auth.requires_login()
def prof():
	a=request.args(0,cast=str).replace('_',' ')
	b=request.args(1,cast=str).replace('_',' ')
	c=db(db.note.authoris==b).select()
	fin=[]
	for i in range(len(c)):
		fin.append(c[i])
	return dict(a=a,b=b,c=c,fin=fin)
@auth.requires_login()
def friendshow():
	a=request.args(0,cast=int)
	a=db((db.note.id==a)).select()
	tit=a[0]['title']
	val=a[0]['val']
	des=a[0]['description']
	tags=a[0]['tags']
	ct=a[0]['cd']
	mt=a[0]['md']
	pri=a[0]['priority']
	l=db((db.att.title==tit)&(db.att.usr==a[0]['authoris'])).select()
	session.title=tit
	return dict(title=tit,val=val,des=des,pr=pri,tags=tags,ct=ct,mt=mt,a=a,l=l)
@auth.requires_login()
def reqsent():
	a=request.args(0,cast=str).replace('_',' ')
	b=db((db.friends.frm==a) &(db.friends.tom==auth.user.email)).select()
	if len(b)==0:
		db.friends.insert(frm=auth.user.email,tom=a,vali=1)
		x=db(db.auth_user.email==a).select()
		db(db.auth_user.email==a).update(Notifications=x[0]['Notifications']+1)
		message="You have sent a friend request to "+a
	else:
		message="You have already sent the friend request"
	response.flash="Friend Request Sent"
	time.sleep(1)
	redirect(URL('sfriends'))
	return dict(message=message)
@auth.requires_login()
def reqaccept():
	a=request.args(0).replace('_',' ')
	message='NO condition met'
	c=request.args(1,cast=int)
#	db((db.friends.frm==a) &(db.friends.tom==b)&(c==2)).update(vali=2)
	if(c==2):
		db.fr.insert(fr1=auth.user.email,fr2=a)
		db((db.friends.frm==a)&(db.friends.tom==auth.user.email)).delete()
		message="You have accepted the friend request"
	elif(c==3):
		db((db.friends.frm==a)&(db.friends.tom==auth.user.email)).delete()
		message="You have Rejected the friend request"
	return dict(message=message,a=a,c=c)
@auth.requires_login()
def myfr():
	if(session.msg=='X'):
		response.flash="Friend Deleted"
		session.msg='Y'
	a=db((db.fr.fr1==auth.user.email)).select()
	b=db(db.fr.fr2==auth.user.email).select()
	fina=[]
	finb=[]
	for i in range(len(a)):
		x=db(db.auth_user.email==a[i]['fr2']).select()
		if(len(x)):
			fina.append(x[0])
	for i in range(len(b)):
		x=db(db.auth_user.email==b[i]['fr1']).select()
		if(len(x)):
			finb.append(x[0])
	return dict(fina=fina,finb=finb)
@auth.requires_login()
def delask():
	response.flash='Are You Sure ??'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	return dict(title=title)
def delfr():
	a=request.args(0,cast=str).replace('_',' ')
	db((db.fr.fr1==auth.user.email)&(db.fr.fr2==a)).delete()
	db((db.fr.fr2==auth.user.email)&(db.fr.fr1==a)).delete()
	session.msg='X'
	redirect(URL('myfr'))
	return dict()
@auth.requires_login()
def edit1():
	if session.message=='NOT':
		response.flash='Invalid Username'
		session.message='Yes'
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	c=db((db.note.title==title)&(db.note.authoris==auth.user.email)).select()
	form=SQLFORM.factory(
		Field('title','string',label='Title',default=c[0]['title']),
		Field('description','string',label='Description',default=c[0]['description']),
		Field('val','text',label='Note',default=c[0]['val'],requires=IS_NOT_EMPTY()),
		Field('tags','string',label='Tags',default=c[0]['tags']))
	if form.process().accepted:
		c=form.vars.tags.split(',')
		a=db(db.note.title==form.vars.title).select()
		if len(a)==1 and a[0]['title']!=title:
			session.message='NOT'
			redirect(URL('edit',args=title))
		db((db.tags.title==title)&(db.tags.authoris==auth.user.email)).delete()
		for i in range(len(c)):	
		 	db.tags.insert(word=c[i],title=form.vars.title,authoris=auth.user.email)	
		
		db((db.note.title==title)&(auth.user.email==db.note.authoris)).update(title=form.vars.title,md=request.now,description=form.vars.description,val=form.vars.val,tags=form.vars.tags)
		a=db(db.auth_user.id==auth.user.id).select()
		a=a[0]['notes']
		b=a.split('@')
		a=''
		for i in range(1,len(b)):
			if b[i].strip()==title.strip():
				b[i]=form.vars.title
			a+='@'+b[i]
		db(db.auth_user.id==auth.user.id).update(notes=a)
		redirect(URL('edshow',args=form.vars.title))
	return dict(form=form)
@auth.requires_login()
def nshow():
    f=request.args(0,cast=int)
    c=[]
    d=[]
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    a=b.split('@')
    for i in range(len(a)):
   	 c=db((db.note.authoris==auth.user.email)&(db.note.title==a[i])).select()
   	 if len(c):
		    d.append(c[0])
    if(f==1):
    	d=sorted(d,key=lambda x: x['title'] )
    elif(f==2):
    	d=sorted(d,key=lambda x: x['cd'] ,reverse=True)
    elif(f==3):
    	d=sorted(d,key=lambda x: x['md'] ,reverse=True)
    response.flash ="Notes Listing !"
    return dict(d=d,b=b,a=[])
@auth.requires_login()
def searchtit1():
	a=request.vars.inp
	a=str(a)
        nam=[]
        name=db(db.note.title>0).select(db.note.ALL)
	l=len(name)
	for i in range(0,l):
		mat=re.search(a,name[i]['title'])
		if mat and name[i]['authoris']==auth.user.email:
			nam.append(name[i])
	return dict(nam=nam,a=a)
@auth.requires_login()
def didtask():
	a=request.args(0,cast=str).replace('_',' ')
	d=db((db.task.authoris==auth.user.email)&(db.task.tit==a)).update(done=True)
	redirect(URL('tshow',args=1))
	return()
@auth.requires_login()
def tshow():
    f=request.args(0,cast=int)
    a=[]
    b=[]
    status='Expired'
    d=db(db.task.authoris==auth.user.email).select()
    for i in range(len(d)):
	    b=[]
	    if d[i]['done']==True:
	    	status='Done'
	    else:
		if d[i]['pending'].date()<datetime.date.today():
		    status='Expired'
		else :
		    status='Pending'
	    b.append(d[i]['tit'])
	    b.append(status)
	    a.append(b)
    if(f==1):
    	d=sorted(d,key=lambda x: x['tit'] )
	a=sorted(a,key=lambda x: x[0])
    elif(f==2):
    	d=sorted(d,key=lambda x: x['pending'] ,reverse=True)
	a=sorted(a,key=lambda x: x[0])
    elif(f==3):
	a=sorted(a,key=lambda x: x[1])
	[x for (y,x) in sorted(zip(d[1],a))]
    response.flash ="Tasks Listing !"
    return dict(d=d,a=a,x='')
@auth.requires_login()
def ndidtask():
	a=request.args(0,cast=str).replace('_',' ')
	d=db((db.task.authoris==auth.user.email)&(db.task.tit==a)).update(done=False)
	redirect(URL('tshow',args=1))
	return()
@auth.requires_login()
def searchtask():
	form=SQLFORM.factory(Field('stime','date',requires=IS_NOT_EMPTY(),label="Start Time"),
			Field('endtime','date',label="End Time"))
	if form.process().accepted:
		st=form.vars.stime
		et=form.vars.endtime
		if et!=None:
			redirect(URL('taskdate2',args=(form.vars.stime,form.vars.endtime)))
		else:
			redirect(URL('taskdate',args=(form.vars.stime)))
	return dict(form=form)
@auth.requires_login()
def taskdate2():
	a=request.args(0,cast=str)
	b=request.args(1,cast=str)
	nam=[]
	name=db(db.task.authoris==auth.user.email).select()
	l=len(name)
	for i in range(l):
		if str(name[i]['pending'].date())>=a and str(name[i]['pending'].date())<=b:
			nam.append(name[i])
	return dict(nam=nam,a=a,b=b)

@auth.requires_login()
def taskdate():
	a=request.args(0,cast=str)
	nam=[]
	name=db(db.task.authoris==auth.user.email).select()
	l=len(name)
	for i in range(l):
		if str(name[i]['pending'].date())==a:
			nam.append(name[i])
	return dict(nam=nam,a=a)
#@auth.requires_login()
#def makeacopy():
#	tit=request.args(0,cast=str).replace('_',' ')
#	usr=request.args(1,cast=str).replace('_',' ')
#	if session.msg=='NO':
#		response.flash='Invalid Title!'
#		session.msg='Yes'
#	a=db(db.auth_user.id==auth.user.id).select()
#	if tit in a[0]['notes'].split('@'):
#		session.msg='NO'
#		redirect(URL('prof',args=(olda,oldb)))
#	b=a[0]['notes']+'@'+tit
#	c=tag.split(',')
#	db(db.auth_user.id==auth.user.id).update(notes=b)
#	session.title=tit
#	db.note.insert(priority=pr,title=tit,cd=request.now,md=request.now,description=desc,val=val,tags=tag,authoris=auth.user.email)
#	for i in range(len(c)):	
#	 	db.tags.insert(word=c[i],title=tit,authoris=auth.user.email)	
#	redirect(URL('show',args=tit))#make it with attachments alsi
#	return dict(form=form)
@auth.requires_login()
def ma1():
	b=request.args(0,cast=int)
	a=db(db.note.id==b).select()
	mail.send(to=auth.user.email,subject=a[0]['title'],message='Description : '+str(a[0]['description'])+'\r\n'+'Content : '+str(a[0]['val'])+'\r\n'+'Creation Date : '+str(a[0]['cd'].date())+'\r\n'+'Modification Date : '+str(a[0]['md'].date())+'\r\n'+'Author Is : '+str(a[0]['authoris']))
	redirect(URL('prof',args=(a[0]['id'],a[0]['authoris'])))
	return dict()

@auth.requires_login()
def ma():
	titl=request.args(0,cast=str).strip()
	titl=titl.replace('_',' ')
	a=db((db.note.authoris==auth.user.email)&(db.note.title==titl)).select()
	mail.send(to=auth.user.email,subject=titl,message='Description : '+str(a[0]['description'])+'\r\n'+'Content : '+str(a[0]['val'])+'\r\n'+'Creation Date : '+str(a[0]['cd'].date())+'\r\n'+'Modification Date : '+str(a[0]['md'].date())+'\r\n'+'Author Is : '+str(auth.user.email))
	redirect(URL('show',args=titl))
	return dict()
@auth.requires_login()
def noti():
    	d=db(db.friends.tom==auth.user.email).select()
	db(db.auth_user.email==auth.user.email).update(Notifications=0)
	a=[]    
	for i in range(len(d)):
		b=db(db.auth_user.email==d[i]['frm']).select()
		a.append(b[0])
	return dict(d=d,a=a)
@auth.requires_login()
def reqdel():
	a=request.args(0,cast=str)
	a=a.replace('_',' ')
	db((db.friends.frm==auth.user.email)&(db.friends.tom==a)).delete()
	redirect(URL('sfriends'))
	return

#a=db((db.note.title==title)& (auth.user.email==db.note.authoris[1:])).select()
