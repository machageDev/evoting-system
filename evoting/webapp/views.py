from django.shortcuts import render ,redirect, get_object_or_404
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Candidate, Election, Post, Vote



def home(request):
    return render(request, 'home.html')

def base(request):  # Ensure this function exists
    return render(request, 'base.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "login.html",{"error":"invalid credentials"})
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already exists"})
        User.objects.create_user(username=username,email=email,password=password)
        return redirect("login")
    return render(request,"register.html")

def navbar(request):
    return render(request, 'navbar.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# Create Election
@login_required 
def create_election(request):
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get("name")
        date = request.POST.get("date")
        status = request.POST.get("status")

        # Validate the data
        if not name or not date:
            messages.error(request, "Election name and date are required.")
            return render(request, "create_election.html")  # Make sure to return an HttpResponse here

        # Create and save the election
        try:
            election = Election(name=name, date=date, status=status)
            election.save()
            messages.success(request, "Election created successfully!")
            return redirect('man_elections')  # Redirect to election management page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, "create_election.html")  

    return render(request, "create_election.html")


def edit_election(request):
    try:
        # Try to retrieve the election using a query parameter
        election_name = request.GET.get('name')  # Use the election name instead of primary key
        election = Election.objects.get(name=election_name)  # Get election by name or another unique field
    except Election.DoesNotExist:
        # Handle the case where the election doesn't exist
        messages.error(request, "Election not found.")
        return redirect('man_elections')  # Redirect to the election management page if not found
    except Exception as e:
        # General exception handling
        messages.error(request, f"Error: {str(e)}")
        return redirect('man_elections')

    if request.method == 'POST':
        # Update the election details
        election.name = request.POST.get('name')
        election.date = request.POST.get('date')
        election.status = request.POST.get('status')
        election.save()

        messages.success(request, f"Election '{election.name}' updated successfully!")
        return redirect('manage_elections')

    # If it's a GET request, render the edit form with the election details
    return render(request, 'edit_election.html', {'election': election})


# views.py

# views.py


def delete_election(request):
    election_id = request.GET.get('id')  
    try:
        election = Election.objects.get(id=election_id)
        election.delete()
        return redirect('man_elections') 
    except Election.DoesNotExist:
        return redirect('man_elections')  




# Manage Elections (Display all elections)
@login_required
def manage_elections(request):
    if request.method == "POST":
        election_id = request.POST.get("election_id")
        election = get_object_or_404(Election, id=election_id)
        election.delete()
        messages.success(request, "Election deleted successfully!")
        return redirect('manage_elections')  # Redirect after deletion

    elections = Election.objects.all()
    return render(request, 'man_elections.html', {'elections': elections})


# Step 1: Generate and send OTP
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            otp = random.randint(100000, 999999)  # Generate 6-digit OTP
            request.session['otp'] = otp  # Store OTP in session
            request.session['email'] = email  # Store email in session

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is {otp}. Use it to reset your password.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp')

        else:
            messages.error(request, 'Email not found.')
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


# Step 2: Verify OTP
def otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if stored_otp and str(entered_otp) == str(stored_otp):
            return redirect('reset_password')  # Redirect to password reset page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'otp.html')


# Step 3: Reset Password
from django.contrib.auth import get_user_model

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        email = request.session.get('email')

        if email:
            user = get_user_model().objects.filter(email=email).first()
            if user:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully. You can now log in.')
                return redirect('login')

        messages.error(request, 'Error resetting password.')

    return render(request, 'reset_password.html')






# Monitor Voting (Ongoing Elections)
@login_required
def monitor_voting(request):
    """View to display ongoing elections."""
    ongoing_elections = Election.objects.filter(status="Ongoing")
    return render(request, "monitor_voting.html", {"ongoing_elections": ongoing_elections})

# Election Results
@login_required
def view_result(request, election_id):
    """View to display election results."""
    election = get_object_or_404(Election, id=election_id)
    return render(request, "election_results.html", {"election": election})
@login_required
def election_results(request, election_id):
    """View to display election results."""
    election = get_object_or_404(Election, id=election_id)
    return render(request, "view_result.html", {"election": election})



# Create User
@login_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "User created successfully.")
            return redirect('man_users')

        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")

    return render(request, 'create_user.html')




@login_required
def man_users(request):
    """View to manage users."""
    try:
        users = User.objects.all()  # Fetch all users
    except Exception as e:
        messages.error(request, f"Database error: {e}")
        users = []
    
    return render(request, 'man_users.html', {'users': users})



@login_required
def edit_user(request):
    user = get_object_or_404(User)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))

        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('man_users')

    return render(request, 'edit_user.html', {'user': user})

from django.http import HttpResponse

