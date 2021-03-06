import logging

logging.basicConfig(format="[%(asctime)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
                    level=logging.INFO)
from sys import argv

from mapper import LaserModel
from mapper import Map
from mapper import ShowMap


from controller import Controller


from planner.planner import Planner
import time


def main():
    mrds_url = "localhost:50000"
    scale = 4
    x1 = -20
    y1 = -20
    x2 = 20
    y2 = 20
    width = x2 - x1
    height = y2 - y1
    # width = 100
    # height = 100
    max_distance = 30

    # TODO: parse arguments and print usage
    if len(argv) == 4:
        width = argv[1]
        height = argv[2]
    # else:
    #    print("Usage: mapper ")

    # occupancy_map = Map(width, height, scale)
    occupancy_map = Map(x1, y1, x2, y2, scale)
    map_shower = ShowMap(scale * width, scale * height, True)  # rows, cols, showgui

    controller = Controller(mrds_url)
    laser_angles = controller.get_laser_scan_angles()
    laser_model = LaserModel(laser_angles, max_distance)

    i= 0
    while i < 10:
        laser_scan = controller.get_laser_scan()
        pos, rot = controller.get_pos_and_orientation()
        laser_model.apply_model(occupancy_map, pos, rot, laser_scan)
        robot_indexes = occupancy_map.convert_to_grid_indexes(pos.x, pos.y)
        # TODO: p max getter
        map_shower.updateMap(occupancy_map.grid(), laser_model._p_max, robot_indexes[0], robot_indexes[1])
        # planner = GoalPlanner()
        # planner.find_frontiers(occupancy_map)
        time.sleep(0.01)
        i+=1


if __name__ == '__main__':
    import cProfile
    import pstats


    cProfile.run("main()", "mapper.stats")
    p = pstats.Stats('mapper.stats')
    p.sort_stats('cumtime')
    p.print_stats()
