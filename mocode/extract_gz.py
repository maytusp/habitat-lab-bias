import gzip
import shutil
import os
scene_dir = "data/datasets/pointnav/gibson_eval_on_train/v1/val/content"
file_list = os.listdir(scene_dir)
for fn_gz in file_list:
    fn = fn_gz.replace('.gz', '')
    fn = os.path.join(scene_dir, fn)
    with gzip.open(f'{fn}.gz', 'rb') as f_in:
        with open(f'{fn}', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)