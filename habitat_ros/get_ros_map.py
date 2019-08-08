#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

#This script geneartes a ros/rviz compatible map based on the specified Habitat scene's top-down map

import os
import argparse

import imageio
import numpy as np

import habitat
from habitat.tasks.nav.nav_task import NavigationEpisode, NavigationGoal
from habitat.utils.visualizations import maps
from habitat.utils.visualizations.maps import COORDINATE_MIN, COORDINATE_MAX

MAP_DIR = os.path.join("habitat_ros", "maps")
if not os.path.exists(MAP_DIR):
    os.makedirs(MAP_DIR)

def get_topdown_map(config_paths, map_name):

    config = habitat.get_config(config_paths=config_paths)
    dataset = habitat.make_dataset(
        id_dataset=config.DATASET.TYPE, config=config.DATASET
    )
    env = habitat.Env(config=config, dataset=dataset)
    env.reset()

    square_map_resolution = 5000
    top_down_map = maps.get_topdown_map(env.sim, map_resolution=(square_map_resolution,square_map_resolution))

    # Image containing 0 if occupied, 1 if unoccupied, and 2 if border (if
    # the flag is set)
    top_down_map[np.where(top_down_map == 0)] = 125
    top_down_map[np.where(top_down_map == 1)] = 255
    top_down_map[np.where(top_down_map == 2)] = 0

    imageio.imsave(os.path.join(MAP_DIR, map_name + ".pgm"), top_down_map)

    complete_name = os.path.join(MAP_DIR, map_name + ".yaml")
    f = open(complete_name, "w+")

    f.write("image: " + map_name + ".pgm\n")
    f.write("resolution: " + str((COORDINATE_MAX - COORDINATE_MIN) / square_map_resolution) + "\n")
    f.write("origin: [" + str(-1) + "," + str(-1) + ", 0.000000]\n")
    f.write("negate: 0\noccupied_thresh: 0.65\nfree_thresh: 0.196")
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-path", type=str, required=True)
    parser.add_argument("--map-name", type=str, required=True)
    args = parser.parse_args()
    get_topdown_map(args.config_path, args.map_name)

if __name__ == "__main__":
    main()
