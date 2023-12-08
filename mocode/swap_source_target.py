# This is for creating a set of episodes using the training scene by swapping source and target positions
import json
import numpy
import gzip
import os

def test_load(scene_path):
    with gzip.open(scene_path, 'rt') as zipfile:
        data = json.load(zipfile)
    print(data['episodes'][0])

# test_load(os.path.join(new_scene_dir, "Adrian.json.gz"))
# test_load(scene_path)

def create_new_episodes(scene_path, new_scene_dir):
    scene_filename = os.path.basename(scene_path)
    with gzip.open(scene_path, 'rt') as zipfile:
        data = json.load(zipfile)    
    data = data['episodes']
    data_new = data.copy()
    num_episodes = len(data)

    start_x_list = []
    start_y_list = []
    goal_x_list = []
    goal_y_list = []

    for episode in range(num_episodes):
        start_pos_ori = data[episode]['start_position']
        goal_pos_ori = data[episode]['goals'][0]['position']

        start_pos_new = goal_pos_ori
        goal_pos_new = start_pos_ori

        data_new[episode]['start_position'] = start_pos_new
        data_new[episode]['goals'][0]['position'] = goal_pos_new

    new_scene = {'episodes': data_new}
    new_scene_path = os.path.join(new_scene_dir, scene_filename)

    if not(os.path.exists(new_scene_dir)):
        os.makedirs(new_scene_dir)
    # print(new_scene)
    with gzip.open(new_scene_path, 'wt') as new_zipfile:
        json.dump(new_scene, new_zipfile)

if __name__ == "__main__":
    scene_name_file = open('data/datasets/pointnav/gibson/v1/scene_names.txt')
    scene_dir = "data/datasets/pointnav/gibson_eval_on_train/v1/train/content/"
    new_scene_dir = "data/datasets/pointnav/gibson_eval_on_train/v1/val/content/"    
    for scene_name in scene_name_file:
        scene_name = scene_name.strip()
        scene_path = os.path.join(scene_dir, f"{scene_name}.json.gz")
        print(f"Creating new episodes from {scene_name}")
        create_new_episodes(scene_path, new_scene_dir)
