import argparse
import os
import logging

import pytest

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='/Users/grigorii/Projects/sync_folder_app/app.log')
    logger = logging.getLogger("foo")
    logger.info('Some msg')

    logging.info("Some message")

    parser = argparse.ArgumentParser(description='cmd utility to sync two folders content')

    parser.add_argument('--src', required=True, help='source folder')
    parser.add_argument('--target', required=True, help='target folder')
    parser.add_argument('--interval_sec', required=True, help='interval of synchronization')
    parser.add_argument('--log', required=True, help='log file path')

    args = vars(parser.parse_args())

    print(args)


# @pytest.fixture(autouse=True)
# def setup():
#     pass
#
#
# def tear_down():
#     pass


def test_smth(tmp_path):
    log = logging.getLogger(__name__)
    log.info('Some msg')

    # print(f'tmp_path={tmp_path}')
    d = tmp_path / "sub"
    d.mkdir()

    assert False
