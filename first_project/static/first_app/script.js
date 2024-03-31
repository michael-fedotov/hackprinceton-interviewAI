let startButton = document.getElementById('start');
let stopButton = document.getElementById('stop');
let webcamVideo = document.getElementById('webcam');
let playbackVideo = document.getElementById('playback');
let recorder, stream;
let recordedChunks = [];



async function startRecording() {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcamVideo.srcObject = stream;
    recordedChunks = [];
    recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    
    recorder.ondataavailable = event => {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };
    
    recorder.onstop = async () => {
        let recordedBlob = new Blob(recordedChunks, { type: 'video/webm' });
        let url = URL.createObjectURL(recordedBlob);
        
        // Hide the live webcam feed and show the playback video
        webcamVideo.hidden = true;
        playbackVideo.hidden = false;
        
        // Set the recorded video for playback
        playbackVideo.src = url;
        
        // Reset the stream and recorder for another recording session
        stream.getTracks().forEach(track => track.stop());
    };
    
    recorder.start();
    stopButton.disabled = false;
    startButton.disabled = true;
}

function stopRecording() {
    recorder.stop();
    stopButton.disabled = true;
    startButton.disabled = false;
}

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);
