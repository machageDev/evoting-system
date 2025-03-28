from datetime import timezone
from multiprocessing import Pool
#from select import poll
from django.shortcuts import render ,redirect, get_object_or_404
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.timezone import now
from .serializers import CandidateSerializer, ElectionSerializer, PostSerializer, RegisterSerializer, UserProfileSerializer, VoteSerializer, VoterSerializer
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
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.db import transaction


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

@api_view(['GET']) 
@permission_classes([AllowAny])  
def api_home(request):
    return Response({
        "message": "Welcome to the eVoting System API!",
        "status": "success",
        "endpoints": {
            "login": "/api/login/",
            "register": "/api/register/",
            "vote": "/api/vote/",
            "results": "/api/results/"
        }
    })


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
    serializer = RegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():  # Ensures atomicity
            username = serializer.validated_data['username'].strip()
            email = serializer.validated_data['email'].strip().lower()
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data['phone_number'].strip()

            if User.objects.filter(email=email).exists():
                return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, password=password, email=email)
            Voter.objects.create(user=user, phone_number=phone_number)
            token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "User registered successfully.", "token": token.key}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": f"Registration failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def apiforgot_password(request):
    try:
        email = request.data.get('email')
        if not email:
            return Response({"error": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(email=email).exists():
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
         # Generate password reset token
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(reverse('password-reset-confirm', kwargs={'token': token, 'uidb64': user.pk}))

        # Send password reset email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_url}",
            from_email="no-reply@yourdomain.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def apicreate_candidate(request):
    try:
        required_fields = ["election", "name", "profile_picture", "position"]
        missing_fields = [field for field in required_fields if not request.data.get(field)]

        if missing_fields:
            return Response({"error": f"Please fill all fields: {', '.join(missing_fields)}"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        
        election_id = request.data.get("election")
        name = request.data.get("name")
        profile_picture = request.data.get("profile_picture")
        position = request.data.get("position")  # Fixed spelling

        # Validate election existence
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response({"error": "Election not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a candidate object
        candidate_data = {
            "election": election.id,
            "name": name,
            "profile_picture": profile_picture,
            "position": position
        }

        serializer = CandidateSerializer(data=candidate_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Candidate created successfully", "data": serializer.data}, 
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def apimanage_candidate(request):
   
    if request.method == 'GET':
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def api_get_candidates(request, election_id):
    try:
        candidates = Candidate.object.filter(election_id=election_id)
        serializer = CandidateSerializer(candidates, many=True)
        return Response({
            "status":"success",
            "candidats": serializer.data
        },status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([AllowAny])   
def api_dashboard(request):
    user = request.user  # Get the user object
    today = now().date()  # Get today's date

    # Get active elections
    active_elections = Election.objects.filter(status='active')

    # Get pending elections (Filter by date, not full timestamp)
    pending_elections = Election.objects.filter(created_at__date=today)

    # Serialize elections
    active_elections_data = ElectionSerializer(active_elections, many=True).data
    pending_elections_data = ElectionSerializer(pending_elections, many=True).data

    # Prepare user data (Only if authenticated)
    user_data = None
    if user.is_authenticated:
        user_data = {
            'username': user.username,
            'email': user.email  # Sending email instead of password
        }

    # Return response
    return Response({
        'user': user_data,  # Can be None if not authenticated
        'active_elections': active_elections_data,
        'pending_elections': pending_elections_data
    })

@api_view(['GET']) 
@permission_classes([])
def apimanage_election(request):
    try:
        election_id = request.GET.get('election_id')
        election = Election.objects.get(id=election_id)
        election.status = 'active'
        election.save()
        return Response({"status":"success"},status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   


@api_view(['POST'])
@permission_classes([AllowAny])
def api_user_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user, context={"request": request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_profile_picture(request):
    user = request.user
   
    if "profile_picture" not in request.FILES:
        return Response({"error": "No image file uploaded"}, status=400)

    user.profile_picture = request.FILES["profile_picture"]
    user.save()

    return Response({"message": "Profile picture updated successfully", "profile_picture": request.build_absolute_uri(user.profile_picture.url)})


@api_view(['POST'])
@permission_classes([AllowAny])
def apicreate_profile(request):
    first_name = request.data.get('first_name')  
    last_name = request.data.get('last_name')    
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')   
    
    if not all([first_name, last_name, email, username, password]):
        return Response({'message': 'Invalid request: All fields are required'}, status=400)    
    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already taken'}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email already registered'}, status=400)    
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    return Response({'message': 'Profile created successfully', 'user_id': user.id}, status=201)    


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
    

@api_view(['POST'])
@permission_classes([AllowAny])
def apicreate_election(request):
    try:
        name = request.data.get('name')
        date = request.data.get('date')
        election_status = request.data.get('status')
        if not all([name, date,  status]):
            return Response({"error": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
        election = Election.objects.create(name=name, date=date, status=election_status)
        
        return Response({"message": "Election created successfully", "id": election.id}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([AllowAny])
def  apiget_election(request):
    try:
        id = request.GET.get('id')
        election = Election.objects.get(id=id)
        serialized_election = ElectionSerializer(election)
        return Response(serialized_election.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET']) 
def api_result(request):
    elections = Election.objects.all()
    election_results = {}

    for election in elections:
        results = {}
        candidates = Candidate.objects.filter(election=election)
        
        for candidate in candidates:
            vote_count = Vote.objects.filter(candidate=candidate).count()
            results[candidate.name] = vote_count

        election_results[election.name] = results

    return JsonResponse({"election_results": election_results})
@api_view(['DELETE'])
@permission_classes([AllowAny])
def api_delete_candidate(request,candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        if candidate.profile_picture:
            candidate.profile_picture.delete(save=False)
            candidate.delete()
            return Response({
               "status": "success",
            "message": f"Candidate {candidate.name} deleted successfully." 
            },status=200)
        else:
            return Response({"error": "Candidate does not exist"}, status=status.HTTP_404_NOT_FOUND)
                
    except Candidate.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Candidate not found."
        }, status=404)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
@permission_classes([IsAuthenticated])  # Optional: Add authentication
def dashboard(request):
    user = request.user
    current_time = timezone.now()

    # Active polls: end_date is in the future
    active_polls = Pool.objects.filter(end_date__gte=current_time)

    # Closed polls: end_date is in the past
    closed_polls = Pool.objects.filter(end_date__lt=current_time)

    # Prepare the response
    data = {
        "username": user.username,
        "active_polls": [
            {
                "id": poll.id,
                "question": poll.question,
                "end_date": poll.end_date.strftime("%Y-%m-%d")
            }
            for poll in active_polls
        ],
        "closed_polls": [
            {
                "id": poll.id,
                "question": poll.question,
                "winner_option": poll.get_winner_option()  # Make sure this method exists
            }
            for poll in closed_polls
        ]
    }

    return Response(data) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_voter_dashboard(request):
    user = request.User
    try:
        voter = Vote.objects.get(user=user)
        voter_data = {
            'name': voter.name,
            'username': voter.username,
            'age': voter.age,
        }
        return Response(voter_data, status=200)
    except vote.DoesNotExit:
         voter_data = {
            'name': user.first_name + " " + user.last_name,
            'username': user.username,
            'age': None,  # Default to None if no age is recorded
        }

    elections = Election.objects.all()  # Adjust query based on your model
    election_data = [
        {
            'id': election.id,
            'name': election.name,
            'date': election.election_date.strftime('%Y-%m-%d'),
            'status': election.status,
        }
        for election in elections
    ]

    return Response({
        'voter': voter_data,
        'elections': election_data,
    })


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
@permission_classes([IsAuthenticated])  # Requires login/authentication
def api_vote(request):
    user = request.user  # Authenticated user
    candidate_id = request.data.get('candidate_id')
    election_id = request.data.get('election_id')

    # Validate input data
    if not candidate_id or not election_id:
        return Response({
            "status": "error",
            "message": "Candidate ID and Election ID are required."
        }, status=400)

    # Check if user has already voted in this election
    if Vote.objects.filter(user=user, election_id=election_id).exists():
        return Response({
            "status": "error",
            "message": "You have already voted in this election."
        }, status=403)

    try:
        # Validate the election and candidate
        election = Election.objects.get(id=election_id)
        candidate = Candidate.objects.get(id=candidate_id, election=election)

        # Create the vote
        vote = Vote.objects.create(user=user, candidate=candidate, election=election)

        return Response({
            "status": "success",
            "message": f"Vote cast successfully for {candidate.name}.",
            "vote_id": vote.id
        }, status=201)

    except Election.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Election not found."
        }, status=404)

    except Candidate.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Candidate not found in this election."
        }, status=404)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_edit_vote(request, election_id):
    user = request.user
    candidate_id = request.data.get('candidate_id')

    # Step 1: Validate candidate ID is provided
    if not candidate_id:
        return Response({
            "status": "error",
            "message": "Candidate ID is required."
        }, status=400)

    try:
        # Step 2: Fetch the vote by user and election
        vote = Vote.objects.get(user=user, election_id=election_id)

        # Step 3: Check if the new candidate exists and belongs to the election
        try:
            candidate = Candidate.objects.get(id=candidate_id, election_id=election_id)
        except Candidate.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Candidate not found in this election."
            }, status=404)

        # Step 4: Update the candidate in the vote
        vote.candidate = candidate
        vote.save()

        return Response({
            "status": "success",
            "message": "Vote updated successfully."
        }, status=200)

    except Vote.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Vote not found for this election."
        }, status=404)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])  
def api_edit_candidate(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)

        
        name = request.data.get('name')
        position = request.data.get('position')
        election_id = request.data.get('election_id')
        profile_picture = request.FILES.get('profile_picture')

    
        if name:
            candidate.name = name
        if position:
            candidate.position = position
        if election_id:
            candidate.election_id = election_id
        if profile_picture:
            candidate.profile_picture = profile_picture

        
        candidate.save()

        return Response({
            "status": "success",
            "message": "Candidate updated successfully!"
        }, status=200)

    except ObjectDoesNotExist:
        return Response({
            "status": "error",
            "message": "Candidate not found."
        }, status=404)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)

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


@api_view(['GET'])
def active_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(start_date__lte=now, end_date__gte=now)
    serializer = ElectionSerializer(elections, many=True)
    return Response(serializer.data)


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


