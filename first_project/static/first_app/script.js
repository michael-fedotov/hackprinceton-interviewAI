let startButton = document.getElementById('start');
let stopButton = document.getElementById('stop');
let video = document.getElementById('webcam');
let recorder, stream;

async function startRecording() {
    stream = await navigator.mediaDevices.getUserMedia({video: true});
    video.srcObject = stream;
    recorder = new MediaRecorder(stream, {mimeType: 'video/webm'});

    const chunks = [];
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = async () => {
        const completeBlob = new Blob(chunks, {type: 'video/webm'});
        uploadVideo(completeBlob);
    };

    recorder.start();
    stopButton.disabled = false;
    startButton.disabled = true;
}

function stopRecording() {
    recorder.stop();
    stream.getVideoTracks()[0].stop();
    stopButton.disabled = true;
    startButton.disabled = false;
}

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);

async function uploadVideo(videoBlob) {
    let formData = new FormData();
    formData.append('video', videoBlob, 'video.mp4');

    try {
        const response = await fetch('/upload_video/', {  // URL adjusted to /first_app/upload/
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
