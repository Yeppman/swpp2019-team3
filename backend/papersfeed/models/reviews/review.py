"""review.py"""
from django.db import models

from papersfeed.models.base_models import BaseModel
from papersfeed.models.users.user import User
from papersfeed.models.papers.paper import Paper


class Review(BaseModel):
    """Review"""
    # Title
    title = models.CharField(max_length=400, null=False)

    # Text
    text = models.TextField(null=False)

    # Paper
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, default=None, related_name='review_paper')

    # 이메일
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='review_user')

    # 익명
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        """Table Meta"""
        db_table = 'swpp_review'  # Table 이름
        ordering = ['-pk']  # Default Order
