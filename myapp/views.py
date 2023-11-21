from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube_search import YoutubeSearch
# Create your views here.
class Home(APIView):
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
            
            return render(template_name="dashboard.html", request=request, context={"videos":video, "topic":topic})
        return render(template_name="dashboard.html", request=request, context={"topic":topic})
    


class  Landingpage(APIView):
    def get(self, request):
        return render(template_name="landingpage.html", request=request)

