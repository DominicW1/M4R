import os
import neat
import numpy as np
import pandas as pd
from tube_network import Station, Platform
import visualise as visualise
import datetime as dt
from network_tools import *
from get_timetables import station_objs
from time import perf_counter
from stations import station_dict
import sys
import multiprocessing
import cProfile
import pstats

def eval_genomes(genomes, config, winner=0):
    for genome_id, genome in genomes:
        eval_genomes_threaded(genome, config, winner=winner)

def eval_genomes_threaded(genome, config, winner=0):
    reset_stations(station_objs)
    genome.fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    starting_station_name = "Morden"
    total_visited = 1
    new_station = station_objs[starting_station_name]
    # initiate clock
    start_time = dt.time(5, 16)
    clock = dt.datetime.combine(dt.date.min, start_time)
    # loop over time
    max_time = dt.datetime.combine(dt.date.min + dt.timedelta(days=1), dt.time(1, 15))
    previous_stations = []
    current_direction = "up"
    current_line = "northern"
    new_station.visit(genome, current_line)
    if winner:
        # pass
        print(f"Station: {new_station}, Fitness: {genome.fitness}, Total Visited: {total_visited}, Time: {clock.time()}")
    while clock < max_time:
        station = new_station
        num_plats = station.num_platforms
        previous_stations.append(station)
        waiting_times = time_to_next_train(station, clock, current_direction, current_line)
        if waiting_times == [10000] * 6:
            break
        need_to_visit = unvisited_stations(station, station_objs)
        going_back = going_back_on_yourself(station, previous_stations)
        current_direction_binary = 1 if current_direction == "up" else 0
        non_tube_options = num_additional_connections(station)
        inputs = need_to_visit + going_back + [total_visited] + [current_direction_binary] + [non_tube_options] + [num_plats]
        # get output from net
        output = np.argmax(net.activate(inputs)) % num_plats
        while (next_station_name := station.platforms[output].next_stop) == "End":
            # the agent cannot continue at the end of the line
            output += 1
            output %= num_plats
        # update time
        jump1 = train_waiting_time(waiting_times, output)
        if jump1 > dt.timedelta(minutes=35):
            while jump1 > dt.timedelta(minutes=35):
                # don't let the agent wait for more than 35 minutes
                output += 1
                output %= num_plats
                jump1 = train_waiting_time(waiting_times, output)
                next_station_name = station.platforms[output].next_stop
        jump2 = time_to_next_station(station, output)
        # update time
        clock += jump1 + jump2
        # make movement
        new_station = station_objs[next_station_name]
        current_direction = station.platforms[output].direction
        current_line = station.platforms[output].line
        # call visit
        if not station.visited:
            total_visited += station.visit(genome, current_line)
        total_visited += new_station.visit(genome, current_line)
        if winner:
            # pass
            print(f"Station: {new_station}, Fitness: {genome.fitness}, Total Visited: {total_visited}, Time: {clock.time()}")
        # if done
        if total_visited == 64:
            break
    time_taken = (clock - dt.datetime.combine(dt.date.min, start_time)) // dt.timedelta(minutes=1)
    genome.fitness -= time_taken * 5e0
    if winner:
        print("Final fitness: ", genome.fitness)
        print("Time taken: ", time_taken)
        print("Not visited:")
        for station in station_objs.values():
            if not station.visited:
                print(station)
    return genome.fitness

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    load = 0
    if load:
        p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-200")
    else:
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    profile = 0
    pr=None

    free_threads = 4
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count()-free_threads, eval_genomes_threaded)

    winner = p.run(pe.evaluate, 101)
    # winner = p.run(pe.evaluate, 1)

    # if profile:
    #     with cProfile.Profile() as pr:
    #         winner = p.run(eval_genomes, 10)
    # else:
    #     winner = p.run(eval_genomes, 1000)

    # if profile:
    #     results = pstats.Stats(pr)
    #     results.dump_stats("results.prof")

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    node_names = {}
    visualise.draw_net(config, winner, True, node_names=node_names, show_disabled=False, fmt="png")
    visualise.plot_stats(stats, ylog=True, view=True)
    
    eval_genomes([(1, winner)], config, winner=1)
 
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    train = 1
    if train:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-whole-tc')
        t1 = perf_counter()
        run(config_path)
        t2 = perf_counter()
        print(f"Training time: {t2-t1} seconds")
    else:
        local_dir = os.path.dirname(__file__)
        path = os.path.join(local_dir, "checkpoints\\neat-checkpoint-53")
        p = neat.Checkpointer.restore_checkpoint(path)
        winner = p.run(eval_genomes, 1)
        winner_net = neat.nn.FeedForwardNetwork.create(winner, p.config)
        
        eval_genomes([(1, winner)], p.config, winner=1)
