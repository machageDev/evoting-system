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


def create_candidate(request):
    
    try:
        
        election = Election.objects.filter(status='active').latest('date')  

        if request.method == "POST":
            name = request.POST.get("name")
            position = request.POST.get("position")
            profile_picture = request.FILES.get("profile_picture")

            if not name or not position:
                messages.error(request, "Candidate name and position are required.")
                return render(request, "create_candidate.html", {"election": election})

            # Create and save candidate
            candidate = Candidate(name=name, position=position, profile_picture=profile_picture, election=election)
            candidate.save()
            
            messages.success(request, "Candidate added successfully!")
            return redirect('manage_cand')

        return render(request, "create_candidate.html", {"election": election})

    except Election.DoesNotExist:
        messages.error(request, "No active election found.")
        return redirect('manage_cand')

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('manage_cand')


def manage_cand(request):
    """Displays a list of candidates for the latest active election."""
    try:
        
        election = Election.objects.filter(status='active').latest('election_date')

        candidates = Candidate.objects.filter(election=election)

        return render(request, "manage_cand.html", {
            "election": election,
            "candidates": candidates
        })

    except Election.DoesNotExist:
        return render("No active election found.", status=404)

    except Exception as e:
        return render (f"An error occurred: {str(e)}", status=500)



def edit_candidate(request, candidate_id):
    
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
    
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election_id = candidate.election.id

    if request.method == "POST":
        candidate.delete()
        return redirect('manage_candidates', election_id=election_id)

    return render(request, 'delete_cand.html', {'candidate': candidate})




# Create Election
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

def delete_election(request):
    try:
        # Get the election by name or any unique field
        election_name = request.GET.get('name')  # Assuming you're passing the name instead of the id
        election = Election.objects.get(name=election_name)  # Search by name instead of id
    except Election.DoesNotExist:
        # Handle the case where the election doesn't exist
        messages.error(request, "Election not found.")
        return redirect('man_elections')  # Redirect if the election doesn't exist
    except Exception as e:
        # Handle any other unexpected errors
        messages.error(request, f"Error: {str(e)}")
        return redirect('man_elections')

    # Delete the election
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
def create_candidate(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            position = request.POST.get('position')
            profile_picture = request.FILES.get('profile_picture')

            if not name or not position:
                messages.error(request, "Name and position are required.")
                return redirect('create_candidate')
            try:
                candidate = Candidate.objects.create(name=name, position=position, profile_picture=profile_picture)
                messages.success(request, "Candidate created successfully.")
                return redirect('manage_cand')
            except Exception as e:
                messages.error(request, f"Error creating candidate:")
                return redirect('create_candidate')
    except Exception as e:
                messages.error(request, f"Error creating candidate: {str(e)}")
                return redirect('manage_cande')
    return render(request, 'create_candidate.html')    


# Edit Candidate
def edit_candidate(request):
    try:
        if request.method == "POST":
            candidate_name = request.POST.get('name')
            candidate_party = request.POST.get('party')

            candidate = Candidate.objects.filter(name=candidate_name, party=candidate_party).first()
            if not candidate:
                messages.error(request, "Candidate not found.")
                return redirect('manage_cand')

            candidate.name = candidate_name
            candidate.party = candidate_party
            candidate.save()
            messages.success(request, f"Candidate '{candidate.name}' updated successfully!")
            return redirect('manage_cand')

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('manage_cand')

    return render(request, 'edit_cand.html')


# Delete Candidate
def delete_candidate(request):
    try:
        if request.method == "POST":
            candidate_name = request.POST.get('name')
            candidate = Candidate.objects.filter(name=candidate_name).first()

            if not candidate:
                messages.error(request, "Candidate not found.")
                return redirect('manage_cand')

            candidate.delete()
            messages.success(request, "Candidate deleted successfully!")
            return redirect('manage_cand')

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('manage_cand')

    return render(request, 'delete_cand.html')


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
