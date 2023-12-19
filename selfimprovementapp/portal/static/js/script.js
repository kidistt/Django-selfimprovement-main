const video=document.getElementById("video")
Promise.all([
    faceapi.nets.TinyFaceDetector.loadFromUrl('/models'),
    faceapi.nets.FaceLandmark68Net.loadFromUrl('/models'),
    faceapi.nets.faceRecognitionNet.loadFromUrl('/models'),
    faceapi.nets.FaceExpression.loadFromUrl('/models')

])

function startVideo()
{
    navigator.getUserMedia(
        {
        video: {}},
        stream=> video.srcObject=stream,
        err=> console.error(err)
    )
    
}
video.addEventListener('play',()=>{
    const canvas=faceapi.createCanvasFromMedia(video)
    document.body.append(canvas)
    const displaySize={width: video.width, height:video.height}
    faceapi.matchDimensions(canvas, displaySize)
    setInterval(async () => {
        const webStream=await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpression()
        const finalStream=faceapi.resizeResults(webStream,displaySize)
        canvas.getContext('2d').clearRect(0,0,canvas.width,canvas.height)
        faceapi.draw.drawDetection(canvas, finalStream)
        faceapi.draw.drawFaceLandmarks(canvas, finalStream)
        faceapi.draw.drawExpressions(canvas, finalStream)
    },100)
}
)