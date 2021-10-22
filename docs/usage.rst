==========
Usage
==========

Sevivi (SEnsor VIdeo VIsualizer) has two modes of operation.
It can either work as a command-line tool, if you use supported input data, or you can use sevivi as a library,
instantiating the input data manually and improving the results by supplementing, for example, the algorithm used
to synchronize the sensors to the video.

Installation
------------

Simply run

.. code-block:: shell

    pip install sevivi


to install sevivi.

Command-Line Usage
------------------

Installing sevivi makes the ``sevivi`` CLI available as a python program.
``sevivi`` has the following command line syntax:

.. code-block::

    usage: sevivi [-h] [--output TARGET_FILE_PATH] config [config ...]

    positional arguments:
      config                Configuration files. Later files overwrite earlier ones. Only the last video section is used. All given sensor configs are interpreted as a list, rather
                            than overwriting earlier configuration.

    optional arguments:
      -h, --help            show this help message and exit
      --output TARGET_FILE_PATH
                            Set the output file. Overwrites config value.


As described above, sevivi supports multiple config files.
Each later config file overwrites the configuration from previous configuration files.
There is one exception for this: the configuration for sensor data sources.
Every sensor data source is appended to the list of all sources instead.

Configuration files are comprised of general options that apply to the entire tool,
a video configuration section, and a number of sensor source configuration sections.

Complete Example
****************

More options and descriptions for each section can be found below.
This is a single example for a full configuration file that can render one
of the examples included in the repository.

.. code-block:: toml

    target_file_path = "camera_sevivi.avi"

    [[video]]
    type = "kinect"
    path = "test_files/videos/joint_synchronization_walking.mp4"
    skeleton_path_3d = "test_files/skeletons/joint_synchronization_walking/positions_3d.csv.gz"

    [[sensor]]
    type = "joint-synced"
    sensor_sync_column_selection = ["Acc_X", "Acc_Y", "Acc_Z"]
    camera_joint_sync_column_selection = ["SPINE_CHEST (x)", "SPINE_CHEST (y)", "SPINE_CHEST (z)"]
    path = "test_files/sensors/joint_synchronization_walking/LF.csv.gz"

    [[sensor]]
    type = "joint-synced"
    sensor_sync_column_selection = ["Acc_X", "Acc_Y", "Acc_Z"]
    camera_joint_sync_column_selection = ["SPINE_CHEST (x)", "SPINE_CHEST (y)", "SPINE_CHEST (z)"]
    path = "test_files/sensors/joint_synchronization_walking/RF.csv.gz"



Common Options
**************

These options are common to the whole tool, and can always be set.
They must be in the root section, as shown in the complete example.

.. code-block:: toml

    # May be 'vertical' to put all sensor graphs below the video, or 'horizontal' to put the sensor graphs left and right of
    # the center of the video
    stacking_direction = "horizontal"
    # set to true to draw ticks with scale, or set to false. false is faster.
    draw_ticks = false
    # currently, the only supported plotting method is moving_vertical_line
    plotting_method = "moving_vertical_line"
    # Set the four character codec name to save in the avi container
    fourcc_codec = "MJPG"
    # Set the target video file path
    target_file_path = "./sevivi.mp4"


Video Options
*************

We support different video input formats, each specified by its unique ``type``.
You can either add your video as a separate config file to the CLI call (makes it easy to switch out)
or add the section into one main config file.

* Example video section for videos without associated synchronization data:

.. code-block:: toml

    [[video]]
    # source video file
    path = "test_files/raw.mkv"
    # type is "raw" as this video doesn't have any data associated with it
    type = "raw"

* Example video section for videos from an Azure Kinect with exported skeleton data:

.. code-block:: toml

    [[video]]
    # path to the input video
    path = "test_files/kinect.mkv"
    # skeleton data. skeleton data can be created by @justamad
    skeleton_path_3d = "test_files/kinect.csv.gz"
    # azure kinect config type
    type = "kinect"

* Example video section for videos created with VideoImuCapture_:

