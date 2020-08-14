from catalog.models import Tickit


from django import template
register = template.Library()
@register.simple_tag
def get_obj(A,pk, attr):
	if A == 'Tickit':
		obj = getattr(Tickit.objects.get(pk=int(pk)), attr)
	if A == 'City':
		obj = getattr(City.objects.get(pk=int(pk)), attr)
	if A == 'Event':
		obj = getattr(Event.objects.get(pk=int(pk)), attr)
	if A == 'Image':
		obj = getattr(Image.objects.get(pk=int(pk)), attr)		

	return obj