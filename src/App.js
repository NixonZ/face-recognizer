import React,{Component} from 'react';
import './App.css';
import io from 'socket.io-client'


const socket = io.connect('http://127.0.0.1:5000/')

socket.on('connect', function () {
  console.log('Connected!');
});
class App extends Component {
  constructor(props){
    super(props);
    this.localVideoRef = React.createRef();
    this.state = {
      image: undefined
    }
  }

  onImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      this.setState({
        image: URL.createObjectURL(event.target.files[0])
      });
    }
  
  }
  componentDidMount(){

    let video = document.getElementById('SourceVideo');
    let canvas = document.getElementById('OutputVideo');
    let canvasTemp = document.getElementById('temp');
    let ctx = canvas.getContext('2d');
    var confirmImage = document.getElementById('target');
    canvasTemp.style.display = "none";
    let button = document.getElementById('recognise')

    var sending = false;

    socket.on('output',(output)=>{
      document.getElementById('Percentage').innerHTML = output.toString();
    })

    confirmImage.addEventListener('load', () => {
      canvasTemp.width = confirmImage.width;
      canvasTemp.height = confirmImage.height;
      canvasTemp.getContext('2d').drawImage(confirmImage,0,0)
      let dataURL = canvasTemp.toDataURL('image/jpeg');
      socket.emit('UploadImage',dataURL)
      sending = true;
    });
    
    button.addEventListener('click',()=>{
      let dataURL = canvas.toDataURL('image/jpeg');
      socket.emit('VideoImage', dataURL)
      socket.emit('Recognise',dataURL)
    })

    function sendSnapshot() {

      ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight)

      let dataURL = canvas.toDataURL('image/jpeg');
      if(sending) {
        socket.emit('VideoImage', dataURL);
        sending = false;  
      }
    }

    navigator.mediaDevices.getUserMedia({
      video: {
        width: { min: 640 },
        height: { min: 480 }
      },
      audio:false
    }).then((stream)=>{
      this.localVideoRef.current.srcObject = stream;
    }).catch((e)=>{
      console.log(e);
    })

    video.addEventListener('canplay',()=>{
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      setInterval(function () {
        sendSnapshot();
      }, 50);
    });

  }
  render() {
    return(
      <div>
        <video id="SourceVideo" ref={this.localVideoRef} autoPlay ></video>
        <canvas id="OutputVideo"></canvas>
        <br/>
        <input type="file" onChange={this.onImageChange} className="filetype" id="group_image" />
        <canvas id='temp'></canvas>
        <img id="target" src={this.state.image} />
        <br/>
        <button id="recognise">Click here to Recognise</button>
        <div id="Percentage"></div>
      </div>
    )
  }
}

export default App;