def save_changes(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        try:
            # Fetch the user by ID and update their details
            user = User.objects.get(id=user_id)
            user.email = email
            user.phone_number = phone_number
            user.save()  # Save changes to the database
            return redirect('man_users')  # Redirect to user management page after saving changes
        except User.DoesNotExist:
            return HttpResponse("User not found.")
    return redirect('man_users')  # If it's not a POST request, just redirect


@login_required
def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        try:
            # Find the user by ID and delete them
            user = User.objects.get(id=user_id)
            user.delete()  # Delete the user from the database
            return redirect('man_users')  # Redirect to the user management page
        except User.DoesNotExist:
            return HttpResponse("User not found.")
    return redirect('man_users') 
    return render(request, 'delete_user.html', {'user': user})


# Create Candidate
@login_required
def create_candidate(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            position = request.POST.get('position')
            profile_picture = request.FILES.get('profile_picture')

            if not name or not position:
                messages.error(request, "Name and position are required.")
                return redirect('create_candidate')

            Candidate.objects.create(name=name, position=position, profile_picture=profile_picture)
            messages.success(request, "Candidate added successfully.")
            return redirect('manage_cand')

    except Exception as e:
        messages.error(request, f"Error creating candidate: {str(e)}")

    return render(request, 'create_candidate.html')


# MANAGE CANDIDATES
def manage_candidates(request):
    try:
        position = request.GET.get('position', '')  # Get filter from query params
        if position:
            candidates = Candidate.objects.filter(position=position).order_by('name')
        else:
            candidates = Candidate.objects.all().order_by('name')
    except Exception as e:
        messages.error(request, f"Error fetching candidates: {str(e)}")
        candidates = []

    return render(request, 'manage_cand.html', {'candidates': candidates, 'selected_position': position})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Candidate

# Edit Candidate
def edit_candidate(request):
    if request.method == "POST":
        candidate_id = request.POST.get('candidate_id')
        name = request.POST.get('name')
        position = request.POST.get('position')

        candidate = Candidate.objects.get(id=candidate_id)
        candidate.name = name
        candidate.position = position
        candidate.save()

        return JsonResponse({'status': 'success'})

# Delete Candidate
def delete_candidate(request):
    if request.method == "POST":
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.delete()

        return JsonResponse({'status': 'success'})





# Voter Dashboard 
@login_required
def voter_dashboard(request):
    elections = Election.objects.filter(status="active")
    return render(request, "voter_dashboard.html", {"elections": elections})

# Voting Process
@login_required
def vote(request):
    if request.method == "POST":
        election_id = request.POST.get("election_id")
        candidate_id = request.POST.get("candidate_id")
        
        election = get_object_or_404(Election, id=election_id)

        # Check if the user has already voted
        if Vote.objects.filter(user=request.user, election=election).exists():
            return render(request, "vote.html", {"error": "You have already voted!"})

        # Save the vote
        Vote.objects.create(user=request.user, election=election, candidate_id=candidate_id)
        return redirect("voter_dashboard")  # Redirect to dashboard after voting

    elections = Election.objects.filter(status="active")
    return render(request, "vote.html", {"elections": elections})

# View Election Result (for a Post)
@login_required
def view_result(request):
    try:
        
        post_name = request.GET.get('name')  
        post = Post.objects.get(name=post_name)  
    except Post.DoesNotExist:
        # Handle the case where the post is not found
        messages.error(request, "Post not found.")
        return redirect("some_default_page")  
    except Exception as e:
        
        messages.error(request, f"Error: {str(e)}")
        return redirect("some_default_page")

    # Fetch candidates related to the post
    candidates = Candidate.objects.filter(position=post)

    return render(request, "view_result.html", {
        "post": post,
        "candidates": candidates
    })



# Voter Dashboard (Active Elections)
@login_required
def voter_dashboard(request):
    elections = Election.objects.filter(status="active")
    return render(request, "voter_dashboard.html", {"elections": elections})

# Voting Process
@login_required
def vote(request):
    if request.method == "POST":
        election_id = request.POST.get("election_id")
        candidate_id = request.POST.get("candidate_id")
        
        election = get_object_or_404(Election, id=election_id)

        # Check if the user has already voted
        if Vote.objects.filter(user=request.user, election=election).exists():
            return render(request, "vote.html", {"error": "You have already voted!"})

        # Save the vote
        Vote.objects.create(user=request.user, election=election, candidate_id=candidate_id)
        return redirect("voter_dashboard")  # Redirect to dashboard after voting

    elections = Election.objects.filter(status="active")
    return render(request, "vote.html", {"elections": elections})

# View Election Result (for a Post)
def view_result(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    candidates = Candidate.objects.filter(position=post)
    return render(request, "view_result.html", {
        "post": post,
        "candidates": candidates
    })


def view_result(request):
    return render(request, "view_result.html")  # Ensure you have a 'results.html' template




def view_result(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Get the election post
    candidates = Candidate.objects.filter(position=post)  # Get candidates for this post

    return render(request, "view_result.html", {
        "post": post,
        "candidates": candidates
    })


@login_required
def user_profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.save()
            messages.success(request,"profile updated successfully!")
            return redirect('user_profile')
        except Exception as e:
            messages.error(request,f"Error updating profile:{e}")
            return redirect('edit_profile.html',{'user':request.user})
 

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
