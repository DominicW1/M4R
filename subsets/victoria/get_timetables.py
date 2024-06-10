import reqs as reqs
from tube_network import Station, Platform
import json
import datetime as dt
from stations import station_dict, nr_station_dict, lines
from next_stations import next_stops
from time import perf_counter
import sys
import pickle
import os
from tqdm import tqdm

def get_timetable(line, station_id, next_stop_id, intervalIds = None, route_number=0):
    url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
    response = reqs.make_request(url)
    json_data = json.loads(response.read())
    #region debug
    # start_id = station_dict["Rickmansworth"]
    # end_id = station_dict["Moor Park"]
    # if station_id == start_id and next_stop_id == end_id and line == "metropolitan" and intervalIds == [3]:
    #     print(url)
    #     # dump json
    #     print(station_id, next_stop_id)
    #     with open("green3.json", "w") as f:
    #         json.dump(json_data, f, indent=4)
        # sys.exit(0)
    #endregion

    if intervalIds is not None:
        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][route_number]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds]
    else:
        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][route_number]["schedules"][0]["knownJourneys"]]

    # turn the times into datetime objects, addings days if necessary
    date_to_datetime(timetable)
    return timetable

def get_day_timetable(crs_code, month, day, destinations, tocCodes, first=1):
    url = f"https://api.rtt.io/api/v1/json/search/{crs_code}/2024/{month}/{day}"
    response = reqs.make_rtt_request(url)
    data = json.loads(response.read())
    #region debug
    # if crs_code == "UPM":
    #     # dump json
    #     with open("green4.json", "w") as f:
    #         json.dump(data, f, indent=4)
    #     sys.exit(0)
    #endregion
    timetable = []
    for service in data["services"]:
        service_loc = service["locationDetail"]
        destination = service_loc["destination"][0]["description"]
        checks = [service["isPassenger"], service_loc["isPublicCall"], service["serviceType"] == "train", service["atocCode"] in tocCodes, destination in destinations]
        if all(checks):
            hhmm_time = service_loc["gbttBookedDeparture"]
            time = dt.datetime.strptime(hhmm_time, "%H%M").time()
            if time < dt.time(4, 0):
                if first:
                    pass
                else:
                    timetable.append(time)
            else:
                if first:
                    timetable.append(time)
                else:
                    pass
    return timetable

def get_overground_timetable(station, direction):
    crs_code = nr_station_dict[station]
    lioness_line = ["Harrow & Wealdstone", "Kenton", "South Kenton", "North Wembley", "Wembley Central", "Stonebridge Park", "Harlesden", "Willesden Junction", "Kensal Green", "Queen's Park"]
    suffragette_line = ["Walthamstow Queens Road", "Leytonstone High Road", "Barking"]
    mildmay1 = ["Richmond", "Kew Gardens", "Gunnersbury"]
    mildmay2 = ["Shepherd's Bush (Central)", "Kensington (Olympia)", "West Brompton"]
    c2c = ["West Ham", "Barking", "Upminster"]
    great_northern = ["Old Street", "Highbury & Islington"]
    chiltern = ["Amersham", "Chalfont & Latimer", "Chorleywood", "Rickmansworth"]
    match station:
        case station if station in lioness_line:
            destinations = ["Watford Junction"] if direction == "up" else ["London Euston"]
            tocCodes = ["LO"]
        case station if station in suffragette_line:
            destinations = ["Barking Riverside"] if direction == "up" else ["Gospel Oak"]
            tocCodes = ["LO"]
        case station if station in mildmay1:
            destinations = ["Richmond"] if direction == "up" else ["Stratford (London)"]
            tocCodes = ["LO"]
        case station if station in mildmay2:
            destinations = ["Stratford (London)", "Watford Junction"] if direction == "up" else ["Clapham Junction", "Selhurst", "East Croydon"]
            tocCodes = ["LO", "SN"]
        case station if station in c2c:
            destinations = ["London Fenchurch Street", "London Liverpool Street"] if direction == "down" else ["Shoeburyness", "Southend Central"]
            tocCodes = ["CC"]
        case station if station in great_northern:
            destinations = ["Moorgate"] if direction == "down" else ["Welwyn Garden City", "Hertford North", "Stevenage"]
            tocCodes = ["GN"]
        case station if station in chiltern:
            destinations = ["Aylesbury", "Aylesbury Vale Parkway"] if direction == "up" else ["London Marylebone"]
            tocCodes = ["CH"]
        case _:
            print(station, "???")
            sys.exit(0)

    day1_timetable = get_day_timetable(crs_code, "06", "10", destinations, tocCodes)
    day2_timetable = get_day_timetable(crs_code, "06", "11", destinations, tocCodes, first=0)
    # attach dates
    day1_timetable = [dt.datetime.combine(dt.date.min, time) for time in day1_timetable]
    day2_timetable = [dt.datetime.combine(dt.date.min + dt.timedelta(days=1), time) for time in day2_timetable]
    timetable = day1_timetable + day2_timetable
    return timetable

