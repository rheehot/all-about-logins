import jwt
import json
import bcrypt
import requests

from datetime import (
    datetime,
    timedelta
)

from django.views           import View
from django.http            import HttpResponse
from django.http            import JsonResponse
from django.core.validators import (
    validate_email,
    ValidationError
)

from config  import (
    SECRET_KEY,
    ALGORITHM
)
from .models import (
    Posting,
    Comment
)

class PostingView(View):
    def get(self, request):
        Posting.objects.all()
        posting_list= [
            {
                'content'       : posting.content,
                'account'       : posting.account.name,
            }
        ]
        return JsonResponse({'comments': comment_list}, status = 200)

    def post(self, request):
        payload  = json.loads(request.body)
        content = payload.get('content', None)
        posting_id = payload.get('posting_id', None)

        account_id = 1

        if content: 
            Comment(
                content = content,
                account_id = account_id,
                posting_id = posting_id,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        missing_key = (
            '\'content\'' * (not content)
        )

        return JsonResponse({'message': 'KEY_ERROR: ' + missing_key}, status = 400)

class CommentsView(View):
    def get(self, request):
        comments = Comment.objects.all().select_related('account').prefetch_related('likecomment_set')
        comment_list = [
            {
                'content'       : comment.content,
                'is_liked'      : comment.likecomment_set.filter(account_id = 1).exists(),
                'account'       : comment.account.email_account,
                'profile_image' : comment.account.profile_image
            } for comment in comments]

        return JsonResponse({'comments': comment_list}, status = 200)

    def post(self, request):
        payload  = json.loads(request.body)
        content  = payload.get('content', None)
        account_id = payload.get('account_id', None)
        posting_id = payload.get('posting_id', None)

        if content: 

            Comment(
                content = content,
                account_id = account_id,
                posting_id = posting_id,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        missing_key = (
            '\'content\'' * (not content)
        )

        return JsonResponse({'message': 'KEY_ERROR: ' + missing_key}, status = 400)

class CommentView(View):
    def delete(self, request, comment_id):
        Comment.objects.get(id = comment_id).delete()
        return JsonResponse({'message': 'DELETED'}, status = 200)
        
