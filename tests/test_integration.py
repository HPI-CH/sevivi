from sevivi import video_renderer_from_csv_files, read_configs

from sys import platform as sys_pf
import matplotlib

if sys_pf == "darwin":
    matplotlib.use("TkAgg")


def test_plain_video_render(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/manual_sync.toml",))
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()


def test_azure_video_render(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()


def test_video_imu_capture_app_render(run_in_repo_root):
    config = read_configs(
        ("test_files/test-data-configs/video_imu_capture_app_sync.toml",)
    )
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()


def test_camera_imu_render(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/imu_sync.toml",))
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()
