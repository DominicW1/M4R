from stations import all_stations, lines
import sys
import pickle
import os
from icecream import ic

def make_next_stops():
    station_list = all_stations[:,0]
    station_list.sort()

    next_stops = {key: [] for key in station_list}

    try:
        next_stops["Acton Town"] = {"district": [("Ealing Common", 2), ("Chiswick Park", 2)], "piccadilly": [("South Ealing", 3), ("Turnham Green", 3), ("Ealing Common", 2), ("Hammersmith (Dist&Picc Line)", 6)]} # could try swap hammersmith and turnham green
        next_stops["Aldgate"] = {"circle": [("Liverpool Street", 2), ("Tower Hill", 2)], "metropolitan": [("Liverpool Street", 2), ("End", 0)], "foot": [("Aldgate East", 2)]}
        next_stops["Aldgate East"] = {"district": [("Tower Hill", 2), ("Whitechapel", 2)], "hammersmith-city": [("Liverpool Street", 2), ("Whitechapel", 2)], "foot": [("Aldgate", 2)]}
        next_stops["Baker Street"] = {"bakerloo": [("Marylebone", 1), ("Regent's Park", 1)], "circle": [("Edgware Road (Circle Line)", 2), ("Great Portland Street", 1)], "hammersmith-city": [("Edgware Road (Circle Line)", 2), ("Great Portland Street", 1)], "jubilee": [("St. John's Wood", 2), ("Bond Street", 2)], "metropolitan": [("Finchley Road", 5), ("Great Portland Street", 2)]}
        next_stops["Barbican"] = {"circle": [("Farringdon", 1), ("Moorgate", 1)], "metropolitan": [("Farringdon", 1), ("Moorgate", 1)], "hammersmith-city": [("Farringdon", 1), ("Moorgate", 1)]}
        next_stops["Barking"] = {"district": [("East Ham", 3), ("Upney", 2)], "hammersmith-city": [("East Ham", 3), ("End", 0)], "suffragette": [("End", 0), ("Walthamstow Central", 15)], "c2c": [("Upminster", 8), ("West Ham", 5)]}
        next_stops["Barons Court"] = {"district": [("Hammersmith (Dist&Picc Line)", 1), ("West Kensington", 1)], "piccadilly": [("Hammersmith (Dist&Picc Line)", 2), ("Earl's Court", 3)]}
        next_stops["Bayswater"] = {"district": [("Notting Hill Gate", 1), ("Paddington", 2)], "circle": [("Notting Hill Gate", 1), ("Paddington", 2)]}
        next_stops["Becontree"] = {"district": [("Upney", 2), ("Dagenham Heathway", 2)]}
        next_stops["Blackfriars"] = {"circle": [("Temple", 1), ("Mansion House", 2)], "district": [("Temple", 1), ("Mansion House", 2)]}
        next_stops["Bow Road"] = {"district": [("Mile End", 1), ("Bromley-by-Bow", 2)], "hammersmith-city": [("Mile End", 1), ("Bromley-by-Bow", 2)]}
        next_stops["Bromley-by-Bow"] = {"district": [("Bow Road", 2), ("West Ham", 2)], "hammersmith-city": [("Bow Road", 2), ("West Ham", 2)]}
        next_stops["Cannon Street"] = {"circle": [("Mansion House", 1), ("Monument", 1)], "district": [("Mansion House", 1), ("Monument", 1)]}
        next_stops["Chiswick Park"] = {"district": [("Acton Town", 2), ("Turnham Green", 2)], "foot": [("Gunnersbury", 4)]}
        next_stops["Dagenham East"] = {"district": [("Dagenham Heathway", 2), ("Elm Park", 3)]}
        next_stops["Dagenham Heathway"] = {"district": [("Becontree", 2), ("Dagenham East", 2)]}
        next_stops["Ealing Broadway"] = {"district": [("End", 0), ("Ealing Common", 3)], "central": [("West Acton", 2), ("End", 0)], "foot": [("Ealing Common", 6)], "bus": [("South Ealing", 13)]}
        next_stops["Ealing Common"] = {"district": [("Ealing Broadway", 3), ("Acton Town", 2)], "piccadilly": [("North Ealing", 2), ("Acton Town", 2)], "foot": [("Ealing Broadway", 6)]}
        next_stops["Earl's Court"] = {"district": [("West Kensington", 2), ("Gloucester Road", 1), ("West Brompton", 2), ("High Street Kensington", 2), ("Kensington (Olympia)", 3)], "piccadilly": [("Barons Court", 3), ("Gloucester Road", 2)]}
        next_stops["East Ham"] = {"district": [("Upton Park", 2), ("Barking", 3)], "hammersmith-city": [("Upton Park", 2), ("Barking", 3)]}
        next_stops["East Putney"] = {"district": [("Southfields", 2), ("Putney Bridge", 2)]}
        next_stops["Edgware Road (Circle Line)"] = {"circle": [("Paddington (H&C Line)", 2), ("Baker Street", 2), ("Paddington", 2)], "district": [("fill", 0), ("End", 0), ("Paddington", 2)], "hammersmith-city": [("Paddington (H&C Line)", 2), ("Baker Street", 2)]}
        next_stops["Elm Park"] = {"district": [("Dagenham East", 3), ("Hornchurch", 2)]}
        next_stops["Embankment"] = {"bakerloo": [("Charing Cross", 1), ("Waterloo", 2)], "circle": [("Westminster", 1), ("Temple", 1)], "district": [("Westminster", 1), ("Temple", 1)], "northern": [("Charing Cross", 1), ("Waterloo", 1)]}
        next_stops["Euston Square"] = {"circle": [("Great Portland Street", 1), ("King's Cross St. Pancras", 2)], "hammersmith-city": [("Great Portland Street", 1), ("King's Cross St. Pancras", 2)], "metropolitan": [("Great Portland Street", 1), ("King's Cross St. Pancras", 2)]}
        next_stops["Farringdon"] = {"circle": [("King's Cross St. Pancras", 3), ("Barbican", 1)], "hammersmith-city": [("King's Cross St. Pancras", 3), ("Barbican", 1)], "metropolitan": [("King's Cross St. Pancras", 3), ("Barbican", 1)]}
        next_stops["Fulham Broadway"] = {"district": [("Parsons Green", 1), ("West Brompton", 2)]}
        next_stops["Gloucester Road"] = {"circle": [("High Street Kensington", 2), ("South Kensington", 1)], "district": [("Earl's Court", 2), ("South Kensington", 1)], "piccadilly": [("Earl's Court", 1), ("South Kensington", 1)]}
        next_stops["Goldhawk Road"] = {"circle": [("Hammersmith (H&C Line)", 2), ("Shepherd's Bush Market", 1)], "hammersmith-city": [("Hammersmith (H&C Line)", 2), ("Shepherd's Bush Market", 1)]}
        next_stops["Great Portland Street"] = {"circle": [("Baker Street", 2), ("Euston Square", 1)], "hammersmith-city": [("Baker Street", 2), ("Euston Square", 1)], "metropolitan": [("Baker Street", 2), ("Euston Square", 1)]}
        next_stops["Gunnersbury"] = {"district": [("Kew Gardens", 2), ("Turnham Green", 3)], "foot": [("Chiswick Park", 4)], "mildmay1": [("Kew Gardens", 2), ("End", 0)]}
        next_stops["Hammersmith (Dist&Picc Line)"] = {"district": [("Ravenscourt Park", 2), ("Barons Court", 1)], "piccadilly": [("Acton Town", 6), ("Barons Court", 1), ("Turnham Green", 4)], "foot": [("Hammersmith (H&C Line)", 1)]}
        next_stops["Hammersmith (H&C Line)"] = {"circle": [("End", 0), ("Goldhawk Road", 2)], "hammersmith-city": [("End", 0), ("Goldhawk Road", 2)], "foot": [("Hammersmith (Dist&Picc Line)", 1)]}
        next_stops["High Street Kensington"] = {"district": [("Earl's Court", 3), ("Notting Hill Gate", 1)], "circle": [("Gloucester Road", 2), ("Notting Hill Gate", 1)]}
        next_stops["Hornchurch"] = {"district": [("Elm Park", 2), ("Upminster Bridge", 2)]}
        next_stops["Kensington (Olympia)"] = {"district": [("End", 0), ("Earl's Court", 3)], "foot": [("West Kensington", 6)], "mildmay2": [("Shepherd's Bush (Central)", 3), ("West Brompton", 3)]}
        next_stops["Kew Gardens"] = {"district": [("Richmond", 4), ("Gunnersbury", 3)], "mildmay1": [("Richmond", 4), ("Gunnersbury", 3)]}
        next_stops["King's Cross St. Pancras"] = {"northern": [("Euston", 2), ("Angel", 2)], "piccadilly": [("Russell Square", 2), ("Caledonian Road", 3)], "victoria": [("Highbury & Islington", 2), ("Euston", 1)], "metropolitan": [("Euston Square", 1), ("Farringdon", 3)], "circle": [("Euston Square", 1), ("Farringdon", 3)], "hammersmith-city": [("Euston Square", 1), ("Farringdon", 3)]}
        next_stops["Ladbroke Grove"] = {"circle": [("Latimer Road", 1), ("Westbourne Park", 1)], "hammersmith-city": [("Latimer Road", 1), ("Westbourne Park", 1)]}
        next_stops["Latimer Road"] = {"circle": [("Wood Lane", 1), ("Ladbroke Grove", 1)], "hammersmith-city": [("Wood Lane", 1), ("Ladbroke Grove", 1)]}
        next_stops["Liverpool Street"] = {"central": [("Bethnal Green", 3), ("Bank", 2)], "circle": [("Moorgate", 1), ("Aldgate", 1)], "hammersmith-city": [("Moorgate", 1), ("Aldgate East", 2)], "metropolitan": [("Moorgate", 1), ("Aldgate", 1)]}
        next_stops["Mansion House"] = {"circle": [("Blackfriars", 1), ("Cannon Street", 1)], "district": [("Blackfriars", 1), ("Cannon Street", 1)]}
        next_stops["Mile End"] = {"central": [("Stratford", 3), ("Bethnal Green", 2)], "district": [("Stepney Green", 2), ("Bow Road", 1)], "hammersmith-city": [("Stepney Green", 2), ("Bow Road", 1)]}
        next_stops["Monument"] = {"circle": [("Cannon Street", 1), ("Tower Hill", 1)], "district": [("Cannon Street", 1), ("Tower Hill", 1)]}
        next_stops["Moorgate"] = {"circle": [("Barbican", 1), ("Liverpool Street", 1)], "hammersmith-city": [("Barbican", 1), ("Liverpool Street", 1)], "metropolitan": [("Barbican", 1), ("Liverpool Street", 1)], "northern": [("Old Street", 1), ("Bank", 2)]}
        next_stops["Neasden"] = {"jubilee": [("Wembley Park", 3), ("Dollis Hill", 1)]}
        next_stops["Notting Hill Gate"] = {"central": [("Queensway", 1), ("Holland Park", 1)], "circle": [("High Street Kensington", 2), ("Bayswater", 1)], "district": [("High Street Kensington", 2), ("Bayswater", 1)]}
        next_stops["Paddington"] = {"bakerloo": [("Warwick Avenue", 2), ("Edgware Road (Bakerloo)", 1)], "circle": [("Bayswater", 2), ("Edgware Road (Circle Line)", 2)], "district": [("Bayswater", 2), ("Edgware Road (Circle Line)", 2)], "foot": [("Paddington (H&C Line)", 2)]}
        next_stops["Paddington (H&C Line)"] = {"circle": [("Royal Oak", 1), ("Edgware Road (Circle Line)", 2)], "hammersmith-city": [("Royal Oak", 1), ("Edgware Road (Circle Line)", 2)], "foot": [("Paddington", 2)]}
        next_stops["Parsons Green"] = {"district": [("Putney Bridge", 2), ("Fulham Broadway", 1)]}
        next_stops["Plaistow"] = {"district": [("West Ham", 2), ("Upton Park", 2)], "hammersmith-city": [("West Ham", 2), ("Upton Park", 2)]}
        next_stops["Putney Bridge"] = {"district": [("East Putney", 2), ("Parsons Green", 2)]}
        next_stops["Ravenscourt Park"] = {"district": [("Stamford Brook", 1), ("Hammersmith (Dist&Picc Line)", 2)]}
        next_stops["Richmond"] = {"district": [("End", 0), ("Kew Gardens", 3)], "mildmay1": [("End", 0), ("Kew Gardens", 3)]}
        next_stops["Royal Oak"] = {"circle": [("Westbourne Park", 2), ("Paddington (H&C Line)", 2)], "hammersmith-city": [("Westbourne Park", 2), ("Paddington (H&C Line)", 2)]}
        next_stops["Shepherd's Bush Market"] = {"circle": [("Goldhawk Road", 1), ("Wood Lane", 1)], "hammersmith-city": [("Goldhawk Road", 1), ("Wood Lane", 1)]}
        next_stops["Sloane Square"] = {"district": [("South Kensington", 2), ("Victoria", 2)], "circle": [("South Kensington", 2), ("Victoria", 2)]}
        next_stops["South Kensington"] = {"district": [("Gloucester Road", 1), ("Sloane Square", 2)], "circle": [("Gloucester Road", 1), ("Sloane Square", 2)], "piccadilly": [("Gloucester Road", 1), ("Knightsbridge", 2)]}
        next_stops["Southfields"] = {"district": [("Wimbledon Park", 2), ("East Putney", 2)]}
        next_stops["St. James's Park"] = {"circle": [("Victoria", 1), ("Westminster", 1)], "district": [("Victoria", 1), ("Westminster", 1)]}
        next_stops["Stamford Brook"] = {"district": [("Turnham Green", 1), ("Ravenscourt Park", 1)]}
        next_stops["Stepney Green"] = {"district": [("Whitechapel", 2), ("Mile End", 2)], "hammersmith-city": [("Whitechapel", 2), ("Mile End", 2)]}
        next_stops["Temple"] = {"circle": [("Embankment", 1), ("Blackfriars", 1)], "district": [("Embankment", 1), ("Blackfriars", 1)]}
        next_stops["Tower Hill"] = {"circle": [("Monument", 1), ("Aldgate", 2)], "district": [("Monument", 1), ("Aldgate East", 2)]}
        next_stops["Turnham Green"] = {"district": [("Chiswick Park", 1), ("Stamford Brook", 1), ("Gunnersbury", 3)], "piccadilly": [("Acton Town", 3), ("Hammersmith (Dist&Picc Line)", 5)]}
        next_stops["Upminster"] = {"district": [("Upminster Bridge", 2), ("End", 0)], "c2c": [("End", 0), ("Barking", 8)]}
        next_stops["Upminster Bridge"] = {"district": [("Hornchurch", 2), ("Upminster", 2)]}
        next_stops["Upney"] = {"district": [("Barking", 2), ("Becontree", 2)]}
        next_stops["Upton Park"] = {"district": [("Plaistow", 2), ("East Ham", 2)], "hammersmith-city": [("Plaistow", 2), ("East Ham", 2)]}
        next_stops["Victoria"] = {"district": [("Sloane Square", 2), ("St. James's Park", 1)], "circle": [("Sloane Square", 2), ("St. James's Park", 1)], "victoria": [("Green Park", 1), ("Pimlico", 1)]}
        next_stops["West Brompton"] = {"district": [("Fulham Broadway", 2), ("Earl's Court", 2)], "mildmay2": [("Kensington (Olympia)", 3), ("End", 0)]}
        next_stops["West Ham"] = {"district": [("Bromley-by-Bow", 2), ("Plaistow", 1)], "hammersmith-city": [("Bromley-by-Bow", 2), ("Plaistow", 1)], "jubilee": [("Canning Town", 2), ("Stratford", 3)], "c2c": [("Barking", 5), ("End", 0)]}
        next_stops["West Kensington"] = {"district": [("Barons Court", 1), ("Earl's Court", 2)], "foot": [("Kensington (Olympia)", 6)]}
        next_stops["Westbourne Park"] = {"circle": [("Ladbroke Grove", 1), ("Royal Oak", 2)], "hammersmith-city": [("Ladbroke Grove", 1), ("Royal Oak", 2)]}
        next_stops["Westminster"] = {"circle": [("St. James's Park", 1), ("Embankment", 1)], "district": [("St. James's Park", 1), ("Embankment", 1)], "jubilee": [("Green Park", 2), ("Waterloo", 1)]}
        next_stops["Whitechapel"] = {"district": [("Aldgate East", 2), ("Stepney Green", 2)], "hammersmith-city": [("Aldgate East", 2), ("Stepney Green", 2)]}
        next_stops["Wimbledon"] = {"district": [("End", 0), ("Wimbledon Park", 2)], "tram": [("Morden", 8)], "bus": [("South Wimbledon", 11)]}
        next_stops["Wimbledon Park"] = {"district": [("Wimbledon", 3), ("Southfields", 2)]}
        next_stops["Wood Lane"] = {"circle": [("Shepherd's Bush Market", 1), ("Latimer Road", 1)], "hammersmith-city": [("Shepherd's Bush Market", 1), ("Latimer Road", 1)]}
    except Exception as e:
        print(e)

    _next_stops = dict(next_stops).copy()

    lines.append("foot")
    lines.append("mildmay1")
    lines.append("c2c")

    for key in _next_stops:
        next_stops[key] = {}
        for line in lines:
            try:
                next_line_stops = _next_stops[key][line]
                next_stops[key][line] = next_line_stops
            except:
                (next_stops.pop(key, None) if next_stops[key] == {} else None) if line == lines[-1] else None

    return next_stops

save = 0
load = 1

local_dir = os.path.dirname(__file__)

if save and load:
    print("no")
    sys.exit(0)
elif save:
    path = os.path.join(local_dir, "pickles/next_stops.pkl")
    with open(path, "wb") as f:
        next_stops = make_next_stops()
        pickle.dump(next_stops, f)
elif load:
    path = os.path.join(local_dir, "pickles/next_stops.pkl")
    with open(path, "rb") as f:
        next_stops = pickle.load(f)
else:
    next_stops = make_next_stops()
