from django.shortcuts import render, get_object_or_404
from core.models import Post, Comment, ReplyComment, FriendRequest, Notification, ChatMessage
import shortuuid
from accounts.models import Account, Profile
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.db.models import Q, Count, Sum, F, FloatField
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Notifications Keys
noti_new_like = "New Like"
noti_new_follower = "New Follower"
noti_friend_request = "Friend Request"
noti_new_comment = "New Comment"
noti_comment_liked = "Comment Liked"
noti_comment_replied = "Comment Replied"
noti_friend_request_accepted = "Friend Request Accepted"

@login_required
def index(request):
    posts = Post.objects.filter(active=True, visibility="Everyone").order_by("-id")
    
    context = {
        "posts":posts,
    }
    return render(request, "core/index.html", context)


@login_required
def post_detail(request, slug):
    post = Post.objects.get(slug=slug, active=True, visibility="Everyone")
    context = {"post":post}
    return render(request, "core/post-detail.html", context)


def send_notification(user, sender, post, comment, notification_type):
    notification = Notification.objects.create(
        user=user, 
        sender=sender, 
        post=post, 
        comment=comment, 
        notification_type=notification_type
    )
    return notification

@login_required
def mark_notification_as_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        "status": "success"
    })

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(title=title, image=image, visibility=visibility, user=request.user, slug=slugify(title) + "-" + str(uniqueid.lower()))
            post.save()
      
            return JsonResponse({'post': {
                'title': post.title,
                'image_url': post.image.url,
                "full_name":post.user.profile.full_name,
                "profile_image":post.user.profile.image.url,
                "date":timesince(post.date),
                "id":post.id,
            }})
        else:
            return JsonResponse({'error': 'Invalid post data'})

    return JsonResponse({"data":"Sent"})


@login_required
def get_post_data(request):
    id = request.GET.get("id")

    try:
        post = Post.objects.get(id=id, user=request.user)

        data = {
            "id": post.id,
            "title": post.title,
            "visibility": post.visibility,
            "image_url": post.image.url if post.image else "",
        }

        return JsonResponse(data)

    except Post.DoesNotExist:
        return JsonResponse({
            "error": "Post not found"
        }, status=404)



@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        title = request.POST.get("edit-post-caption")
        visibility = request.POST.get("edit-visibility")
        image = request.FILES.get("edit-post-thumbnail")

        try:
            post = Post.objects.get(id=post_id, user=request.user)

            post.title = title
            post.visibility = visibility

            if image:
                post.image = image

            post.save()

            return JsonResponse({
                "status": "success",
                "post": {
                    "id": post.id,
                    "title": post.title,
                    "image_url": post.image.url,
                    "visibility": post.visibility,
                }
            })

        except Post.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Post not found"
            })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    })

@login_required
def delete_post(request):
    post_id = request.GET.get("id")

    try:
        post = Post.objects.get(id=post_id, user=request.user)
        post.delete()

        return JsonResponse({
            "status": "success",
            "message": "Post deleted successfully"
        })

    except Post.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Post not found"
        })

def like_post(request):
    id = request.GET['id'] 
    post = Post.objects.get(id=id)
    user = request.user
    bool = False

    if user in post.likes.all():
        post.likes.remove(user)
        bool = False
    else:
        post.likes.add(user)
        bool = True

        if post.user != request.user:
            send_notification(post.user, user, post, None, noti_new_like)

    data = {
        "bool":bool,
        'likes':post.likes.all().count()
    }
    return JsonResponse({"data":data})


@csrf_exempt
def comment_on_post(request):

    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user

    new_comment = Comment.objects.create(
        post=post,
        comment=comment,
        user=user
    )

    if new_comment.user != post.user:
        send_notification(post.user, user, post, new_comment, noti_new_comment)

    data = {
        "bool":True,
        'comment':new_comment.comment,
        "profile_image":new_comment.user.profile.image.url,
        "date":timesince(new_comment.date),
        "comment_id":new_comment.id,
        "post_id":new_comment.post.id,
        "comment_count":comment_count + int(1)
    }
    return JsonResponse({"data":data})


