"""utils.py"""
# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from notifications.signals import notify

from papersfeed import constants
from papersfeed.utils.base_utils import is_parameter_exists, ApiError
from papersfeed.utils.papers.utils import __get_paper_like_count
from papersfeed.models.papers.paper import Paper
from papersfeed.models.papers.paper_like import PaperLike
from papersfeed.utils.reviews.utils import __get_review_like_count
from papersfeed.models.reviews.review import Review
from papersfeed.models.reviews.review_like import ReviewLike
from papersfeed.utils.collections.utils import __get_collection_like_count
from papersfeed.models.collections.collection import Collection
from papersfeed.models.collections.collection_like import CollectionLike
from papersfeed.models.collections.collection_user import CollectionUser
from papersfeed.models.replies.reply import Reply
from papersfeed.models.replies.reply_collection import ReplyCollection
from papersfeed.models.replies.reply_review import ReplyReview
from papersfeed.models.replies.reply_like import ReplyLike
from papersfeed.utils.replies.utils import __get_reply_like_count
from papersfeed.models.users.user import User
from papersfeed.models.subscription.subscription import Subscription
from papersfeed.models.users.user_action import UserAction, USER_ACTION_TYPE


@transaction.atomic
def insert_like_paper(args):
    """Insert Like of Paper"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Paper Id
    paper_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    # Check Paper Id
    if not Paper.objects.filter(id=paper_id).exists():
        raise ApiError(constants.NOT_EXIST_OBJECT)

    # If Not Already Like, Create One
    if not PaperLike.objects.filter(paper_id=paper_id, user_id=request_user.id).exists():
        PaperLike.objects.create(
            paper_id=paper_id,
            user_id=request_user.id,
        )

        # store an action for subscription feed
        try:
            subscription = Subscription.objects.get(
                actor=request_user,
                verb="liked",
                action_object_object_id=paper_id
            )
            subscription.save() # for updating time
        except Subscription.DoesNotExist:
            paper = Paper.objects.get(id=paper_id)
            Subscription.objects.create(
                actor=request_user,
                verb="liked",
                action_object=paper
            )

        # Create action for recommendation
        try:
            obj = UserAction.objects.get(
                user_id=request_user.id,
                paper_id=paper_id,
                type=USER_ACTION_TYPE[1]
                )
            obj.count = obj.count + 1
            obj.save()
        except ObjectDoesNotExist:
            UserAction.objects.create(
                user_id=request_user.id,
                paper_id=paper_id,
                type=USER_ACTION_TYPE[1],
                count=1,
            )

    like_counts = __get_paper_like_count([paper_id], 'paper_id')
    return {constants.LIKES: like_counts[paper_id] if paper_id in like_counts else 0}


@transaction.atomic
def remove_like_paper(args):
    """Remove Like of Paper"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Paper ID
    paper_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    try:
        paper_like = PaperLike.objects.get(paper_id=paper_id, user_id=request_user.id)
    except ObjectDoesNotExist:
        raise ApiError(constants.NOT_EXIST_OBJECT)

    paper_like.delete()

    # Update action count for recommendation
    obj = UserAction.objects.get(
        user_id=request_user.id,
        paper_id=paper_id,
        type=USER_ACTION_TYPE[1]
        )
    obj.count = obj.count - 1
    obj.save()

    like_counts = __get_paper_like_count([paper_id], 'paper_id')
    return {constants.LIKES: like_counts[paper_id] if paper_id in like_counts else 0}


@transaction.atomic
def insert_like_review(args):
    """Insert Like of Review"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Review Id
    review_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    # Check Review Id
    if not Review.objects.filter(id=review_id).exists():
        raise ApiError(constants.NOT_EXIST_OBJECT)

    # If Not Already Like, Create One
    if not ReviewLike.objects.filter(review_id=review_id, user_id=request_user.id).exists():
        review_like = ReviewLike(
            review_id=review_id,
            user_id=request_user.id,
        )
        review_like.save()

        review = Review.objects.get(id=review_id)
        review_author = User.objects.get(id=review.user_id)

        # store an action for subscription feed
        try:
            subscription = Subscription.objects.get(
                actor=request_user,
                verb="liked",
                action_object_object_id=review_id
            )
            subscription.save() # for updating time
        except Subscription.DoesNotExist:
            Subscription.objects.create(
                actor=request_user,
                verb="liked",
                action_object=review
            )

        notify.send(
            request_user,
            recipient=[review_author],
            verb='liked',
            action_object=review_like,
            target=review,
        )

    like_counts = __get_review_like_count([review_id], 'review_id')
    return {constants.LIKES: like_counts[review_id] if review_id in like_counts else 0}


@transaction.atomic
def remove_like_review(args):
    """Remove Like of Review"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Review ID
    review_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    try:
        review_like = ReviewLike.objects.get(review_id=review_id, user_id=request_user.id)
    except ObjectDoesNotExist:
        raise ApiError(constants.NOT_EXIST_OBJECT)

    review_like.delete()

    like_counts = __get_review_like_count([review_id], 'review_id')
    return {constants.LIKES: like_counts[review_id] if review_id in like_counts else 0}


