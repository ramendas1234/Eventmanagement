
from .models import Attendee
class EventLibrary:
	def attendee_delete(ids):
		ids = request.POST["udf1"].split(',')
		for item in ids:
			print(item)
			attendeeObj = Attendee.objects.get(pk=item)
			attendeeObj.delete()
		return 'abc'