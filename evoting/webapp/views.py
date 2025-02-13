from multiprocessing import AuthenticationError
from django.shortcuts import render ,redirect, get_object_or_404
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User  # Import User model
from django.conf import settings
from .models import Election, Voter


def home(request):
    return render(request, 'index.html')

def base(request):  # Ensure this function exists
    return render(request, 'base.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = AuthenticationError(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html",{"error":"invalid credentials"})
    return render(request, 'login.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request,"register.html",{"form":form})

def navbar(request):
    return render(request, 'navbar.html')
def dashboard(request):
    return render(request, 'dashboard.html')



from .models import Election
from .forms import CreateUserForm, ElectionForm

def create_election(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_elections')  # Redirect to election list
    else:
        form = ElectionForm()

    return render(request, 'create_election.html', {'form': form})

def manage_elections(request):
    elections = Election.objects.all()
    return render(request, 'manage_elections.html', {'elections': elections})

def delete_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    election.delete()
    return redirect('manage_elections')




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




from .forms import CandidateForm  
from .models import Election

def add_candidate(request, election_id):
    election = Election.objects.get(id=election_id)  # Fetch the election
    form = CandidateForm()  # Create the form instance

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)  # Include files if you have file upload
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election  # Associate candidate with the election
            candidate.save()
            return redirect('manage_candidates', election_id=election.id)

    return render(request, 'create.cand.html', {'form': form, 'election': election})  # Pass form to template


from .forms import CreateUserForm
from django.contrib.auth import login

def create_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('manage_users')  # Redirect to the user management page
    else:
        form = CreateUserForm()
    
    return render(request, 'create_user.html', {'form': form})

def monitor_voting(request):
    """View to display ongoing elections."""
    ongoing_elections = Election.objects.filter(status="Ongoing")
    return render(request, "monitor_voting.html", {"ongoing_elections": ongoing_elections})

def election_results(request, election_id):
    """View to display election results."""
    election = get_object_or_404(Election, id=election_id)
    return render(request, "election_results.html", {"election": election})


from .models import Candidate
from .forms import CandidateForm

def create_candidate(request):
    """View to create a new candidate."""
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_candidates")
    else:
        form = CandidateForm()
    return render(request, "create_cand.html", {"form": form})

def edit_candidate(request, candidate_id):
    """View to edit an existing candidate."""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect("manage_candidates")
    else:
        form = CandidateForm(instance=candidate)
    return render(request, "edit_cand.html", {"form": form, "candidate": candidate})

def delete_candidate(request, candidate_id):
    """View to delete a candidate."""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()
    return redirect("manage_candidates")

def manage_candidates(request):
    """View to display all candidates."""
    candidates = Candidate.objects.all()
    return render(request, "manage_cand.html", {"candidates": candidates})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Election, Vote

@login_required
def voter_dashboard(request):
    """Display the voter dashboard with active elections."""
    elections = Election.objects.filter(status="active")  # Show only active elections

    context = {
        "elections": elections,
    }
    return render(request, "voter_dashboard.html", context)

@login_required
def vote(request):
    """Handles the voting process."""
    if request.method == "POST":
        election_id = request.POST.get("election_id")
        candidate_id = request.POST.get("candidate_id")

        # Get the election object
        election = get_object_or_404(Election, id=election_id)

        # Ensure the user has not voted already
        if Vote.objects.filter(user=request.user, election=election).exists():
            return render(request, "vote.html", {"error": "You have already voted!"})

        # Save the vote
        vote = Vote(user=request.user, election=election, candidate_id=candidate_id)
        vote.save()

        return redirect("voter_dashboard")  # Redirect after voting

    # Show elections for voting
    elections = Election.objects.filter(status="active")
    return render(request, "vote.html", {"elections": elections})



