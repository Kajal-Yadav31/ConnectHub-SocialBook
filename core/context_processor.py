from core.models import FriendRequest, Notification, ChatMessage
from accounts.models import Account
from django.db.models import OuterRef, Subquery
from django.db.models import Q, Count, Sum, F, FloatField

def my_context_processor(request):

    try:
        friend_request = FriendRequest.objects.filter(receiver=request.user)
    except:
        friend_request = None

    try:
        notification = Notification.objects.filter(user=request.user)
    except:
        notification = None

    
    return {
        "friend_request":friend_request,
         "notification":notification,
    }

def chat_users(request):
    if request.user.is_authenticated:
        users = Account.objects.exclude(
            username=request.user.username
        )
    else:
        users = []

    return {
        "chat_users": users
    }