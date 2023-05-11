import argparse
import hashlib
import logging
import os
import shutil
import time

log = logging.getLogger(__name__)


# Function for compare 2 files by hash
def compare_files(file1, file2):
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False


# Function for synchronization
def sync_dirs(dir_src, dir_target):
    log.debug(f'Enter sync_dirs: dir_src={dir_src}, dir_target={dir_target}')
    # if item is in src, but not in target
    for item in os.listdir(dir_src):
        src_path = os.path.join(dir_src, item)
        target_path = os.path.join(dir_target, item)
        if os.path.isfile(src_path):
            if not os.path.exists(target_path):
                shutil.copy2(src_path, dir_target)
                log.info(f'{src_path} is copied')
            # if files in src and target have similar names - compare them by hash and replace if they are different
            elif compare_files(src_path, target_path):
                log.debug(f'{src_path} is up to date')
            else:
                shutil.copy2(src_path, dir_target)
                log.info(f'{src_path} is copied')
        # if there are subdirs in dirs - coping if subdir doesn't exist and sync content if exists (recursively)
        elif os.path.isdir(src_path):
            if not os.path.exists(target_path):
                shutil.copytree(src_path, target_path)
                log.info(f'{src_path} is copied')
            else:
                sync_dirs(src_path, target_path)
    # if there are files in target, but not in src - remove them from target
    for item in os.listdir(dir_target):
        src_path = os.path.join(dir_src, item)
        target_path = os.path.join(dir_target, item)
        if os.path.isfile(target_path):
            if not os.path.exists(src_path):
                os.remove(target_path)
                log.info(f'{target_path} is deleted')
        # the same with subdirs
        elif os.path.isdir(target_path):
            if not os.path.exists(src_path):
                shutil.rmtree(target_path)
                log.info(f'{target_path} is deleted')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cmd utility to sync two folders content')
    parser.add_argument('--src', required=True, help='source folder')
    parser.add_argument('--target', required=True, help='target folder')
    parser.add_argument('--interval_sec', required=True, help='interval of synchronization')
    parser.add_argument('--log', required=True, help='log file path')

    args = vars(parser.parse_args())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
        handlers=[
            logging.FileHandler(args.get('log')),
            logging.StreamHandler()
        ]
    )
    log = logging.getLogger(__name__)

    while True:
        log.info('Synchronization iteration')
        sync_dirs(args.get('src'), args.get('target'))
        time.sleep(int(args.get('interval_sec')))


def test_creating_new_files(tmp_path):
    # Given ------------------------------------------------------------------------------------------------------------
    dir_src = tmp_path / 'source'
    os.mkdir(dir_src)

    dir_target = tmp_path / 'target'
    os.mkdir(dir_target)

    # Create files in src
    dic = {
        'f1.txt': 'foo\n',
        'f2.txt': 'bar\n',
        'f3.txt': 'foo_2\n'
    }

    for k, v in dic.items():
        with open(dir_src.joinpath(k), 'a') as f:
            f.write(v)

    # Create subdir with file in src
    os.mkdir(os.path.join(dir_src, 'sub_dir'))

    with open(os.path.join(dir_src, 'sub_dir', 'f4.txt'), 'w') as f:
        f.write('Hello, world!\n')

    # When -------------------------------------------------------------------------------------------------------------

    sync_dirs(dir_src, dir_target)

    # Then -------------------------------------------------------------------------------------------------------------
    for k, v in dic.items():
        assert os.path.exists(dir_target / k)
        with open(dir_target / k, 'r') as f:
            content = f.read()
        assert content == v

    assert os.path.exists(dir_target / 'sub_dir')
    assert os.path.exists(dir_target / 'sub_dir' / 'f4.txt')
    with open(dir_target / 'sub_dir' / 'f4.txt', 'r') as f:
        content = f.read()
    assert content == 'Hello, world!\n'


