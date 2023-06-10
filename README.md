# Time-Detector
Python program for calculating time of analog clock image based on clockwise angles.
- firstly, searching of analog clock center, and drawing circle on it.
- after that, draw clockwise lines from center of analog clock.
- calculate the length of each clockwise, the short one for hours, and the longest for minutes.
- finally, calculate time (Hours:minutes) based on drawn clockwise lines angles.

![](https://github.com/DEVLOKER/Time-Detector/blob/main/static/img/tutorial.png)

## Used Modules
`pip install opencv-python numpy flask`

## Run it
- In the project directory, type: `flask --app app run`
- In browser navigate to: `http://127.0.0.1:5000`

![](https://github.com/DEVLOKER/Time-Detector/blob/main/screenshots/time-detector.gif)

## Results

![](https://github.com/DEVLOKER/Time-Detector/blob/main/screenshots/time-detector.jpg)
