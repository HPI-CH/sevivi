from sevivi import video_renderer_from_csv_files, read_configs


def test_plain_video_render(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/manual_sync.toml",))
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()


def test_azure_video_render(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()
