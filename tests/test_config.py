from sevivi.config.config_reader import read_configs


def test_get_missing_files_all_available(run_in_repo_root):
    config = read_configs(
        ("test_files/test-data-configs/kinect_sync_3d_hand_movement.toml",)
    )
    assert len(config.get_missing_files()) == 0


def test_get_missing_files_four_missing(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/missing_files.toml",))
    missing = config.get_missing_files()
    assert len(missing) == 4
    assert "test_files/videos/todo.mp4" in missing
    assert "test_files/todo0.csv.gz" in missing
    assert "test_files/todo1.csv.gz" in missing
    assert "test_files/todo2.csv.gz" in missing
