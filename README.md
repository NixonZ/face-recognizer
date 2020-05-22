
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

  

## Available Scripts

  

In the project directory, you can run:

  

### `yarn start`

  

Runs the app in the development mode.<br />

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

  

### `yarn start-api`

  

Runs the Backend for image processing

  

### `yarn test`

  

Launches the test runner in the interactive watch mode.<br />

See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

  

### `yarn build`

  

Builds the app for production to the `build` folder.<br />

It correctly bundles React in production mode and optimizes the build for the best performance.

  

The build is minified and the filenames include the hashes.<br />

Your app is ready to be deployed!

  

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

  

## `Working`

  

The user's video data and the uploaded image is sent to the Python Flask backend. This can be done by clicking the button at the bottom of the Webpage.

The Video snapshot along with the uploaded image is sent to the backend the face is detected using haar feature based cascade classifier. More can be read [here](https://docs.opencv.org/3.4/d2/d99/tutorial_js_face_detection.html).
The detected faces are fed into [OpenFace](https://cmusatyalab.github.io/openface/) . OpenFace is a Python and [Torch](http://torch.ch/) implementation of face recognition with deep neural networks. The images and nn-model are read using openCV.

The working of the backend is:
![enter image description here](https://raw.githubusercontent.com/cmusatyalab/openface/master/images/summary.jpg)
Each detected face is converted into a 128 dimensional vector which represents the various features of faces. Then we find out the distance between the two vectors which is given out as the output for the Face recognizer. [ It is implemented as the dot of both the vectors so we are finding out the angle between them. Thus if both Faces are similar then they must point to same vector and thus the dot between them is 1 or angle between the vectors is 0]

In good light-conditions an accuracy of 0.90 can be achieved when the faces match. In case of poor light conditions a minimum of 0.75 accuracy must be set as a minimum for recognition.
When the face do not match the accuracy usually lies between 0.4~0.5.
In case face is not detected in the image the same will be shown in the webpage.