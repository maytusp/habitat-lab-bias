import os
import matplotlib.pyplot as plt
import numpy as np
eval_on_train_dir = "video_pointnav_gibson_rgb_eval_on_train/"
eval_on_val_dir = "video_pointnav_gibson_rgb_eval/"


eval_on_train_swap_dir = "video_pointnav_gibson_rgb_eval_on_train_swap_position/"


def count_spl(dir, name="eval on train scenes"):
    file_list = os.listdir(dir)
    spl_list = []
    perfect_spl = 0
    for fn in file_list:
        _, after_spl_txt = fn.strip().split("-spl=")
        spl = float(after_spl_txt[0:4])
        spl_list.append(spl)
        if spl == 1.00:
            perfect_spl+=1
    bins = [i/100 for i in range(0,101)]
    plt.hist(spl_list, bins=bins, density=True)
    plt.title(f"SPL distribution ({name})")
    plt.savefig(f"{name}.png")
    plt.close()
    perfect_spl = perfect_spl / len(spl_list)
    return spl_list, np.mean(spl_list), np.std(spl_list), perfect_spl
spl_train, mean_train, std_train, perfect_spl_train = count_spl(eval_on_train_dir, name="eval on all scenes")
spl_train_swap, mean_train_swap, std_train_swap, perfect_spl_train_swap = count_spl(eval_on_train_swap_dir, name="eval on all scenes (swap S-T)")
# spl_val, mean_val, std_val, perfect_spl_val = count_spl(eval_on_val_dir, name="eval on unseen scenes")
print(f"Eval on seen scenes: {mean_train}+-{std_train} \n {perfect_spl_train}")
print(f"Eval on swap scenes: {mean_train_swap}+-{std_train_swap} \n {perfect_spl_train_swap}")
# print(f"Eval on unseen scenes: {mean_val}+-{std_val} \n {perfect_spl_val}")