from django.shortcuts import render ,redirect, get_object_or_404
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .serializers import CandidateSerializer, ElectionSerializer, PostSerializer, RegisterSerializer, VoteSerializer, VoterSerializer
from .models import Post, Voter, Vote, Candidate, Election 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model, authenticate
from .models import Election, Post, Candidate, Vote, Voter
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django.http import HttpResponse



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

            
            voter = Voter.objects.create(user=user, name=username)  
            voter.save()

            messages.success(request, "User and Voter created successfully.")
            return redirect('man_users')

        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")

    return render(request, 'create_user.html')

@login_required
def man_users(request):
    """View to manage voters."""
    try:
        voters = Voter.objects.all()  
    except Exception as e:
        messages.error(request, f"Database error: {e}")
        voters = []
    
    return render(request, 'man_users.html', {'voters': voters})
@login_required
def edit_user(request):

    voter = get_object_or_404(Voter, user__id=request.user.id)

    if request.method == "POST":
        voter.user.username = request.POST.get('username')
        voter.user.email = request.POST.get('email')
        
        if request.POST.get('password'):
            voter.user.set_password(request.POST.get('password'))

        voter.user.save()  
        voter.save()  
        messages.success(request, "Voter updated successfully.")
        return redirect('man_users')

    return render(request, 'edit_user.html', {'voter': voter})

