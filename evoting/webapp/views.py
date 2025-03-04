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
            # Create the regular User
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Now create the associated Voter record
            voter = Voter.objects.create(user=user, name=username)  # Assuming name is passed or can be set to username
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
        voters = Voter.objects.all()  # Fetch all voters
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

        voter.user.save()  # Save the associated User model
        voter.save()  # Save the Voter model
        messages.success(request, "Voter updated successfully.")
        return redirect('man_users')

    return render(request, 'edit_user.html', {'voter': voter})



from django.http import HttpResponse
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
@login_required
def delete_user(request):
    if request.method == "POST":
        voter_id = request.POST.get("voter_id")
        try:
            # Find the voter by ID and delete them
            voter = Voter.objects.get(id=voter_id)
            voter.delete()  # Delete the voter from the database
            return redirect('man_users')  # Redirect to the user management page
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
@login_required
def result(request):
    try:
        # Fetch all active elections
        elections = Election.objects.filter(status='active')

        election_results = {}
        for election in elections:
            # Get the candidates for this election and their vote count
            candidates = Candidate.objects.filter(election=election)
            results = {}
            for candidate in candidates:
                vote_count = Vote.objects.filter(candidate=candidate).count()
                results[candidate.name] = vote_count
            election_results[election.name] = results
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
            election_id = request.POST.get("election_id")
            candidate_id = request.POST.get("candidate_id")

            # Check if both election and candidate are selected
            if not election_id or not candidate_id:
                messages.error(request, "Please select both an election and a candidate.")
                return redirect("vote")

            election = get_object_or_404(Election, id=election_id)
            candidate = get_object_or_404(Candidate, id=candidate_id, election=election)

            # Check if the user has already voted in this election
            if Vote.objects.filter(user=request.user, election=election).exists():
                messages.error(request, "You have already voted in this election.")
                return redirect("vote")
            # Save the vote
            Vote.objects.create(user=request.user, election=election, candidate=candidate)
            messages.success(request, f"You have successfully voted for {candidate.name} in {election.name}.")
            
            # Redirect to results page after voting
            return redirect("result")
        except Exception as e:
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


from rest_framework import serializers, viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model, authenticate
from .models import Election, Post, Candidate, Vote, Voter
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Voter
        fields = ['name', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Voter.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")


# View for Registering a New User
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for User Login and Token Generation
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# ViewSets for CRUD operations on Election, Post, Candidate, Vote, and Voter
class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]



class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Custom logic to handle vote creation
        user = request.user
        candidate_id = request.data.get('candidate')

        # Check if the user has already voted in the same election (optional)
        if Vote.objects.filter(user=user, candidate__id=candidate_id).exists():
            return Response({"detail": "You have already voted."}, status=400)

        # If no prior vote exists, proceed to create the vote
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Allow users to view their vote"""
        # You can customize this if needed, e.g., by checking ownership of the vote
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Allow users to update their vote"""
        # Optionally, you can restrict users from changing their vote after voting
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Allow users to delete their vote"""
        # Optionally, you can customize this method as well
        return super().destroy(request, *args, **kwargs)

