from django.http import HttpResponse
from message_queue import tasks

# def test_pub_view(request):
#     tasks.publish_message({'hello': 'world'})
#     return HttpResponse(status=201)