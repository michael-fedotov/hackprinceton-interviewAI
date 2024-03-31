let startButton = document.getElementById('start');
let stopButton = document.getElementById('stop');
let uploadButton = document.getElementById('upload'); // Upload button
let webcamVideo = document.getElementById('webcam');
let playbackVideo = document.getElementById('playback');
let recorder, stream;
let recordedBlob;

async function startRecording() {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcamVideo.srcObject = stream;
    let recordedChunks = [];
    recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });

    recorder.ondataavailable = event => {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };

    recorder.onstop = async () => {
        recordedBlob = new Blob(recordedChunks, { type: 'video/webm' });
        let url = URL.createObjectURL(recordedBlob);

        webcamVideo.hidden = true;
        playbackVideo.hidden = false;

        playbackVideo.src = url;

        stream.getTracks().forEach(track => track.stop());

        uploadButton.disabled = false; // Enable the upload button after recording
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

// Upload video function
async function uploadVideo() {
    let formData = new FormData();
    formData.append('video', recordedBlob, 'video.mp4'); // Changed to use the recordedBlob

    try {
        const response = await fetch('/upload_video/', { // Adjust the URL as necessary
            method: 'POST',
            body: formData,
        });
        if(response.ok) {
            console.log('Video uploaded successfully');
            const data = await response.json();
            console.log('Server response:', data);
        } else {
            console.error('Upload failed');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function analyzeVideo() {
    console.log('Analyzing the video...');

}

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);
uploadButton.addEventListener('click', uploadVideo); // Event listener for the upload button
analyzeButton.addEventListener('click', analyzeVideo);