def test_change_file_content(tmp_path):
    # Given ------------------------------------------------------------------------------------------------------------
    dir_src = tmp_path / 'source'
    os.mkdir(dir_src)

    dir_target = tmp_path / 'target'
    os.mkdir(dir_target)

    # Create files in src
    dic = {
        'f1.txt': 'foo\n',
        'f2.txt': 'bar\n',
        'f3.txt': 'foo_2\n'
    }

    for k, v in dic.items():
        with open(dir_src.joinpath(k), 'a') as f:
            f.write(v)

    # Create subdir with file in src
    os.mkdir(os.path.join(dir_src, 'sub_dir'))

    with open(os.path.join(dir_src, 'sub_dir', 'f4.txt'), 'w') as f:
        f.write('Hello, world!\n')

    # Create files with similar names, but different content in target
    dic_2 = {
        'f1.txt': 'Hello\n',
        'f2.txt': 'Guten Tag\n',
        'f3.txt': 'Danke\n'
    }

    for k, v in dic_2.items():
        with open(dir_target.joinpath(k), 'a') as f:
            f.write(v)

    # Create subdir with file in target
    os.mkdir(os.path.join(dir_target, 'sub_dir'))

    with open(os.path.join(dir_target, 'sub_dir', 'f4.txt'), 'w') as f:
        f.write('Hello, Veeam!\n')

    # When -------------------------------------------------------------------------------------------------------------

    sync_dirs(dir_src, dir_target)

    # Then -------------------------------------------------------------------------------------------------------------
    for k, v in dic.items():
        assert os.path.exists(dir_target / k)
        with open(dir_target / k, 'r') as f:
            content = f.read()
        assert content == v

    assert os.path.exists(dir_target / 'sub_dir')
    assert os.path.exists(dir_target / 'sub_dir' / 'f4.txt')
    with open(dir_target / 'sub_dir' / 'f4.txt', 'r') as f:
        content = f.read()
    assert content == 'Hello, world!\n'


def test_delete_file(tmp_path):
    # Given ------------------------------------------------------------------------------------------------------------
    dir_src = tmp_path / 'source'
    os.mkdir(dir_src)

    dir_target = tmp_path / 'target'
    os.mkdir(dir_target)

    # Create files in src
    dic = {
        'f1.txt': 'foo\n',
        'f2.txt': 'bar\n',
        'f3.txt': 'foo_2\n'
    }

    for k, v in dic.items():
        with open(dir_src.joinpath(k), 'a') as f:
            f.write(v)

    # Create subdir with file in src
    os.mkdir(os.path.join(dir_src, 'sub_dir'))

    with open(os.path.join(dir_src, 'sub_dir', 'f4.txt'), 'w') as f:
        f.write('Hello, world!\n')

    # Create files with different names in target
    dic_2 = {
        'f5.txt': 'Hello\n',
        'f6.txt': 'Guten Tag\n',
        'f7.txt': 'Danke\n'
    }

    for k, v in dic_2.items():
        with open(dir_target.joinpath(k), 'a') as f:
            f.write(v)

    # Create subdir with file in target
    os.mkdir(os.path.join(dir_target, 'sub_dir_2'))

    with open(os.path.join(dir_target, 'sub_dir_2', 'f8.txt'), 'w') as f:
        f.write('Hello, Veeam!\n')

    # When -------------------------------------------------------------------------------------------------------------

    sync_dirs(dir_src, dir_target)

    # Then -------------------------------------------------------------------------------------------------------------
    for k, v in dic.items():
        assert os.path.exists(dir_target / k)
        with open(dir_target / k, 'r') as f:
            content = f.read()
        assert content == v

    assert os.path.exists(dir_target / 'sub_dir')
    assert os.path.exists(dir_target / 'sub_dir' / 'f4.txt')
    with open(dir_target / 'sub_dir' / 'f4.txt', 'r') as f:
        content = f.read()
    assert content == 'Hello, world!\n'

    for k in dic_2.keys():
        assert not os.path.exists(dir_target / k)

    assert not os.path.exists(dir_target / 'sub_dir_2')
