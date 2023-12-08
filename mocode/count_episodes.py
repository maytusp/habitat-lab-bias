import os
import glob
import re
import json
import matplotlib.pyplot as plt
scene_path_list = glob.glob("val/content/*.json")
count_dict = {}
img_saved_dir = "figures"
if not(os.path.exists(img_saved_dir)):
    os.makedirs(img_saved_dir)
def get_two_decimal(pos):
    x, y, z = pos[0], pos[1], pos[2]
    x_str, y_str, z_str = "%.2f" % x, "%.2f" % y, "%.2f" % z
    x, y, z = float(x_str), float(y_str), float(z_str)
    return [x,y,z], [x_str, y_str, z_str]

def plot_hist_xy(x_list, y_list, fn):
    plt.hist2d(x_list, y_list)
    plt.title(f"{fn}")
    plt.xlabel("x-position")
    plt.ylabel("y-position")
    saved_path = os.path.join(img_saved_dir, f"{fn}.png")
    plt.savefig(saved_path)
    plt.close()

for fpath in scene_path_list:
    fn = os.path.basename(fpath)
    f = open(fpath)
    data = json.load(f)
    data = data['episodes']
    num_episodes = len(data)
    start_pos_dict = {}
    target_pos_dict = {}
    start_x_list = []
    start_y_list = []
    goal_x_list = []
    goal_y_list = []
    for episode in range(num_episodes):
        start_pos, start_pos_str = get_two_decimal(data[episode]['start_position'])
        goal_pos, goal_pos_str = get_two_decimal(data[episode]['goals'][0]['position'])
        # start_pos_str = ",".join(start_pos_str)
        start_x_list.append(start_pos[0])
        start_y_list.append(start_pos[1])
        goal_x_list.append(goal_pos[0])
        goal_y_list.append(goal_pos[1])
        # if start_pos_str not in start_pos_dict:
        #     start_pos_dict[start_pos_str] = 1
        # else:
        #     start_pos_dict[start_pos_str] += 1
            # print("ALREADY IN")
    # print(len(start_pos_dict))
    fn_start = f"{fn}_start"
    fn_goal = f"{fn}goal"
    plot_hist_xy(start_x_list, start_y_list, fn_start)
    plot_hist_xy(goal_x_list, goal_y_list, fn_goal)
    count_dict[fpath] = num_episodes
print(count_dict)
