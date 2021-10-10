from itertools import chain


from django.db.models import CharField, Value, Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from django.contrib.auth.decorators import login_required
from account.models import UserFollows
from django.core.exceptions import PermissionDenied


# Create your views here.
@login_required(login_url='account/login')
def add_ticket(request):
    """Create a ticket"""
    if request.method == "GET":
        form = TicketForm()
        return render(request, 'review/add_ticket.html', locals())
    elif request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            modif_form = form.save(commit=False)
            modif_form.user = request.user
            modif_form.save()
            return redirect('feed')


@login_required(login_url='account/login')
def edit_ticket(request, id_ticket):
    """Modify a ticket"""
    ticket = Ticket.objects.get(pk=id_ticket)
    if ticket.user == request.user:
        form = TicketForm(instance=ticket)
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                modif_form = form.save(commit=False)
                modif_form.user = request.user
                modif_form.save()
                return redirect('feed')
        return render(request, 'review/edit_ticket.html', locals())
    elif ticket.user != request.user:
        raise PermissionDenied


@login_required(login_url='account/login')
def delete_ticket(request, id_ticket):
    """Delete a ticket"""
    ticket = get_object_or_404(Ticket, pk=id_ticket)
    if ticket.user == request.user:
        ticket.delete()
        return redirect('my_posts')
    elif ticket.user != request.user:
        raise PermissionDenied


@login_required(login_url='account/login')
def add_ticket_and_review(request):
    """Create a ticket and a review"""
    if request.method == "GET":
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, 'review/add_ticket_and_review.html', locals())

    elif request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            modif_ticket_form = ticket_form.save(commit=False)
            modif_ticket_form.user = request.user
            modif_ticket_form.save()
            modif_review_form = review_form.save(commit=False)
            modif_review_form.ticket = modif_ticket_form
            modif_review_form.rating = request.POST.get('rating')
            modif_review_form.user = request.user
            modif_review_form.save()
            return redirect('feed')


@login_required(login_url='account/login')
def add_review(request, id_ticket):
    """Create a review"""
    ticket = Ticket.objects.get(pk=id_ticket)
    if request.method == "GET":
        form = ReviewForm()
        return render(request, 'review/add_review.html', locals())

    elif request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            modif_form = form.save(commit=False)
            modif_form.ticket = ticket
            modif_form.user = request.user
            modif_form.rating = request.POST.get('rating')
            modif_form.save()
            ticket.save()
            return redirect('feed')


@login_required(login_url='account/login')
def edit_review(request, id_review):
    """Modify a review"""
    review = Review.objects.get(pk=id_review)
    if review.user == request.user:
        form = ReviewForm(instance=review)
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                modif_form = form.save(commit=False)
                modif_form.rating = request.POST.get('rating')
                modif_form.save()
                return redirect('feed')
        return render(request, 'review/edit_review.html', locals())
    elif review.user != request.user:
        raise PermissionDenied


@login_required(login_url='account/login')
def delete_review(request, id_review):
    """Delete a review"""
    review = get_object_or_404(Review, pk=id_review)
    if review.user == request.user:
        review.delete()
        return redirect('my_posts')
    else:
        raise PermissionDenied


@login_required(login_url='account/login')
def my_posts(request):
    """Show my tickets and my reviews"""
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    star_rating = range(5)
    # combine and sort the two types of posts
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'review/my_posts.html', locals())


@login_required(login_url='account/login')
def feed(request):
    """Show tickets and reviews of myself and of my followed users"""
    star_rating = range(5)
    users = []
    user_follows = UserFollows.objects.filter(user=request.user)
    for user_follow in user_follows:
        users.append(user_follow.followed_user)
    users.append(request.user)

    # Complex lookups with Q objects
    reviews = Review.objects.filter(Q(user__in=users))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # ticket_with_review = ticket with review already made
    all_reviews = Review.objects.all()
    ticket_with_review = []
    for review in all_reviews:
        ticket_with_review.append(review.ticket)

    tickets = Ticket.objects.filter(Q(user__in=users))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # Combine and sort the two types of posts
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
    return render(request, 'review/feed.html', locals())
