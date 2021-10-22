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

.. code-block::bash

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

Common Options
**************

.. code-block::

    stacking_direction = "horizontal"
    draw_ticks = false
    add_magnitude = false
    use_parallel_image_ingestion = true
    plotting_method = "moving_vertical_line"



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

As an example, to manually create a VideoRenderer that renders the example provided in the repository