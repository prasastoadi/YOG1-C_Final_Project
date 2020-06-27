import pandas as pd

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