==============
sevivi readme
==============


.. image:: https://img.shields.io/pypi/v/sevivi.svg
        :target: https://pypi.python.org/pypi/sevivi

.. image:: https://github.com/hpi-dhc/sevivi/actions/workflows/deploy.yml/badge.svg
        :target: https://github.com/hpi-dhc/sevivi/actions/workflows/deploy.yml?query=branch%main

.. image:: https://github.com/hpi-dhc/sevivi/actions/workflows/all.yml/badge.svg
        :target: https://github.com/hpi-dhc/sevivi/actions/workflows/all.yml?query=branch%3Amain

.. image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/enra64/a31baa6cd608054767ab49693000dbfd/raw/sevivi_coverage_main.json
        :target: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/enra64/a31baa6cd608054767ab49693000dbfd/raw/sevivi_coverage_main.json

.. image:: https://readthedocs.org/projects/sevivi/badge/?version=latest
        :target: https://sevivi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
     :target: https://github.com/hpi-dhc/sevivi/blob/master/CODE_OF_CONDUCT.md

sevivi is a python package and command line tool to generate videos of sensor data graphs synchronized to a video of the sensor movement.

* Free software: MIT license
* Documentation: https://sevivi.readthedocs.io.


Features
--------

Sevivi is designed to render plots of sensor data next to a video that was taken synchronously, synchronizing the sensor
data precisely to the video.
It allows you to investigate why certain patterns occur in your sensor data based on the exact moment in the video.

It can be used as a command-line program or a library for more advanced usage, and the following video types are supported:

* Render sensor data with IMUs next to a video with skeleton data
* Render sensor data with IMUs next to a video provided together with IMU data
* Render arbitrary sensor data next to a video, synchronizing with manual offsets

Installation
------------

Install the package from pypi:

.. code:: shell

    pip install sevivi

Usage
-----

Check out the usage documentation, please!
If you just want to render a video to get started, keep reading.
After you have downloaded the repository, you can use our test data. Run the following:

.. code-block:: shell

    git clone git@github.com:your_name_here/sevivi.git
    cd sevivi/
    pip install sevivi
    sevivi test-files/test-data-configs/kinect_sync_squatting.toml

If you want to use sevivi as a library, you can copy-paste the following code into your project.
You should download our test files for this to run immediately.

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



Template Credits
----------------

This package was created with Cookiecutter_ and the `pyOpenSci/cookiecutter-pyopensci`_ project template, based off `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`pyOpenSci/cookiecutter-pyopensci`: https://github.com/pyOpenSci/cookiecutter-pyopensci
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
