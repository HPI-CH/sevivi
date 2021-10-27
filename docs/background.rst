==========
Background
==========

This tool has been born out of research regarding human motion analysis with acceleration- and gyroscope sensors.
During our trials, we had kinect cameras running to gather movement skeletons from participants.
When analyzing trials, we often found the need to see how specific movements influenced the values from the acceleration
and gyroscope sensors.
However, we were unable to find a tool capable of showing the sensor data stream at the same time as the video from
the kinect cameras.

A first prototype showed great promise in the usefulness of such a tool, allowing us to easily create repetition
detection algorithms for our squat exercise trials.

As we could not find a tool like ours before, we decided to polish our research about it and create an open-source
version!

Concept
-------

Sevivi (SEnsor VIdeo VIsualizer) always uses exactly one video source.
Around the video, the data from any number of sensors can be shown.
An exemplary result can be seen below.
Data from multiple axes of the same sensor (e.g., the 3 accelerometer axes of the ankle sensor) is grouped into the same graph.

.. image:: docs/images/sevivi-screenshot.jpg
   :width: 600

To achieve the goal of having the sensor data playback be synchronous to the video playback, some method of synchronization is required.
Sevivi solves this problem by requiring data that is recorded on the same clock as the camera frames.
For a Kinect, this might be the tracked skeleton, for a smartphone, it could be the integrated IMU.

As we can now assume we have data synchronous to the video, our synchronization problem suddenly becomes much simpler.
We only need to align each sensor to the data from the video source, and voilà, we can simply render a graph of the data.

Let's take this very abstract information and translate it to understandable examples in the next section.

Concept Examples
----------------

While in theory sevivi could be use to combine any type of sensors, the most common use case is to use acceleration sensors.
This is because many acceleration can be derived from skeleton tracking, and many wearable sensors include an acceleration sensor,
leading to the necessary combination of two acceleration streams being available.

Kinect + IMU Sensors
********************

Kinect cameras record an RGB image and a depth image. With both of these data streams, it is possible to achieve very
good human skeleton tracking.
The result of this tracking is a stream of positions for each of the 24 joints the kinect tracks.
Now, let's assume we have collected data from an IMU on the wrist, and want to show its values during specific movements.

Our goal is to align the acceleration recorded by the wrist's IMU sensor with the wrist joint from the kinect.
As the kinect records positions, we need to calculate the second derivation of this data to arrive at acceleration as well.
Now, we can simply find the peak in the cross-correlation between the two data streams, and we know how much we need to shift
the data from the sensor in time to align it with the acceleration data from the kinect.

Smartphone IMU + IMU Sensors
****************************

As you probably know, every modern smartphone has an IMU.
There exist various apps that allow recording the IMU together with a video from the camera.
Sevivi specifically has support for the VideoIMUCapture_ app.
By shaking the camera together with the IMU sensors, distinctive spikes are recorded in the acceleration data.
These spikes can be used to align the camera IMU with the IMU sensors.
After shaking, the IMU sensors can be attached to whatever is to be tracked.
Again, we have the two acceleration streams to synchronize on.

Manual Synchronization
**********************

Sevivi also allows to manually set the offset between camera and your sensor data.
This is useful in case your desired sensor or camera has no data stream to synchronize on.

.. _VideoIMUCapture: https://github.com/DavidGillsjo/VideoIMUCapture-Android/