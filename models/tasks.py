def ma(*a):
	import datetime
	mail.send(a[0],subject='Your Task '+a[1]+' is pending!!',message='You Have Tasks Pending')
	return
from gluon.scheduler import Scheduler
scheduler=Scheduler(db,dict(f=ma))
