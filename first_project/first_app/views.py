from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from moviepy.editor import VideoFileClip
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os

# Create your views here.

def index(request):
    tv_shows_list={"tv_shows":{'Game of Thrones':'9.3','Blacklist': '8','Suits': '8.5','The Witcher': '8.5'}}
    return render(request,'first_app/index.html',context=tv_shows_list)

def home(request):
    return HttpResponse("Welcome to home page!")

def educative(request):
    return HttpResponse("Welcome to Educative page!")

def record(request):
    return render(request,'first_app/record.html')

@csrf_exempt 
def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if not video_file:
            return JsonResponse({'error': 'No video file uploaded.'}, status=400)
        
        # Define save path
        save_path = 'uploaded_videos'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Save video file
        video_file_path = default_storage.save(os.path.join(save_path, video_file.name), video_file)
        
        # Process video to extract audio
        clip = VideoFileClip(video_file_path)
        audio_file_path = os.path.splitext(video_file_path)[0] + '.mp3'
        clip.audio.write_audiofile(audio_file_path)
        
        # Limit video duration to 1 minutez
        if clip.duration > 60:
            clip = clip.subclip(0, 60)  # Keep only the first minute
            clip.write_videofile(video_file_path, codec='libx264', audio_codec='aac')
        
        return JsonResponse({
            'message': 'File uploaded and processed successfully.',
            'video_path': video_file_path,
            'audio_path': audio_file_path
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)