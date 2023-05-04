import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cmd utility to sync two folders content')

    parser.add_argument('--src', required=True, help='source folder')
    parser.add_argument('--target', required=True, help='target folder')
    parser.add_argument('--interval_sec', required=True, help='interval of synchronization')
    parser.add_argument('--log', required=True, help='log file path')

    args = vars(parser.parse_args())

    print(args)
