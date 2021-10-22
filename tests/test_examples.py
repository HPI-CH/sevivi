def test_manually_creating_video_renderer(run_in_repo_root):
    import pandas as pd

    from sevivi.config import RenderConfig, ManuallySynchronizedSensorConfig
    from sevivi.image_provider import (
        GraphImageProvider,
        VideoImuCaptureAppImageProvider,
    )
    from sevivi.video_renderer import VideoRenderer

    video_provider = VideoImuCaptureAppImageProvider(
        video_path="test_files/videos/imu_sync.mp4",
        imu_pb_path="test_files/sensors/video_imu_capture_app/video_meta.pb3",
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
