from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value, Q
from itertools import chain
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm

@login_required
def feed(request):
    # Utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    
    # Tickets & Reviews (Moi + Suivis + Réponses à mes tickets)
    tickets = Ticket.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    ).annotate(content_type=Value('TICKET', CharField()))
    
    reviews = Review.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user) | Q(ticket__user=request.user)
    ).annotate(content_type=Value('REVIEW', CharField()))
    
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'litrevu/feed.html', {'posts': posts})

@login_required
def subscriptions(request):
    form = UserFollowsForm()
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    
    if request.method == 'POST':
        # Logique pour suivre un utilisateur...
        pass
        
    return render(request, 'litrevu/subscriptions.html', {
        'form': form, 'following': following, 'followers': followers
    })
    
    from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
    return render(request, 'litrevu/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('feed')
    return render(request, 'litrevu/signup.html')

@login_required
def create_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    return render(request, 'litrevu/ticket_form.html', {'form': form})

@login_required
def create_review_no_ticket(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    return render(request, 'litrevu/review_form.html', {
        'ticket_form': ticket_form, 'review_form': review_form
    })

@login_required
def reply_to_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    return render(request, 'litrevu/review_form.html', {
        'review_form': form, 'ticket': ticket
    })

@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')
    reviews = Review.objects.filter(user=request.user).order_by('-time_created')
    return render(request, 'litrevu/posts.html', {
        'tickets': tickets, 'reviews': reviews
    })