@transaction.atomic
def insert_like_collection(args):
    """Insert Like of Collection"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Collection Id
    collection_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    # Check Collection Id
    if not Collection.objects.filter(id=collection_id).exists():
        raise ApiError(constants.NOT_EXIST_OBJECT)

    # If Not Already Like, Create One
    if not CollectionLike.objects.filter(collection_id=collection_id, user_id=request_user.id).exists():
        collection_like = CollectionLike(
            collection_id=collection_id,
            user_id=request_user.id,
        )
        collection_like.save()

        collection = Collection.objects.get(id=collection_id)

        collection_members = CollectionUser.objects.filter(Q(collection_id=collection_id))
        member_ids = [collection_member.user_id for collection_member in collection_members]
        member_ids = list(set(member_ids))

        members = User.objects.filter(Q(id__in=member_ids))

        # store an action for subscription feed
        try:
            subscription = Subscription.objects.get(
                actor=request_user,
                verb="liked",
                action_object_object_id=collection_id
            )
            subscription.save() # for updating time
        except Subscription.DoesNotExist:
            Subscription.objects.create(
                actor=request_user,
                verb="liked",
                action_object=collection
            )

        notify.send(
            request_user,
            recipient=members,
            verb='liked',
            action_object=collection_like,
            target=collection,
        )

    like_counts = __get_collection_like_count([collection_id], 'collection_id')
    return {constants.LIKES: like_counts[collection_id] if collection_id in like_counts else 0}


@transaction.atomic
def remove_like_collection(args):
    """Remove Like of Collection"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Collection ID
    collection_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    try:
        collection_like = CollectionLike.objects.get(collection_id=collection_id, user_id=request_user.id)
    except ObjectDoesNotExist:
        raise ApiError(constants.NOT_EXIST_OBJECT)

    collection_like.delete()

    like_counts = __get_collection_like_count([collection_id], 'collection_id')
    return {constants.LIKES: like_counts[collection_id] if collection_id in like_counts else 0}


@transaction.atomic
def insert_like_reply(args):
    """Insert Like of Reply"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Reply Id
    reply_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    # Check Reply Id
    if not Reply.objects.filter(id=reply_id).exists():
        raise ApiError(constants.NOT_EXIST_OBJECT)

    # If Not Already Like, Create One
    if not ReplyLike.objects.filter(reply_id=reply_id, user_id=request_user.id).exists():
        ReplyLike.objects.create(
            reply_id=reply_id,
            user_id=request_user.id,
        )

        # send notifications to the author of the reply
        reply = Reply.objects.get(id=reply_id)
        reply_author = User.objects.get(id=reply.user_id)

        # consider target as the object which has the reply, instead of reply object
        try: # assume it is the reply of a collection
            collection_id = ReplyCollection.objects.get(reply_id=reply_id).collection_id
            target = Collection.objects.get(id=collection_id)
        except ObjectDoesNotExist: # maybe it is the reply of a review
            try:
                review_id = ReplyReview.objects.get(reply_id=reply_id).review_id
                target = Review.objects.get(id=review_id)
            except ObjectDoesNotExist:
                raise ApiError(constants.NOT_EXIST_OBJECT)

        notify.send(
            request_user,
            recipient=[reply_author],
            verb='liked your reply of',
            action_object=reply, # reply instead of reply_like
            target=target,
        )

    like_counts = __get_reply_like_count([reply_id], 'reply_id')
    return {constants.LIKES: like_counts[reply_id] if reply_id in like_counts else 0}


@transaction.atomic
def remove_like_reply(args):
    """Remove Like of Reply"""
    is_parameter_exists([
        constants.ID
    ], args)

    # Reply ID
    reply_id = int(args[constants.ID])

    # Request User
    request_user = args[constants.USER]

    try:
        reply_like = ReplyLike.objects.get(reply_id=reply_id, user_id=request_user.id)
    except ObjectDoesNotExist:
        raise ApiError(constants.NOT_EXIST_OBJECT)

    reply_like.delete()

    like_counts = __get_reply_like_count([reply_id], 'reply_id')
    return {constants.LIKES: like_counts[reply_id] if reply_id in like_counts else 0}
