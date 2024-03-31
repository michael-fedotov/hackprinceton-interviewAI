import cv2
import matplotlib.pyplot as plt
from deepface import DeepFace

def get_emotion_dict(path):
    video = cv2.VideoCapture(path)

    # Frames per second of the video
    fps = video.get(cv2.CAP_PROP_FPS)

    # Total number of frames
    totalNoFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # video duration in seconds
    num_seconds = int(totalNoFrames // fps)
    acc_dict = {
    "angry": 0,
    "disgust": 0,
    "fear": 0,
    "happy": 0,
    "sad": 0,
    "surprise": 0,
    "neutral": 0,}

    num_frames = 0

    for i in range(1, num_seconds):
        minutes = int(i // 60)
        seconds = i
        frame_id = int(fps * (minutes * 60 + seconds))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        if ret:
            num_frames += 1
            result = DeepFace.analyze(frame, actions=["emotion"])
            emotions = result[0]["emotion"]
            for key in list(acc_dict.keys()):
                acc_dict[key] += emotions[key] 
    
    summary_dict = {key: (value/num_frames) for key, value in acc_dict.items()}
    return summary_dict