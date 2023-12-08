import os
from typing import TYPE_CHECKING, Union, cast

import matplotlib.pyplot as plt
import numpy as np
from habitat.config import read_write
import habitat
from habitat.config.default_structured_configs import (
    CollisionsMeasurementConfig,
    FogOfWarConfig,
    TopDownMapMeasurementConfig,
)
from habitat.core.agent import Agent
from habitat.tasks.nav.nav import NavigationEpisode, NavigationGoal
from habitat.tasks.nav.shortest_path_follower import ShortestPathFollower
from habitat.utils.visualizations import maps
from habitat.utils.visualizations.utils import (
    images_to_video,
    observations_to_image,
    overlay_frame,
)
from habitat_sim.utils import viz_utils as vut

# Quiet the Habitat simulator logging
os.environ["MAGNUM_LOG"] = "quiet"
os.environ["HABITAT_SIM_LOG"] = "quiet"

if TYPE_CHECKING:
    from habitat.core.simulator import Observations
    from habitat.sims.habitat_simulator.habitat_simulator import HabitatSim


output_path = "gibson_maps/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

def example_pointnav_draw_target_birdseye_view():
    # Define NavigationEpisode parameters
    goal_radius = 0.5
    goal = NavigationGoal(position=[10, 0.25, 10], radius=goal_radius)
    agent_position = [0, 0.25, 0]
    agent_rotation = -np.pi / 4

    # Create dummy episode for birdseye view visualization
    dummy_episode = NavigationEpisode(
        goals=[goal],
        episode_id="dummy_id",
        scene_id="dummy_scene",
        start_position=agent_position,
        start_rotation=agent_rotation,  # type: ignore[arg-type]
    )

    agent_position = np.array(agent_position)
    # Draw birdseye view
    target_image = maps.pointnav_draw_target_birdseye_view(
        agent_position,
        agent_rotation,
        np.asarray(dummy_episode.goals[0].position),
        goal_radius=dummy_episode.goals[0].radius,
        agent_radius_px=25,
    )
    plt.imshow(target_image)
    plt.title("pointnav_target_image.png")
    plt.show()
    plt.savefig(os.path.join(output_path, "test_pointnav_target_image.png"))


def example_get_topdown_map(scene_name="Woonsocket"):
    # Create habitat config
    config = habitat.get_config(
        config_path="benchmark/nav/pointnav/pointnav_gibson_rgb_eval_on_train.yaml"
    )
    # print("BEFORE", config)
    if scene_name != "":
        with read_write(config):
            config.habitat.dataset.content_scenes = [f'{scene_name}']
    # print("AFTER", config)
    # Create dataset
    dataset = habitat.make_dataset(
        id_dataset=config.habitat.dataset.type, config=config.habitat.dataset
    )
    # print("DATASET", dataset)
    # Create simulation environment
    with habitat.Env(config=config, dataset=dataset) as env:
        # Load the first episode
        env.reset()
        # Generate topdown map
        top_down_map = maps.get_topdown_map_from_sim(
            cast("HabitatSim", env.sim), map_resolution=256
        )
        # save a raw map before recoloring
        np.save(os.path.join(output_path, f"{scene_name}_raw_map.npy"), top_down_map)
        recolor_map = np.array(
            [[255, 255, 255], [128, 128, 128], [0, 0, 0]], dtype=np.uint8
        )
        # By default, `get_topdown_map_from_sim` returns image
        # containing 0 if occupied, 1 if unoccupied, and 2 if border
        # The line below recolors returned image so that
        # occupied regions are colored in [255, 255, 255],
        # unoccupied in [128, 128, 128] and border is [0, 0, 0]
        top_down_map = recolor_map[top_down_map]
        
        plt.imshow(top_down_map)
        plt.title(f"{scene_name} map")
        plt.show()
        plt.savefig(os.path.join(output_path, f"{scene_name}_map.png"))

if __name__ == "__main__":
    # example_pointnav_draw_target_birdseye_view()
    scene_names_file = open("data/datasets/pointnav/gibson/v1/scene_names.txt")
    for scene_name in scene_names_file:
        scene_name = scene_name.strip()
        print(f"Getting the map of {scene_name}")
        example_get_topdown_map(scene_name)



