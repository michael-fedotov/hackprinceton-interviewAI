from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from moviepy.editor import VideoFileClip
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import tasks
from .tasks import process_video_emotions
from django.core.files.storage import default_storage
import os

current_dir = os.path.dirname(__file__)
sister_dir = os.path.abspath(os.path.join(current_dir, '..', 'Candidate_analysis'))
# file_path = os.path.join(sister_dir, 'emotion.py')
file_path = os.path.join(sister_dir, 'tasks.py')


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
        # print('hello')
        # Save video file
        video_file_path = default_storage.save(os.path.join(save_path, video_file.name), video_file)
        request.session['video_output_path'] = video_file_path
        # return render(request, 'first_app/review_video.html', {'video_url': video_file_path})
        # print(request.session['emotions_dict'])
        try:
            # Process video to extract audio
            clip = VideoFileClip(video_file_path)

            # Limit video duration to 1 minute
            if clip.duration > 60:
                clip = clip.subclip(0, 60)  # Keep only the first minute

            # Write video file as mp4
            video_output_path = os.path.splitext(video_file_path)[0] + '.mp4'
            clip.write_videofile(video_output_path, codec='libx264', audio_codec='aac')
            # request.session['emotions_dict'] = (video_file_path)
            # Return response with the path to the converted video

            request.session['video_output_path'] = video_output_path
            return redirect(('review_video'))
            return JsonResponse({
                'message': 'File uploaded and processed successfully.',
                'video_path': video_output_path,
            })
        except Exception as e:
            # request.session['video_output_path'] = video_output_path
            return redirect(('/review_video'))
            # Log the error
            print(f"Error processing video: {str(e)}")
            return JsonResponse({'error': 'Failed to process uploaded video.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    



def review_video(request):
    # result = tasks.process_video_emotions.delay('/Users/michaelfedotov/Documents/Projects/DJANGO/hackprinceton-interviewAI/video1.mp4')
    # result.wait()
    # summary_dict = result.get()
    video_path = request.session.get('video_output_path')
    task = process_video_emotions.delay(video_path)

    # video_output_path = request.session.get('video_output_path')
    # if not video_output_path:
    #     # Redirect or show an error if there's no video path stored in session
    #     return redirect('/')  # Adjust as necessary

    # context = {'video_url': video_output_path}
    # return render(request, 'first_app/review_video.html', {'video_url': video_output_path})

