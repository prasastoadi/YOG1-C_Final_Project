import os
import pandas as pd

def create_dirs(dirs):
    """
    dirs - a list of directories to create if these directories are not found
    :param dirs:
    :return exit_code: 0:success -1:failed
    """
    try:
        for dir_ in dirs:
            if not os.path.exists(dir_):
                os.makedirs(dir_)
        return 0
    except Exception as err:
        print("Creating directories error: {0}".format(err))
        exit(-1)

def extract_dir_to_df(root_dir: str)-> pd.DataFrame:
    dirnames = os.listdir(root_dir)
    dirnames = [dire for dire in dirnames 
                if os.path.isdir(os.path.join(root_dir, dire))]
    data = {'filepath': [],
            'class': []}

    for dir_ in sorted(dirnames):
        clsname = dir_.split('.')[0]
        list_dir = os.listdir(os.path.join(root_dir, dir_))
        for fname in list_dir:
            fullpath = os.path.join(root_dir, dir_, fname)
            if not os.path.isfile(fullpath):
                continue
            data['filepath'].append(fullpath)
            data['class'].append(clsname)
    return pd.DataFrame(data)