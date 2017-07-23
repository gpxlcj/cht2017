import os, errno
import random
import time
from shutil import copyfile
import argparse

def sample(sets, numbers, data_path):

    files_list = os.listdir(data_path)

    for s in range(sets):
        try:
            os.makedirs(os.path.join(data_path, 'sample/set'+str(s+1)))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print("Set {:d}".format(s+1))
        random.shuffle(files_list)
        sample_files = random.sample(files_list,  numbers)
        print(sample_files)
        #for f in sample_files:
        #    copyfile(os.path.join(data_path, f), os.path.join('sample/set'+str(s+1), f))
        for i in range(numbers):
            copyfile(os.path.join(data_path, sample_files[i]), os.path.join(data_path, 'sample/set'+str(s+1), str(i)+'.html'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str, help='path to the figure data')
    args = parser.parse_args()

    sample(10, 30, args.data_path)