@api_view(['POST'])
@permission_classes([AllowAny])
def apiregister(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number=request.data.get('phone_number')
        if not all ([username, email, password,phone_number]):
            return Response({"error": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        voter = Voter.objects.create(user=user,phone_number=phone_number)
        token, created = Token.objects.get_or_create(user=user)

        return Response({"message": "User registered successfully.", "token": token.key}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])
@permission_classes([AllowAny])
def get_elections(request):
    try:
        user_id = request.GET.get('id')
        print(id)
        elections = Election.objects.all()
        serialized_elections = ElectionSerializer(elections, many=True)
        return Response(serialized_elections.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([AllowAny])  
def create_election(request):
    try:
        name = request.data.get('name')    
        date = request.data.get('date')      
        election_status = request.data.get('status')        
        if not all([name, date,  status]):
            return Response({"error": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)        
        if Election.objects.filter(name=name).exists():
            return Response({"error": "Election already exists"}, status=status.HTTP_400_BAD_REQUEST)        
        election = Election.objects.create(
            name=name,
            date=date,            
            status=election_status
        )

        return Response({"message": "Election created successfully."}, status=status.HTTP_201_CREATED)

    except Exception as e:    
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([AllowAny])  
def delete_election(request):
    election_id = request.GET.get('id')
    if not election_id:
        return Response({"error": "Please provide election id"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        election = Election.objects.get(id=election_id)
        election.delete()
        return Response({"message": "Election deleted successfully"}, status=status.HTTP_200_OK)
    except Election.DoesNotExist:
        return Response({"error": "Election not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error":e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@permission_classes([AllowAny])  
def apilogin(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if not all([username,password]):
            return Response({"error":"Incomplete data"},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = username,password = password)
        if user is not None:
            token,created = Token.objects.get_or_create(user = user)
            return Response({"message":"success","token":token.key},status=status.HTTP_200_OK)
        return Response({"error":"Invalid credentials"},status = status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"error":e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_changes(request):
    if request.method == "POST":
        voter_id = request.POST.get("voter_id")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        try:
            # Fetch the voter by ID and update their details
            voter = Voter.objects.get(id=voter_id)
            voter.user.email = email  # Update associated User model
            voter.phone_number = phone_number
            voter.user.save()  # Save the User model
            voter.save()  # Save the Voter model
            return redirect('man_users')  # Redirect to user management page after saving changes
        except Voter.DoesNotExist:
            return HttpResponse("Voter not found.")
    return redirect('man_users')  # If it's not a POST request, just redirect




@login_required
def delete_user(request):
    if request.method == "POST":
        voter_id = request.POST.get("voter_id")
        try:
            # Find the voter by ID and delete them
            voter = Voter.objects.get(id=voter_id)
            voter.delete()  
            return redirect('man_users')  
        except Voter.DoesNotExist:
            return HttpResponse("Voter not found.")
    return redirect('man_users')



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
@login_required
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
                  

def edit_candidate(request):
    if request.method == "POST":
        candidate_id = request.POST.get("candidate_id")
        new_name = request.POST.get("name")
        new_position = request.POST.get("position")

        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate.name = new_name
        candidate.position = new_position
        candidate.save()

        messages.success(request, "Candidate updated successfully.")
        return redirect('manage_cand')

    messages.error(request, "Invalid request.")
    return redirect('manage_cand')

def delete_candidate(request):
    if request.method == "POST":
        candidate_id = request.POST.get("candidate_id")

        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate.delete()

        messages.success(request, "Candidate deleted successfully.")
        return redirect('manage_cand')

    messages.error(request, "Invalid request.")
    return redirect('manage_cand')


def save_changes(request):
    if request.method == "POST":
        candidate_id = request.POST.get("candidate_id")
        name = request.POST.get("name")
        position = request.POST.get("position")

        try:
            # Fetch the candidate by ID and update their details
            candidate = get_object_or_404(Candidate, id=candidate_id)
            candidate.name = name
            candidate.position = position
            candidate.save()  # Save changes to the database
            return redirect('manage_cand')  # Redirect to candidate management page after saving changes
        except Candidate.DoesNotExist:
            return HttpResponse("Candidate not found.")
    
    return redirect('manage_cand')  # If it's not a POST request, just redirect




# Voter Dashboard 
@login_required
def voter_dashboard(request):
    elections = Election.objects.filter(status="active")
    return render(request, "voter_dashboard.html", {"elections": elections})

# Voting Process


# View Election Result (for a Post)
from django.db.models import Count
@login_required
def result(request):
    try:
        # Fetch all active elections
        elections = Election.objects.filter(status='active')

        election_results = {}

        for election in elections:
            # Get candidates and their vote count in one query (optimized)
            candidates = Candidate.objects.filter(election=election).annotate(vote_count=Count('vote'))

            # Store results in a dictionary
            results = {candidate.name: candidate.vote_count for candidate in candidates}

            election_results[election.name] = results  # Store each election's results
    except Exception as e:
        messages.error(request, f"An error occurred while fetching results: {str(e)}")
        election_results = {}

    return render(request, 'view_result.html', {'election_results': election_results})

@login_required
def vote(request):
    """View for voters to cast their votes."""
    try:
        elections = Election.objects.filter(status='active')  # Only show active elections
        election_id = request.GET.get('election_id')  # Get selected election ID

        if election_id:
            # If election is selected, filter candidates for that election
            candidates = Candidate.objects.filter(election_id=election_id)
        else:
            candidates = []
    except Exception as e:
        messages.error(request, f"Error fetching elections or candidates: {e}")
        elections = []
        candidates = []

    return render(request, 'vote.html', {'elections': elections, 'candidates': candidates})



# Handle vote submission
@login_required
def submit_vote(request): 
    if request.method == "POST":
        try:
            print("🔹 submit_vote view called!")  # Debugging

            election_id = request.POST.get("election_id")
            candidate_id = request.POST.get("candidate_id")
            print(f"Received election_id: {election_id}, candidate_id: {candidate_id}")  # Debugging

            # Check if both election and candidate are selected
            if not election_id or not candidate_id:
                messages.error(request, "Please select both an election and a candidate.")
                return redirect("vote")

            election = get_object_or_404(Election, id=election_id)
            candidate = get_object_or_404(Candidate, id=candidate_id, election=election)
            print(f"Election: {election}, Candidate: {candidate}")  # Debugging

            # Check if the user is authenticated
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to vote.")
                return redirect("login")

            # Check if the user has already voted in this election
            if Vote.objects.filter(user=request.user, candidate__election=election).exists():
                messages.error(request, "You have already voted in this election.")
                return redirect("voter_dashboard")

            # Save the vote
            vote = Vote.objects.create(user=request.user, election=election, candidate=candidate)
            print(f"✅ Vote saved: {vote}")  # Debugging

            messages.success(request, f"You have successfully voted for {candidate.name} in {election.name}.")

            # Redirect to results page after voting
            return redirect("result")

        except Exception as e:
            print(f"❌ Error: {e}")  # Debugging
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("vote")

    return redirect("vote")





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

@login_required
def profile(request):
    return render(request, 'profile.html') 
@login_required
def edit_profile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        if hasattr(user,'profile'):
            user.profile.phone_number = phone_number
            user.profile.save()   
            messages.success(request,"profile updated successfully!")
        return redirect('profile')
    
    return render(request,'edit_profile.html')    


