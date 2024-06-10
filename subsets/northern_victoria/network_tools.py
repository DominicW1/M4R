import datetime as dt
import bisect as bs

def time_to_next_train(station, time, current_direction, current_line):
    waits = []
    original_time = time
    for platform in station.platforms:
        if platform.departure_times == []:
            waits.append(10000)
            continue
        jump = change_line_or_direction_penalty(current_direction, current_line, platform)
        time = original_time + jump
        if platform.line == "tram":
            match station:
                case "Morden":
                    time += dt.timedelta(minutes=4)
                case _:
                    pass
        elif platform.line == "mildmay2":
            match station:
                case "Shepherd's Bush (Central)":
                    time += dt.timedelta(minutes=1)
                case _:
                    pass
        elif platform.line == "suffragette":
            match station:
                case "Walthamstow Central":
                    time += dt.timedelta(minutes=1)
                case "Leytonstone":
                    time += dt.timedelta(minutes=4)
                case _:
                    pass
        index = bs.bisect_left(platform.departure_times, time)
        if index == len(platform.departure_times):
            waits.append(10000)
        else:
            waits.append((platform.departure_times[index] - original_time) // dt.timedelta(minutes=1))
    waits = (waits + 6*[10000])[:6]
    return waits

def reset_stations(station_objs):
    for station in station_objs.values():
        station.visited = False
        for platform in station.platforms:
            platform.visited = False

def unvisited_stations(station, station_objs):
    points = [-1]*6
    for i in range(station.num_platforms):
        try:
            if (not station_objs[station.platforms[i].next_stop].visited):
                if station.platforms[i].line in ["foot", "tram", "bus", "great_northern", "c2c", "suffragette", "mildmay2"]:
                    points[i] = 1
                else:
                    points[i] = 2
            else:
                points[i] = 0
        except KeyError:
            pass
    return points

def going_back_on_yourself(station, previous_stations):
    points = [0]*6
    terminus = False
    for plat in station.platforms:
        if plat.next_stop == "End":
            terminus = True
            break
    for i, plat in enumerate(station.platforms):
        try:
            if (plat.next_stop == previous_stations[-2].name):
                if not terminus:
                    points[i] = -1
                else:
                    points[i] = 1
            else:
                points[i] = 1
        except KeyError:
            pass
        except IndexError:
            pass
    return points

def train_waiting_time(waiting_times, output):
    return dt.timedelta(days=0, minutes=waiting_times[output])

def time_to_next_station(station, output):
    return dt.timedelta(minutes=station.platforms[output].time_to_next_stop)

def change_line_or_direction_penalty(current_direction, current_line, platform):
    if current_line in ["foot", "bus", "tram"] or platform.line in ["foot", "bus", "tram"]:
        return dt.timedelta(minutes=0)

    different_line = current_line != platform.line
    if different_line:
        current_line_list = current_line.split("_")
        platform_line_list = platform.line.split("_")
        for line in current_line_list:
            if line in platform_line_list:
                different_line = False
                break
        if different_line:
            for line in platform_line_list:
                if line in current_line_list:
                    different_line = False
                    break

    if different_line:
        jump = dt.timedelta(minutes=2)
    elif current_direction != platform.direction:
        jump = dt.timedelta(minutes=1)
    else:
        jump = dt.timedelta(minutes=0)
    return jump

def num_trains_left(station, time):
    """
    Returns list of number of trains after the current time
    for each platform at the station.
    """
    trains = []
    for platform in station.platforms:
        if platform.departure_times == []:
            trains.append(0)
            continue
        index = bs.bisect_left(platform.departure_times, time)
        if index == len(platform.departure_times):
            trains.append(0)
        else:
            trains.append(len(platform.departure_times) - index)
    trains = (trains + 6*[0])[:6]
    return trains

def num_additional_connections(station):
    num=0
    for plat in station.platforms:
        match plat.line:
            case line if line in ["foot", "tram", "mildmay2", "suffragette", "c2c", "great_northern", "bus"]:
                num += 1
            case _:
                pass
    return num
