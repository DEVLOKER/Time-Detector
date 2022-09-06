# Time-Detector
Python program for calculating time of analog clock image based on clockwise angles.
- firstly, searching of analog clock center, and drawing circle on it.
- after that, draw clockwise lines from center of analog clock.
- calculate the length of each clockwise, the short one for hours, and the longest for minutes.
- finally, calculate time (Hours:minutes) based on drawed clockwise lines angles.

## Used Modules
`pip install opencv-python numpy`

## Available Scripts
In the project directory, you can run:
`python TimeDetector.py <path/to/image>`

example:
`python TimeDetector.py clocks/clock-1.png`

## Results

| command        | time result           | image  |
| ------------- |:-------------:| -----:|
| `python TimeDetector.py clocks/clock-01.png` | Time is `06:34` | ![clock-01](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-01.png?raw=true "Time is 06:34") |
| `python TimeDetector.py clocks/clock-02.png` | Time is `06:14` | ![clock-02](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-02.png?raw=true "Time is 06:14") |
| `python TimeDetector.py clocks/clock-03.jpg` | Time is `09:32` | ![clock-03](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-03.jpg?raw=true "Time is 09:32") |
| `python TimeDetector.py clocks/clock-04.jpg` | Time is `04:14` | ![clock-04](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-04.jpg?raw=true "Time is 04:14") |
| `python TimeDetector.py clocks/clock-05.jpg` | Time is `12:11` | ![clock-05](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-05.jpg?raw=true "Time is 12:11") |
| `python TimeDetector.py clocks/clock-06.jpg` | Time is `10:40` | ![clock-06](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-06.jpg?raw=true "Time is 10:40") |
| `python TimeDetector.py clocks/clock-07.jpg` | Time is `01:45` | ![clock-07](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-07.jpg?raw=true "Time is 01:45") |
| `python TimeDetector.py clocks/clock-08.jpg` | Time is `10:08` | ![clock-08](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-08.jpg?raw=true "Time is 10:08") |
| `python TimeDetector.py clocks/clock-09.jpg` | Time is `10:09` | ![clock-09](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-09.jpg?raw=true "Time is 10:09") |
| `python TimeDetector.py clocks/clock-10.jpg` | Time is `12:20` | ![clock-10](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-10.jpg?raw=true "Time is 12:20") |
| `python TimeDetector.py clocks/clock-11.jpg` | Time is `01:52` | ![clock-11](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-11.jpg?raw=true "Time is 01:52") |
| `python TimeDetector.py clocks/clock-12.jpg` | Time is `02:49` | ![clock-12](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-12.jpg?raw=true "Time is 02:49") |
| `python TimeDetector.py clocks/clock-13.jpg` | Time is `01:50` | ![clock-13](https://github.com/DEVLOKER/Time-Detector/blob/main/results/clock-13.jpg?raw=true "Time is 01:50") |
