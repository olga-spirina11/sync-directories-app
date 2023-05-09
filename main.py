import argparse
import logging
import os.path


def sync_dirs(src_dir, target_dir):
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='/Users/grigorii/Projects/sync_folder_app/app.log')
    logger = logging.getLogger("foo")
    logger.info('Some msg')

    logging.info("Some message")

    parser = argparse.ArgumentParser(description='cmd utility to sync two folders content')

    parser.add_argument('--src', required=True, help='source folder')
    parser.add_argument('--target', required=True, help='target folder')
    parser.add_argument('--interval-sec', required=True, help='interval of synchronization')
    parser.add_argument('--log', required=True, help='log file path')

    args = vars(parser.parse_args())

    print(args)

    sync_dirs(args.get('src'), args.get('target'))


# @pytest.fixture(autouse=True)
# def setup():
#     pass
#
#
# def tear_down():
#     pass


def test_creating_new_files(tmp_path):
    # Given ------------------------------------------------------------------------------------------------------------
    log = logging.getLogger(__name__)
    log.info(tmp_path)

    # Create source & target dirs
    dir_src = tmp_path / "source"
    dir_src.mkdir()

    dir_target = tmp_path / "target"
    dir_target.mkdir()

    # Create files
    dic = {
        'f1.txt': 'foo\n',
        'f2.txt': 'bar\n',
        'f3.txt': 'foo_2\n'
    }
    for k, v in dic.items():
        with open(dir_src.joinpath(k), 'a') as f:
            f.write(v)

    # When -------------------------------------------------------------------------------------------------------------
    sync_dirs('source', 'target')

    # Then -------------------------------------------------------------------------------------------------------------
    assert os.path.exists(dir_target / 'f1.txt')
    with open(dir_target / 'f1.txt', 'r') as f:
        content = f.read()
    assert content == 'foo\n'
    # TODO: the same with f2 and f3


def test_change_file_content(tmp_path):
    # given
    dir_src = tmp_path / "source"
    dir_src.mkdir()

    dir_target = tmp_path / "target"
    dir_target.mkdir()



    # when
    sync_dirs('source', 'target')

    #then