.. code-block:: toml

    [[video]]
    # path to the input video
    path = "test_files/videos/imu_sync.mp4"
    # specify the path to the IMU data; this is a protobuf file from the VideoImuCapture app
    imu_path = "test_files/sensors/video_imu_capture_app/video_meta.pb3"
    # config type to specify this is from the VideoImuCapture app
    type = "videoImuApp"

* Example video section for videos that have IMU data associated in some other way:

.. code-block:: toml

    [[video]]
    # video file path
    path = "test_files/videos/imu_sync.mp4"
    # specify this is a video with IMU data attached
    type = "imu"
    # specify the path to the IMU data
    imu_path = "test_files/kinect_imu.csv.gz"

Sensor Options
**************

Last but not least, the input sensors need to be specified.
Each sensor can be added by adding another ``[[sensor]]`` block.
Some options are common to all sensors:

.. code-block:: toml

    [[sensor]]
    # Only data after this time (measured in unshifted sensor time) is included
    start_time = "00:00:00.000000"
    # Only data before this time (measured in unshifted sensor time) is included
    end_time = "00:00:01.000000"

Again, a number of types with specific options are available:

* Manual Synchronization -- this can be useful to, e.g., synchronize a sensor that doesn't
  include the right modality to be synchronized against the camera

.. code-block:: toml

    [[sensor]]
    # how many seconds into the future the data from this sensor should be move to align its start with the video start.
    # this value can be negative.
    offset_seconds = 123.4
    # A manually synchronized sensor
    type = "manually-synced"
    # path to the data of this sensor
    path = "test_files/manual_imu.csv.gz"

* Camera IMU synchronization: This sensor configuration can be used to synchronize sensors by their data to camera data

.. code-block:: toml

    [[sensor]]
    # This is a sensor synchronized to the IMU of the camera.
    type = "camera-imu-synced"
    # Select the columns **from the sensor** that should be aligned to the columns **from the camera**
    sensor_sync_column_selection = ["AccX", "Accel Y"]
    # Select the columns **from the camera** that should be aligned to the columns **from the sensor**
    camera_imu_sync_column_selection = ["AccX", "Accel Y"]
    # Specify the path to the data
    path = "test_files/sensor_imu.csv.gz"



Usage as a library
------------------

To use sevivi as a library, which is useful to change implementations, add some, or just because you don't feel like
writing configuration files, keep in mind that the main interface to sevivi is the ``VideoRenderer`` class.
Once you have created a ``VideoRenderer`` instance, you can call the ``render_video`` method to start writing the result.

To create the instance, you need to provide a ``VideoImageProvider`` subclass
and a ``GraphImageProvider`` for each sensor you want to add to the video.

The following ``VideoImageProvider`` subclasses are available out of the box:

* AzureProvider
* PlainVideoImageProvider
* ImuCameraImageProvider
* VideoImuCaptureAppImageProvider

As an example, to manually create a VideoRenderer that renders one of the examples provided in the repository, the following code
can be used:

.. code-block:: python


    import pandas as pd

    from sevivi.config import RenderConfig, ManuallySynchronizedSensorConfig
    from sevivi.image_provider import GraphImageProvider, VideoImuCaptureAppImageProvider
    from sevivi.video_renderer import VideoRenderer

    video_provider = VideoImuCaptureAppImageProvider(
        video_path="test_files/videos/imu_sync.mp4",
        imu_pb_path="test_files/sensors/video_imu_capture_app/video_meta.pb3"
    )

    # create a GraphImageProvider for each of your sensors
    sensor_config = ManuallySynchronizedSensorConfig()
    sensor_config.offset_seconds = 0.0
    sensor_config.name = "Human-Readable Name"
    sensor_config.path = "test_files/sensors/imu_synchronization/camera_imu.csv.gz"
    data = pd.read_csv(sensor_config.path, index_col=0, parse_dates=True)
    graph_image_provider = GraphImageProvider(data, sensor_config)

    # render the video
    renderer = VideoRenderer(RenderConfig(), video_provider, [graph_image_provider])
    renderer.render_video()


.. _VideoIMUCapture: https://github.com/DavidGillsjo/VideoIMUCapture-Android/