def make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds = None, route_number=0):
    try:
        next_stop_id = station_dict[next_stop]
        timetable = get_timetable(line, station_id, next_stop_id, intervalIds, route_number)
        next_stop = next_stop if next_stop != "Morden_tram" else "Morden"
        next_stop = next_stop if next_stop != "Wimbledon_tram" else "Wimbledon"
        platform = Platform(station_objs[station], next_stop, line)
        platform.time_to_next_stop = time_to_next
        platform.departure_times = timetable
        platform.direction = direction
    except KeyError:
        platform = Platform(station_objs[station], next_stop, line, end=True, direction=direction)

def make_overground_platform(station, next_stop, time_to_next, direction, line):
        match station:
            case "Walthamstow Central":
                timetable = get_overground_timetable("Walthamstow Queens Road", direction)
            case "Leytonstone":
                timetable = get_overground_timetable("Leytonstone High Road", direction)
            case "Shepherds Bush (Central)":
                timetable = get_overground_timetable("Shepherds Bush", direction)
            case _:
                timetable = get_overground_timetable(station, direction)
        # create platform object
        platform = Platform(station_objs[station], next_stop, line)
        platform.time_to_next_stop = time_to_next
        platform.departure_times = timetable
        platform.direction = direction

def date_to_datetime(timetable):
    for i, time in enumerate(timetable):
        if time < dt.time(4, 0):
            timetable[i] = dt.datetime.combine(dt.date.min + dt.timedelta(days=1), time)
        else:
            timetable[i] = dt.datetime.combine(dt.date.min, time)
    return timetable

def combine_platforms(station, *args, num=2, up=1, down=1):
    plat_list = station_objs[station].platforms
    if num == 2:
        line1, line2 = args
        ups = [plat for plat in plat_list if (plat.direction == "up" and (plat.line == line1 or plat.line == line2))] if up else []
        downs = [plat for plat in plat_list if (plat.direction == "down" and (plat.line == line1 or plat.line == line2))] if down else []
        if up:
            up_timetable1 = ups[0].departure_times
            up_timetable2 = ups[1].departure_times
            up_timetable = up_timetable1 + up_timetable2
            up_timetable.sort()
            late_times = []
            for time in up_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            up_timetable += late_times
            up_timetable = up_timetable[len(late_times):]
            up_time_to_next = ups[0].time_to_next_stop
            up_next_stop = ups[0].next_stop
            up_direction = ups[0].direction
        if down:
            down_timetable1 = downs[0].departure_times
            down_timetable2 = downs[1].departure_times
            down_timetable = down_timetable1 + down_timetable2
            down_timetable.sort()
            late_times = []
            for time in down_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            down_timetable += late_times
            down_timetable = down_timetable[len(late_times):]
            down_time_to_next = downs[0].time_to_next_stop
            down_next_stop = downs[0].next_stop
            down_direction = downs[0].direction

        big_platforms = station_objs[station].platforms
        station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups and platform not in downs]
        new_name = ""
        if up:
            for plat in ups:
                if plat.line in lines:
                    new_name += plat.line + "_"
            new_name = new_name[:-1]
        else:
            for plat in downs:
                if plat.line in lines:
                    new_name += plat.line + "_"
            new_name = new_name[:-1]
        if up:
            platform = Platform(station_objs[station], up_next_stop, new_name)
            platform.time_to_next_stop = up_time_to_next
            platform.departure_times = up_timetable
            platform.direction = up_direction
        if down:
            platform = Platform(station_objs[station], down_next_stop, new_name)
            platform.time_to_next_stop = down_time_to_next
            platform.departure_times = down_timetable
            platform.direction = down_direction

    else:
        line1, line2, line3 = args
        ups = [plat for plat in plat_list if (plat.direction == "up" and (plat.line == line1 or plat.line == line2 or plat.line == line3))] if up else []
        downs = [plat for plat in plat_list if (plat.direction == "down" and (plat.line == line1 or plat.line == line2 or plat.line == line3))] if down else []
        if up:
            up_timetable1 = ups[0].departure_times
            up_timetable2 = ups[1].departure_times
            up_timetable3 = ups[2].departure_times
            up_timetable = up_timetable1 + up_timetable2 + up_timetable3
            up_timetable.sort()
            late_times = []
            for time in up_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            up_timetable += late_times
            up_timetable = up_timetable[len(late_times):]
            up_time_to_next = ups[0].time_to_next_stop
            up_next_stop = ups[0].next_stop
            up_direction = ups[0].direction
        if down:
            down_timetable1 = downs[0].departure_times
            down_timetable2 = downs[1].departure_times
            down_timetable3 = downs[2].departure_times
            down_timetable = down_timetable1 + down_timetable2 + down_timetable3
            down_timetable.sort()
            late_times = []
            for time in down_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            down_timetable += late_times
            down_timetable = down_timetable[len(late_times):]
            down_time_to_next = downs[0].time_to_next_stop
            down_next_stop = downs[0].next_stop
            down_direction = downs[0].direction

        big_platforms = station_objs[station].platforms
        station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups and platform not in downs]
        new_name = ""
        if up:
            for plat in ups:
                if plat.line in lines:
                    new_name += plat.line + "_"
            new_name = new_name[:-1]
        else:
            for plat in downs:
                if plat.line in lines:
                    new_name += plat.line + "_"
            new_name = new_name[:-1]
        if up:
            platform = Platform(station_objs[station], up_next_stop, new_name)
            platform.time_to_next_stop = up_time_to_next
            platform.departure_times = up_timetable
            platform.direction = up_direction
        if down:
            platform = Platform(station_objs[station], down_next_stop, new_name)
            platform.time_to_next_stop = down_time_to_next
            platform.departure_times = down_timetable
            platform.direction = down_direction

