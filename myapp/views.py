from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube_search import YoutubeSearch
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .serializer import UserRegistrationSerializer, VideoSerializer
from rest_framework import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, Video




from rest_framework import generics
class Home(LoginRequiredMixin, APIView):
    login_url="/login/"
    def get(self, request):
        return render(template_name="dashboard.html", request=request)
    
    def post(self, request):
        topic = request.POST.get("topic", '')
        print(topic)
        if topic:
            results = YoutubeSearch(topic,max_results=15).to_dict()
            video = []
            video_list =[]

            for result in results:
                video_data = {
                    'title': result['title'],
                    'video_id': result['id'],
                    'link': f"https://www.youtube.com/watch?v={result['id']}",
                    'thumbnail': result['thumbnails'][0] if 'thumbnails' in result else None,
                }

                video.append(video_data)
            
            return render(template_name="dashboard.html", request=request, context={"videos":video, "topic":topic, "user":request.user})
        return render(template_name="dashboard.html", request=request, context={"topic":topic, "user":request.user})
    


class  Landingpage(APIView):
    def get(self, request):
        return render(template_name="landingpage.html", request=request)
    

class LoginView(APIView):
    def get(self, request):
        return render(template_name="login.html", request=request)
    
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Assuming your login form sends 'username' and 'password' in the POST data
        username = request.data.get('email')
        password = request.data.get('password')
        print(request.POST)
        print(username)
        print(password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return render(template_name="dashboard.html", request=request)
        else:
            return render(template_name="login.html", request=request, context={"error":"email or password invalid"})


class SignUpView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        return render(request, template_name="signup.html")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
       
        if serializer.is_valid():
           try:
            
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                
                return redirect("landing")
           except serializers.ValidationError as e:
            # Handle any specific exceptions you want to catch
                  print(e)
                  return render(request, template_name="signup.html", context={"error": "Registration failed. Please try again."})
        else:
            error = serializer.errors
            return render(request, template_name="signup.html", context={"error": error})


class APILogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Log the user out
        logout(request)
        return render(request=request, template_name="landingpage.html")


class HandleVideo(APIView):
    def post(self, request):
        video_data = VideoSerializer(data=request.data)

        if video_data.is_valid():
            video_data.save(user = request.user)
            return Response({'message': 'Video saved successfully'})
        else:
            print("not valid")
            print(video_data.errors)
            return Response({'message': 'Invalid data provided'}, status=400)
        
class userview(APIView):
    def get(self, request):
        users = User.objects.all()
        data = UserRegistrationSerializer(users, many=True)
        return Response(data.data)
    

class userVideos(APIView):

    def get(self, request):
        videos = Video.objects.filter(user= request.user)
        data = VideoSerializer(videos, many=True)
        
        return render(template_name="userVideos.html", context={"videos":data})


        
        
       

        
    


   