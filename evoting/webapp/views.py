from multiprocessing import AuthenticationError
from sqlite3 import DatabaseError
from django.shortcuts import render ,redirect, get_object_or_404
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Candidate, Election, Post, Vote
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')

def base(request):  # Ensure this function exists
    return render(request, 'base.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
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
def dashboard(request):
    return render(request, 'dashboard.html')


def create_candidate(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        profile_picture = request.FILES.get('profile_picture')

        # Handle manual validation
        if not name or not position:
            return render(request, 'create_candidate.html', {'error': 'All fields are required!', 'election': election})

        # Save the candidate to the database
        Candidate.objects.create(
            name=name, 
            position=position, 
            profile_picture=profile_picture, 
            election=election
        )
        return redirect('manage_candidates', election_id=election.id)

    return render(request, 'create_candidate.html', {'election': election})



def manage_candidates(request, election_id):
    """Displays a list of candidates for a given election."""
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)
    
    return render(request, "manage_cand.html", {
        "election": election,
        "candidates": candidates
    })

def create_candidate(request, election_id):
    """Handles candidate creation without Django forms."""
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        profile_picture = request.FILES.get('profile_picture')

        if not name or not position:
            return render(request, 'create_candidate.html', {
                'error': 'All fields are required!',
                'election': election
            })

        Candidate.objects.create(
            name=name, 
            position=position, 
            profile_picture=profile_picture, 
            election=election
        )
        return redirect('manage_candidates', election_id=election.id)

    return render(request, 'create_candidate.html', {'election': election})

def edit_candidate(request, candidate_id):
    """Handles editing an existing candidate without Django forms."""
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if request.method == 'POST':
        candidate.name = request.POST.get('name')
        candidate.position = request.POST.get('position')
        if 'profile_picture' in request.FILES:
            candidate.profile_picture = request.FILES.get('profile_picture')
        candidate.save()
        return redirect('manage_candidates', election_id=candidate.election.id)

    return render(request, 'edit_cand.html', {'candidate': candidate})

def delete_candidate(request, candidate_id):
    """Handles deleting a candidate."""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election_id = candidate.election.id

    if request.method == "POST":
        candidate.delete()
        return redirect('manage_candidates', election_id=election_id)

    return render(request, 'delete_cand.html', {'candidate': candidate})




# Create Election
def create_election(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        status = request.POST.get('status')
        new_election = Election.objects.create(name=name, election_date=date, status=status)
        messages.success(request, f"Election '{new_election.name}' created successfully!")
        return redirect('manage_elections')
    return render(request, 'create_election.html')

# Edit Election
def edit_election(request):
    try:
        election = Election.objects.get(Election, pk=request.GET.get("pk"))
    except Exception as e:
        messages.error(request,e)
        return redirect("man_elections")
    if request.method == 'POST':
        election.name = request.POST.get('name')
        election.election_date = request.POST.get('date')
        election.status = request.POST.get('status')
        election.save()
        messages.success(request, f"Election '{election.name}' updated successfully!")
        return redirect('manage_elections')
    return render(request, 'edit_election.html', {'election': election})

# Delete Election
def delete_election(request):
    election_id = request.GET.get('id')
    election = get_object_or_404(Election, id=election_id)
    election.delete()
    messages.success(request, f"Election '{election.name}' deleted successfully!")
    return redirect('manage_elections')

# Manage Elections (Display all elections)
def manage_elections(request):
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
def monitor_voting(request):
    """View to display ongoing elections."""
    ongoing_elections = Election.objects.filter(status="Ongoing")
    return render(request, "monitor_voting.html", {"ongoing_elections": ongoing_elections})

# Election Results
def view_result(request, election_id):
    """View to display election results."""
    election = get_object_or_404(Election, id=election_id)
    return render(request, "election_results.html", {"election": election})

def election_results(request, election_id):
    """View to display election results."""
    election = get_object_or_404(Election, id=election_id)
    return render(request, "view_result.html", {"election": election})



# Create User
def create_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Create the user object
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return redirect('man_users')  # Redirect to the user management page
    return render(request, 'create_user.html')
def man_users(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    try:
        users = User.objects.all()  
    except DatabaseError as e:
        
        print(f"Database error occurred: {e}")
        users = []  

    context = {
        'users': users
    }
    return render(request, 'man_users.html', context)



def edit_user(request):
    try:
        user_id = request.GET.get('user_id')  # Get user_id from request
        if not user_id:
            messages.error(request, "User ID is missing.")
            return redirect('manage_users')

        user = get_object_or_404(User, id=user_id)

        if request.method == "POST":
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            if request.POST.get('password'):
                user.set_password(request.POST.get('password'))  # Update password securely
            user.save()
            messages.success(request, "User updated successfully.")
            return redirect('man_users')  # Redirect to user management page

        return render(request, 'edit_user.html', {'user': user})

    except Exception as e:
        messages.error(request, f"Error updating user: {str(e)}")
        return redirect('man_users')  # Redirect in case of errors


def delete_user(request):
    try:
        user_id = request.GET.get('user_id')  # Get user_id from request
        if not user_id:
            messages.error(request, "User ID is missing.")
            return redirect('man_users')

        user = get_object_or_404(User, id=user_id)

        if request.method == "POST":
            user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect('man_users')  # Redirect to user management page

        return render(request, 'delete_user.html', {'user': user})

    except Exception as e:
        messages.error(request, f"Error deleting user: {str(e)}")
        return redirect('man_users')  # Redirect in case of errors


# Monitor Voting (Ongoing Elections)
def monitor_voting(request):
    ongoing_elections = Election.objects.filter(status="Ongoing")
    return render(request, "monitor_voting.html", {"ongoing_elections": ongoing_elections})

# Election Results
def election_results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    return render(request, "election_results.html", {"election": election})

# Create Candidate
def create_candidate(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        party = request.POST.get('party')
        
        # Create the candidate and associate with the election
        candidate = Candidate.objects.create(name=name, party=party, election=election)
        messages.success(request, f"Candidate '{candidate.name}' added to election '{election.name}' successfully!")
        return redirect('manage_candidates', election_id=election.id)

    return render(request, 'create_candidate.html', {'election': election})

# Edit Candidate
def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == "POST":
        candidate.name = request.POST.get('name')
        candidate.party = request.POST.get('party')
        candidate.save()
        return redirect('manage_cand', election_id=candidate.election.id)

    return render(request, 'edit_cand.html', {'candidate': candidate})

# Delete Candidate
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == "POST":
        candidate.delete()
        messages.success(request, f"Candidate '{candidate.name}' deleted successfully!")
        return redirect('manage_cand', election_id=candidate.election.id)

    return render(request, 'delete_cand.html', {'candidate': candidate})

# Manage Candidates (View all candidates)
def manage_candidates(request):
    candidates = Candidate.objects.all()
    return render(request, "manage_cand.html", {"candidates": candidates})

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