@csrf_exempt
def like_comment(request):

    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False 

    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True 

        if comment.user != user:
            send_notification(comment.user, user, comment.post, comment, noti_comment_liked)

    data = {
        "bool":bool,
        'likes':comment.likes.all().count()
    }
    return JsonResponse({"data":data})


@csrf_exempt
def reply_comment(request):

    id = request.GET['id']
    reply = request.GET['reply']

    comment = Comment.objects.get(id=id)
    user = request.user

    new_reply = ReplyComment.objects.create(
        comment=comment,
        reply=reply,
        user=user
    )

    if comment.user != user:
        send_notification(comment.user, user, comment.post, comment, noti_comment_replied)

    data = {
        "bool":True,
        'reply':new_reply.reply,
        "profile_image":new_reply.user.profile.image.url,
        "date":timesince(new_reply.date),
        "reply_id":new_reply.id,
        "post_id":new_reply.comment.post.id,
    }
    return JsonResponse({"data":data})


@csrf_exempt
def delete_comment(request):
    id = request.GET['id']
    
    comment = Comment.objects.get(id=id, user=request.user)
    comment.delete()

    data = {
        "bool":True,
    }
    return JsonResponse({"data":data})


@csrf_exempt
@login_required
def add_friend(request):
    sender = request.user
    receiver_id = request.GET.get('id') 

    bool = False

    if sender.id == int(receiver_id):
        return JsonResponse({'error': 'You cannot send a friend request to yourself.'})
    
    receiver = Account.objects.get(id=receiver_id)
    
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        
        return JsonResponse({'error': 'Cancelled', 'bool':bool})
    
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True

        send_notification(
            user=receiver,
            sender=sender,
            post=None,
            comment=None,
            notification_type="Friend Request"
        )

        return JsonResponse({'success': 'Sent',  'bool':bool})


@csrf_exempt
def accept_friend_request(request):
    id = request.GET['id'] 

    receiver = request.user
    sender = Account.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()

    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)

    friend_request.delete()

    send_notification(sender, receiver, None, None, noti_friend_request_accepted)

    data = {
        "message":"Accepted",
        "bool":True,
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
def reject_friend_request(request):
    id = request.GET['id'] 

    receiver = request.user
    sender = Account.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
    friend_request.delete()

    data = {
        "message":"Rejected",
        "bool":True,
    }
    return JsonResponse({'data': data})


@csrf_exempt
def unfriend(request):
    sender = request.user
    friend_id = request.GET['id'] 
    bool = False

    if sender.id == int(friend_id):
        return JsonResponse({'error': 'You cannot unfriend yourself, wait a minute how did you even send yourself a friend request?.'})
    
    my_friend = Account.objects.get(id=friend_id)
    
    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        bool = True
        return JsonResponse({'success': 'Unfriend Successfull',  'bool':bool})


@login_required
def inbox(request):
    user_id = request.user
    chat_message = ChatMessage.objects.filter(     
        id__in =  Subquery(
            Account.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id") 
        )
    ).order_by("-id")
    
    context = {
        'chat_message': chat_message,
    }
    return render(request, 'chat/inbox.html', context)


@login_required
def inbox_detail(request, username):
    user_id = request.user
    message_list = ChatMessage.objects.filter(
        id__in =  Subquery(
            Account.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")
    
    sender = request.user
    receiver = get_object_or_404(Account, username=username)
    receiver_details = receiver

    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, reciever=receiver) | Q(sender=receiver, reciever=sender)
    ).order_by("date")

    messages_detail.update(is_read=True)
    
    if messages_detail.exists():
        r = messages_detail.first()
        reciever = r.reciever
    else:
        reciever = receiver

    context = {
        'message_detail': messages_detail,
        "reciever":reciever,
        "sender":sender,
        "receiver_details":receiver_details,
        "message_list":message_list,
    }
    return render(request, 'chat/inbox_detail.html', context)

@login_required
def block_user(request):
    id = request.GET['id']
    user = request.user
    friend = Account.objects.get(id=id)

    if user.id == friend.id:
        return JsonResponse({'error': 'You cannot block yourself'})


    if friend in user.profile.friends.all():
        user.profile.blocked.add(friend)
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
    else:
        return JsonResponse({'error': 'You cannot block someone that is not your friend'})

    return JsonResponse({'success': 'User Blocked'})
    