def get_timetables():
    for station in tqdm(list(station_dict.keys())): # progress bar
    # for station in station_dict.keys():
        # create station object
        station_objs[station] = Station(station)
        station_id = station_dict[station]
        station_lines = next_stops[station].keys()
        for line in station_lines:
            match line:
                case "metropolitan":
                    # dir_list = ["up", "down", "up", "up", "down"]
                    dir_list = ["up", "down", "up", "down"]
                    for i, temp in enumerate(next_stops[station][line]):
                        next_stop, time_to_next = temp
                        if next_stop == "fill":
                            continue
                        direction = dir_list[i]
                        match station:
                            case "Wembley Park":
                                if next_stop == "Finchley Road":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                elif next_stop == "Harrow-on-the-Hill":
                                    intervalIds = [2, 3, 5, 7, 8, 9, 12]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                else:
                                    intervalIds = [0, 1, 4, 6, 10, 11]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                            case "Rickmansworth":
                                if next_stop == "Croxley":
                                    intervalIds = [3]
                                    next_stop_id = station_dict["Moor Park"]
                                    timetable = get_timetable(line, station_id, next_stop_id, intervalIds)
                                    platform = Platform(station_objs[station], next_stop, line)
                                    platform.time_to_next_stop = time_to_next
                                    platform.departure_times = timetable
                                    platform.direction = direction
                                elif next_stop == "Moor Park":
                                    intervalIds = [0, 1, 2, 4, 5, 6, 7, 8]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                else:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                            case "Chalfont & Latimer":
                                if next_stop == "Chesham":
                                    intervalIds = [1]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                elif next_stop == "Amersham":
                                    intervalIds = [0]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                else:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                            case "Harrow-on-the-Hill":
                                if next_stop == "Wembley Park":
                                    intervalIds = [1, 4]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                elif next_stop == "Northwick Park":
                                    intervalIds = [0, 2, 3]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                elif next_stop == "Moor Park":
                                    intervalIds = [4, 5, 7]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                elif next_stop == "West Harrow":
                                    intervalIds = [0]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                else:
                                    intervalIds = [1, 2, 3]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                            case "Moor Park":
                                if next_stop == "Rickmansworth":
                                    next_stop_id = station_dict[next_stop]
                                    url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                    response = reqs.make_request(url)
                                    json_data = json.loads(response.read())
                                    timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"]] # routes[1] instead of 0
                                    timetable = date_to_datetime(timetable)
                                    platform = Platform(station_objs[station], next_stop, line)
                                    platform.time_to_next_stop = time_to_next
                                    platform.departure_times = timetable
                                    platform.direction = direction
                                elif next_stop == "Croxley":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                elif next_stop == "Harrow-on-the-Hill":
                                    intervalIds = [1, 6]
                                    next_stop_id = station_dict[next_stop]
                                    url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                    response = reqs.make_request(url)
                                    json_data = json.loads(response.read())
                                    timetable1 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds] # routes[0]
                                    timetable2 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds] # routes[1]
                                    timetable = timetable1 + timetable2
                                    timetable.sort()
                                    # move all of the times before 5:00 to the end as they're the next day
                                    late_times = []
                                    for time in timetable:
                                        if time < dt.time(5, 0):
                                            late_times.append(time)
                                    timetable += late_times
                                    timetable = timetable[len(late_times):]
                                    timetable = date_to_datetime(timetable)
                                    platform = Platform(station_objs[station], next_stop, line)
                                    platform.time_to_next_stop = time_to_next
                                    platform.departure_times = timetable
                                    platform.direction = direction
                                else:
                                    intervalIds = [0, 2, 3, 4, 5, 7]
                                    next_stop_id = station_dict[next_stop]
                                    url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                    response = reqs.make_request(url)
                                    json_data = json.loads(response.read())
                                    timetable1 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds] # routes[0]
                                    timetable2 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds] # routes[1]
                                    timetable = timetable1 + timetable2
                                    timetable.sort()
                                    # move all of the times before 5:00 to the end as they're the next day
                                    late_times = []
                                    for time in timetable:
                                        if time < dt.time(5, 0):
                                            late_times.append(time)
                                    timetable += late_times
                                    timetable = timetable[len(late_times):]
                                    timetable = date_to_datetime(timetable)
                                    platform = Platform(station_objs[station], next_stop, line)
                                    platform.time_to_next_stop = time_to_next
                                    platform.departure_times = timetable
                                    platform.direction = direction
                            case "Croxley":
                                if next_stop == "Moor Park":
                                    next_stop_id = station_dict[next_stop]
                                    url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                    response = reqs.make_request(url)
                                    json_data = json.loads(response.read())
                                    timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"]]
                                    timetable = date_to_datetime(timetable)
                                    platform = Platform(station_objs[station], next_stop, line)
                                    platform.time_to_next_stop = time_to_next
                                    platform.departure_times = timetable
                                    platform.direction = direction
                                else:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                            case _:
                                make_platform(station, line, station_id, next_stop, time_to_next, direction)

                case "northern":
                    dir_list = ["up", "down", "up", "down"]
                    for i, temp in enumerate(next_stops[station][line]):
                        try:
                            next_stop, time_to_next = temp
                            direction = dir_list[i]
                            match station:
                                case "Finchley Central":
                                    if next_stop == "West Finchley":
                                        intervalIds = [0]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Mill Hill East":
                                        intervalIds = [1]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case "Camden Town":
                                    if next_stop == "Kentish Town":
                                        # get timetable for Tufnell Park to Archway
                                        tufnell_park_id = station_dict["Tufnell Park"]
                                        archway_id = station_dict["Archway"]
                                        timetable = get_timetable(line, tufnell_park_id, archway_id)
                                        # shift all times back by 3 minutes
                                        for i, time in enumerate(timetable):
                                            timetable[i] = time - dt.timedelta(minutes=3)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    elif next_stop == "Mornington Crescent":
                                        intervalIds = [1, 2, 3]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Euston":
                                        intervalIds = [0]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case "Euston":
                                    if next_stop == "Mornington Crescent":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"]]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    elif next_stop == "King's Cross St. Pancras":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"]]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case "Kennington":
                                    if next_stop == "Oval":
                                        intervalIds = [0]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Nine Elms":
                                        intervalIds = [1]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Elephant & Castle":
                                        intervalIds = [0, 3, 5, 6, 9]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    else:
                                        intervalIds = [1, 2, 4, 7, 8]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                case _:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                        except Exception as e:
                            print(e)
                            print(station, temp)
                            sys.exit(0)

                case "circle":
                    dir_list = ["up", "down", "up"]
                    for i, temp in enumerate(next_stops[station][line]):
                        try:
                            next_stop, time_to_next = temp
                            direction = dir_list[i]
                            match station:
                                case "Edgware Road (Circle Line)":
                                    if next_stop == "Paddington":
                                        pad_hc_id = station_dict["Paddington (H&C Line)"]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{pad_hc_id}"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable1 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"]]
                                        intervalIds = [0, 4]
                                        timetable2 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds]
                                        timetable = timetable1 + timetable2
                                        timetable.sort()
                                        # move all of the times before 5:00 to the end as they're the next day
                                        late_times = []
                                        for time in timetable:
                                            if time < dt.time(5, 0):
                                                late_times.append(time)
                                        timetable += late_times
                                        timetable = timetable[len(late_times):]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    elif next_stop == "Paddington (H&C Line)":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        intervalIds = [1]
                                        timetable1 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"] if train["intervalId"] in intervalIds]
                                        timetable2 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][2]["schedules"][0]["knownJourneys"]]
                                        timetable = timetable1 + timetable2
                                        timetable.sort()
                                        # move all of the times before 5:00 to the end as they're the next day
                                        late_times = []
                                        for time in timetable:
                                            if time < dt.time(5, 0):
                                                late_times.append(time)
                                        timetable += late_times
                                        timetable = timetable[len(late_times):]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    elif next_stop == "Baker Street":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}?direction=inbound"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"]]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                case "Paddington":
                                    if next_stop == "Edgware Road (Circle Line)":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}?direction=outbound"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"]]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case "Baker Street":
                                    if next_stop == "Edgware Road (Circle Line)":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}?direction=inbound"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"]]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case "Gloucester Road":
                                    if next_stop == "High Street Kensington":
                                        next_stop_id = station_dict[next_stop]
                                        url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{station_id}/to/{next_stop_id}"
                                        response = reqs.make_request(url)
                                        json_data = json.loads(response.read())
                                        timetable1 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][0]["schedules"][0]["knownJourneys"]]
                                        timetable2 = [dt.time((int(train["hour"]) % 24), int(train["minute"])) for train in json_data["timetable"]["routes"][1]["schedules"][0]["knownJourneys"]]
                                        timetable = timetable1 + timetable2
                                        timetable.sort()
                                        # move all of the times before 5:00 to the end as they're the next day
                                        late_times = []
                                        for time in timetable:
                                            if time < dt.time(5, 0):
                                                late_times.append(time)
                                        timetable += late_times
                                        timetable = timetable[len(late_times):]
                                        timetable = date_to_datetime(timetable)
                                        platform = Platform(station_objs[station], next_stop, line)
                                        platform.time_to_next_stop = time_to_next
                                        platform.departure_times = timetable
                                        platform.direction = direction
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case _:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                        except Exception as e:
                            print(e)
                            print(line)
                            print(station, next_stop)
                            print(station_dict[station], station_dict[next_stop])
                            sys.exit(0)

                case "district":
                    dir_list = ["up", "down", "up", "down", "up"]
                    for i, temp in enumerate(next_stops[station][line]):
                        try:
                            next_stop, time_to_next = temp
                            if next_stop == "fill":
                                continue
                            direction = dir_list[i]
                            match station:
                                case "Earl's Court":
                                    if next_stop == "Kensington (Olympia)":
                                        intervalIds = [3]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "West Kensington":
                                        intervalIds = [1, 2, 4]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "West Brompton":
                                        intervalIds = [0]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "High Street Kensington":
                                        intervalIds = [1, 5]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Gloucester Road":
                                        intervalIds = [0, 2, 3, 4]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                case "Turnham Green":
                                    if next_stop == "Chiswick Park":
                                        intervalIds = [0]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Gunnersbury":
                                        intervalIds = [1]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    else:
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                case _:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                        except Exception as e:
                            print(e)
                            print(line)
                            print(station, next_stop)
                            sys.exit(0)

                case "piccadilly":
                    try:
                        dir_list = ["up", "down", "up", "down"]
                        for i, temp in enumerate(next_stops[station][line]):
                            next_stop, time_to_next = temp
                            direction = dir_list[i]
                            match station:
                                case "Acton Town":
                                    if next_stop == "South Ealing":
                                        intervalIds = [0, 1, 3, 4]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Ealing Common":
                                        intervalIds = [2, 5]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Turnham Green":
                                        intervalIds = [1, 4, 5, 6, 8]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Hammersmith (Dist&Picc Line)":
                                        intervalIds = [0, 2, 3]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)

                                case "Hatton Cross":
                                    if next_stop == "Heathrow Terminal 4":
                                        intervalIds = [1]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Heathrow Terminals 2 & 3":
                                        intervalIds = [0, 2]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Hounslow West":
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)

                                case "Hammersmith (Dist&Picc Line)":
                                    if next_stop == "Acton Town":
                                        intervalIds = [0, 1, 2, 7, 8]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Turnham Green":
                                        intervalIds = [3, 4, 5, 6, 9, 10]
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                    elif next_stop == "Barons Court":
                                        make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                
                                case _:
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                    except Exception as e:
                        print(e)
                        print(station)
                        sys.exit(0)

                case "central":
                    dir_list = ["up", "down", "up", "down"]
                    for i, temp in enumerate(next_stops[station][line]):
                        next_stop, time_to_next = temp
                        if next_stop == "fill":
                            continue
                        direction = dir_list[i]
                        match station:
                            case "North Acton":
                                if next_stop == "East Acton":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                elif next_stop == "West Acton":
                                    intervalIds = [1]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                else:
                                    intervalIds = [0, 2, 3]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)

                            case "Hainault":
                                if next_stop == "Fairlop":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, route_number=1)
                                elif next_stop == "Grange Hill":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)

                            case "Leytonstone":
                                if next_stop == "Leyton":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                elif next_stop == "Snaresbrook":
                                    intervalIds = [1, 3]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                elif next_stop == "Wanstead":
                                    intervalIds = [0]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)

                            case "Woodford":
                                if next_stop == "South Woodford":
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction)
                                elif next_stop == "Buckhurst Hill":
                                    intervalIds = [0]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                                elif next_stop == "Roding Valley":
                                    intervalIds = [1]
                                    make_platform(station, line, station_id, next_stop, time_to_next, direction, intervalIds)
                            
                            case _:
                                make_platform(station, line, station_id, next_stop, time_to_next, direction)

                case line if line in ["foot", "bus"]:
                    dir_list = ["up", "up"]
                    for i, temp in enumerate(next_stops[station][line]):
                        next_stop, time_to_next = next_stops[station][line][0]
                        next_stop_id = station_dict[next_stop]
                        timetable = [dt.datetime.combine(dt.date.min, dt.time(4, 0)) + dt.timedelta(minutes=i) for i in range(60*21)]
                        platform = Platform(station_objs[station], next_stop, line)
                        platform.time_to_next_stop = time_to_next
                        platform.departure_times = timetable

                case line if line in ["lioness", "suffragette", "mildmay1", "mildmay2", "c2c", "great_northern", "chiltern"]:
                    dir_list = ["up", "down"]
                    for i, temp in enumerate(next_stops[station][line]):
                        next_stop, time_to_next = temp
                        if next_stop == "End":
                            continue
                        direction = dir_list[i]
                        make_overground_platform(station, next_stop, time_to_next, direction, line=line)

                case "tram":
                    dir_list = ["up"]
                    for i, temp in enumerate(next_stops[station][line]):
                        next_stop, time_to_next = temp
                        direction = dir_list[i]
                        match station:
                            case "Morden":
                                station_id = station_dict["Morden_tram"]
                                next_stop = "Wimbledon_tram"
                                make_platform(station, line, station_id, next_stop, time_to_next, direction)
                            case "Wimbledon":
                                station_id = station_dict["Wimbledon_tram"]
                                next_stop = "Morden_tram"
                                make_platform(station, line, station_id, next_stop, time_to_next, direction)

                case _:
                    dir_list = ["up", "down"]
                    for i, temp in enumerate(next_stops[station][line]):
                        try:
                            next_stop, time_to_next = temp
                            try:
                                direction = dir_list[i]
                            except IndexError:
                                print(station, line, next_stop, time_to_next)
                            make_platform(station, line, station_id, next_stop, time_to_next, direction)
                        except Exception as e:
                            print(e)
                            print(station, line)
                            sys.exit(0)

        if ("district" in station_lines) and ("hammersmith-city" in station_lines) and ("circle" in station_lines):
            # just edgware road (circle line)
            ups_to_pad_hc = [platform for platform in station_objs[station].platforms if platform.next_stop == "Paddington (H&C Line)"]
            ups_to_pad = [platform for platform in station_objs[station].platforms if platform.next_stop == "Paddington"]
            downs_to_baker = [platform for platform in station_objs[station].platforms if platform.next_stop == "Baker Street"]
            ups_to_pad_hc_timetable1 = ups_to_pad_hc[0].departure_times
            ups_to_pad_hc_timetable2 = ups_to_pad_hc[1].departure_times
            ups_to_pad_timetable1 = ups_to_pad[0].departure_times
            ups_to_pad_timetable2 = ups_to_pad[1].departure_times
            downs_to_baker_timetable1 = downs_to_baker[0].departure_times
            downs_to_baker_timetable2 = downs_to_baker[1].departure_times
            ups_to_pad_hc_timetable = ups_to_pad_hc_timetable1 + ups_to_pad_hc_timetable2
            ups_to_pad_timetable = ups_to_pad_timetable1 + ups_to_pad_timetable2
            downs_to_baker_timetable = downs_to_baker_timetable1 + downs_to_baker_timetable2
            ups_to_pad_hc_timetable.sort()
            ups_to_pad_timetable.sort()
            downs_to_baker_timetable.sort()
            late_times = []
            for time in ups_to_pad_hc_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            ups_to_pad_hc_timetable += late_times
            ups_to_pad_hc_timetable = ups_to_pad_hc_timetable[len(late_times):]
            for time in ups_to_pad_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            ups_to_pad_timetable += late_times
            ups_to_pad_timetable = ups_to_pad_timetable[len(late_times):]
            for time in downs_to_baker_timetable:
                if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                    late_times.append(time)
            downs_to_baker_timetable += late_times
            downs_to_baker_timetable = downs_to_baker_timetable[len(late_times):]
            ups_to_pad_hc_time_to_next = ups_to_pad_hc[0].time_to_next_stop
            ups_to_pad_time_to_next = ups_to_pad[0].time_to_next_stop
            downs_to_baker_time_to_next = downs_to_baker[0].time_to_next_stop
            ups_to_pad_hc_next_stop = ups_to_pad_hc[0].next_stop
            ups_to_pad_next_stop = ups_to_pad[0].next_stop
            downs_to_baker_next_stop = downs_to_baker[0].next_stop
            big_platforms = station_objs[station].platforms
            station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups_to_pad_hc and platform not in ups_to_pad and platform not in downs_to_baker]
            ups_to_pad_hc_platform = Platform(station_objs[station], ups_to_pad_hc_next_stop, "circle_hammersmith-city")
            ups_to_pad_hc_platform.time_to_next_stop = ups_to_pad_hc_time_to_next
            ups_to_pad_hc_platform.departure_times = ups_to_pad_hc_timetable
            ups_to_pad_hc_platform.direction = "up"
            ups_to_pad_platform = Platform(station_objs[station], ups_to_pad_next_stop, "circle_district")
            ups_to_pad_platform.time_to_next_stop = ups_to_pad_time_to_next
            ups_to_pad_platform.departure_times = ups_to_pad_timetable
            ups_to_pad_platform.direction = "up"
            downs_to_baker_platform = Platform(station_objs[station], downs_to_baker_next_stop, "circle_hammersmith-city")
            downs_to_baker_platform.time_to_next_stop = downs_to_baker_time_to_next
            downs_to_baker_platform.departure_times = downs_to_baker_timetable
            downs_to_baker_platform.direction = "down"
        elif ("circle" in station_lines) and ("hammersmith-city" in station_lines) and ("metropolitan" in station_lines):
            match station:
                case "Baker Street":
                    # down as normal, up only circle and hammersmith-city
                    ups = [platform for platform in station_objs[station].platforms if (platform.direction == "up" and (platform.line == "circle" or platform.line == "hammersmith-city"))]
                    downs = [platform for platform in station_objs[station].platforms if (platform.direction == "down" and (platform.line == "circle" or platform.line == "hammersmith-city" or platform.line == "metropolitan"))]
                    up_timetable1 = ups[0].departure_times
                    up_timetable2 = ups[1].departure_times
                    down_timetable1 = downs[0].departure_times
                    down_timetable2 = downs[1].departure_times
                    down_timetable3 = downs[2].departure_times
                    up_timetable = up_timetable1 + up_timetable2
                    down_timetable = down_timetable1 + down_timetable2 + down_timetable3
                    up_timetable.sort()
                    down_timetable.sort()
                    late_times = []
                    for time in up_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    up_timetable += late_times
                    up_timetable = up_timetable[len(late_times):]
                    for time in down_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    down_timetable += late_times
                    down_timetable = down_timetable[len(late_times):]
                    up_time_to_next = ups[0].time_to_next_stop
                    down_time_to_next = downs[0].time_to_next_stop
                    up_next_stop = ups[0].next_stop
                    down_next_stop = downs[0].next_stop
                    big_platforms = station_objs[station].platforms
                    station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups and platform not in downs]
                    up_platform = Platform(station_objs[station], up_next_stop, "circle_hammersmith-city")
                    up_platform.time_to_next_stop = up_time_to_next
                    up_platform.departure_times = up_timetable
                    up_platform.direction = "up"
                    down_platform = Platform(station_objs[station], down_next_stop, "circle_hammersmith-city_metropolitan")
                    down_platform.time_to_next_stop = down_time_to_next
                    down_platform.departure_times = down_timetable
                    down_platform.direction = "down"
                case "Liverpool Street":
                    # up as normal, down only circle and metropolitan
                    ups = [platform for platform in station_objs[station].platforms if (platform.direction == "up" and (platform.line == "circle" or platform.line == "hammersmith-city" or platform.line == "metropolitan"))]
                    downs = [platform for platform in station_objs[station].platforms if (platform.direction == "down" and (platform.line == "circle" or platform.line == "metropolitan"))]
                    up_timetable1 = ups[0].departure_times
                    up_timetable2 = ups[1].departure_times
                    up_timetable3 = ups[2].departure_times
                    down_timetable1 = downs[0].departure_times
                    down_timetable2 = downs[1].departure_times
                    up_timetable = up_timetable1 + up_timetable2 + up_timetable3
                    down_timetable = down_timetable1 + down_timetable2
                    up_timetable.sort()
                    down_timetable.sort()
                    late_times = []
                    for time in up_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    up_timetable += late_times
                    up_timetable = up_timetable[len(late_times):]
                    late_times = []
                    for time in down_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    down_timetable += late_times
                    down_timetable = down_timetable[len(late_times):]
                    up_time_to_next = ups[0].time_to_next_stop
                    down_time_to_next = downs[0].time_to_next_stop
                    up_next_stop = ups[0].next_stop
                    down_next_stop = downs[0].next_stop
                    big_platforms = station_objs[station].platforms
                    station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups and platform not in downs]
                    up_platform = Platform(station_objs[station], up_next_stop, "circle_hammersmith-city_metropolitan")
                    up_platform.time_to_next_stop = up_time_to_next
                    up_platform.departure_times = up_timetable
                    up_platform.direction = "up"
                    down_platform = Platform(station_objs[station], down_next_stop, "circle_metropolitan")
                    down_platform.time_to_next_stop = down_time_to_next
                    down_platform.departure_times = down_timetable
                    down_platform.direction = "down"
                case _:
                    combine_platforms(station, "circle", "hammersmith-city", "metropolitan", num=3)
        elif ("district" in station_lines) and ("hammersmith-city" in station_lines):
            match station:
                case "Aldgate East":
                    combine_platforms(station, "district", "hammersmith-city", up=0)
                case "Barking":
                    combine_platforms(station, "district", "hammersmith-city", down=0)
                case _:
                    combine_platforms(station, "district", "hammersmith-city")
        elif ("circle" in station_lines) and ("hammersmith-city" in station_lines):
            match station:
                case "Hammersmith (H&C Line)":
                    ups = [platform for platform in station_objs[station].platforms if (platform.direction == "up" and (platform.line == "circle" or platform.line == "hammersmith-city"))]
                    downs = [platform for platform in station_objs[station].platforms if (platform.direction == "down" and (platform.line == "circle" or platform.line == "hammersmith-city"))]
                    up_timetable1 = ups[0].departure_times
                    up_timetable2 = ups[1].departure_times
                    down_timetable1 = downs[0].departure_times
                    down_timetable2 = downs[1].departure_times
                    up_timetable = up_timetable1 + up_timetable2
                    down_timetable = down_timetable1 + down_timetable2
                    up_timetable.sort()
                    down_timetable.sort()
                    late_times = []
                    for time in up_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    up_timetable += late_times
                    up_timetable = up_timetable[len(late_times):]
                    for time in down_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    down_timetable += late_times
                    down_timetable = down_timetable[len(late_times):]
                    up_time_to_next = ups[0].time_to_next_stop
                    down_time_to_next = downs[0].time_to_next_stop
                    up_next_stop = ups[0].next_stop
                    down_next_stop = downs[0].next_stop
                    big_platforms = station_objs[station].platforms
                    station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups and platform not in downs]
                    up_platform = Platform(station_objs[station], up_next_stop, "circle_hammersmith-city", end=True)
                    up_platform.time_to_next_stop = up_time_to_next
                    up_platform.departure_times = up_timetable
                    up_platform.direction = "up"
                    down_platform = Platform(station_objs[station], down_next_stop, "circle_hammersmith-city")
                    down_platform.time_to_next_stop = down_time_to_next
                    down_platform.departure_times = down_timetable
                    down_platform.direction = "down"
                case _:
                    combine_platforms(station, "circle", "hammersmith-city")
        elif ("district" in station_lines) and ("circle" in station_lines):
            match station:
                case "Tower Hill":
                    # only change the up platform
                    combine_platforms(station, "district", "circle", down=0)
                case "Gloucester Road":
                    # only change the down platform
                    combine_platforms(station, "district", "circle", up=0)
                case "High Street Kensington":
                    # only change the down platform
                    combine_platforms(station, "district", "circle", up=0)
                case _:
                    combine_platforms(station, "district", "circle")
        elif ("bakerloo" in station_lines) and ("lioness" in station_lines):
            match station:
                case "Harrow & Wealdstone":
                    # only change the down platform
                    combine_platforms(station, "bakerloo", "lioness", up=0)
                case "Queen's Park":
                    # only change the up platform
                    combine_platforms(station, "bakerloo", "lioness", down=0)
                case _:
                    combine_platforms(station, "bakerloo", "lioness")
        elif ("piccadilly" in station_lines) and ("metropolitan" in station_lines):
            match station:
                case "Rayners Lane":
                    combine_platforms(station, "piccadilly", "metropolitan", down=0)
                case "Uxbridge":
                    combine_platforms(station, "piccadilly", "metropolitan", up=0)
                case _:
                    combine_platforms(station, "piccadilly", "metropolitan")
        elif ("circle" in station_lines) and ("metropolitan" in station_lines):
            combine_platforms(station, "circle", "metropolitan", down=0)
        elif ("chiltern" in station_lines) and ("metropolitan" in station_lines):
            match station:
                case "Amersham":
                    combine_platforms(station, "chiltern", "metropolitan", up=0)
                case "Rickmansworth":
                    combine_platforms(station, "chiltern", "metropolitan", down=0)
                case "Chalfont & Latimer":
                    # asset up platform next stop is Amersham
                    ups = [platform for platform in station_objs[station].platforms if (platform.direction == "up" and (platform.line == "chiltern" or platform.line == "metropolitan") and platform.next_stop == "Amersham")]
                    downs = [platform for platform in station_objs[station].platforms if (platform.direction == "down" and (platform.line == "chiltern" or platform.line == "metropolitan"))]
                    up_timetable1 = ups[0].departure_times
                    up_timetable2 = ups[1].departure_times
                    down_timetable1 = downs[0].departure_times
                    down_timetable2 = downs[1].departure_times
                    up_timetable = up_timetable1 + up_timetable2
                    down_timetable = down_timetable1 + down_timetable2
                    up_timetable.sort()
                    down_timetable.sort()
                    late_times = []
                    for time in up_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    up_timetable += late_times
                    up_timetable = up_timetable[len(late_times):]
                    for time in down_timetable:
                        if time < dt.datetime.combine(dt.date.min, dt.time(5, 0)):
                            late_times.append(time)
                    down_timetable += late_times
                    down_timetable = down_timetable[len(late_times):]
                    up_time_to_next = ups[0].time_to_next_stop
                    down_time_to_next = downs[0].time_to_next_stop
                    up_next_stop = ups[0].next_stop
                    down_next_stop = downs[0].next_stop
                    big_platforms = station_objs[station].platforms
                    station_objs[station].platforms = [platform for platform in big_platforms if platform not in ups and platform not in downs]
                    up_platform = Platform(station_objs[station], up_next_stop, "metropolitan")
                    up_platform.time_to_next_stop = up_time_to_next
                    up_platform.departure_times = up_timetable
                    up_platform.direction = "up"
                    down_platform = Platform(station_objs[station], down_next_stop, "metropolitan")
                    down_platform.time_to_next_stop = down_time_to_next
                    down_platform.departure_times = down_timetable
                    down_platform.direction = "down"
                case _:
                    combine_platforms(station, "chiltern", "metropolitan")
        elif ("district" in station_lines) and ("mildmay1" in station_lines):
            match station:
                case "Gunnersbury":
                    combine_platforms(station, "district", "mildmay1", down=0)
                case "Richmond":
                    combine_platforms(station, "district", "mildmay1", up=0)
                case _:
                    combine_platforms(station, "district", "mildmay1")

        #region sort
        # move foot lines to end of list
        non_tube_lines = ["c2c", "chiltern", "great_northern", "lioness", "mildmay1", "mildmay2", "suffragette", "tram", "bus", "foot"]
        station_objs[station].platforms.sort(key=lambda x: non_tube_lines.index(x.line) if x.line in non_tube_lines else -1)
        #endregion


save = 0
load = 1

local_dir = os.path.dirname(__file__)

if save and load:
    print("no")
    sys.exit(0)
elif save:
    station_objs = {}
    get_timetables()
    path = os.path.join(local_dir, "pickles/station_objs.pkl")
    with open(path, "wb") as f:
        pickle.dump(station_objs, f)
elif load:
    path = os.path.join(local_dir, "pickles/station_objs.pkl")
    with open(path, "rb") as f:
        station_objs = pickle.load(f)
else:
    station_objs = {}
    get_timetables()

#region testing1
# line = "piccadilly"
# station_id = station_dict["Arnos Grove"]
# next_stop_id = station_dict["Southgate"]
# timetable = get_timetable(line, station_id, next_stop_id)
# print(timetable)
#endregion

#region testing2
# print timetable for a station
# station = "Euston"
# station_obj = station_objs[station]
# for platform in station_obj.platforms:
#     print(platform)
#     print(platform.direction)
#     print(platform.departure_times)
#     print()
#endregion
