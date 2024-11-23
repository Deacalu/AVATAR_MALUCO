document.getElementById('speakButton').addEventListener('click', function() {
    // Captura áudio do usuário e envia ao backend
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        let mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function(e) {
            let audioBlob = e.data;
            sendAudioToBackend(audioBlob);
        };
        mediaRecorder.start();
        setTimeout(() => mediaRecorder.stop(), 3000);  // Grava por 3 segundos
    });
});

function sendAudioToBackend(audioBlob) {
    let formData = new FormData();
    formData.append('audio', audioBlob);

    fetch('/api/process_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Exibe a resposta e reproduz o áudio gerado pelo backend
        document.getElementById('response').innerText = data.response;
        let audio = new Audio(data.audio);
        audio.play();
    });
}
