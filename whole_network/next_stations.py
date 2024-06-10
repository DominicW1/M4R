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
        next_stops["Alperton"] = {"piccadilly": [("Sudbury Town", 2), ("Park Royal", 2)]}
        next_stops["Amersham"] = {"metropolitan": [("End", 0), ("Chalfont & Latimer", 3)], "chiltern": [("End", 0), ("Chalfont & Latimer", 3)]}
        next_stops["Angel"] = {"northern": [("King's Cross St. Pancras", 2), ("Old Street", 2)]}
        next_stops["Archway"] = {"northern": [("Highgate", 2), ("Tufnell Park", 1)]}
        next_stops["Arnos Grove"] = {"piccadilly": [("Bounds Green", 2), ("Southgate", 2)]}
        next_stops["Arsenal"] = {"piccadilly": [("Holloway Road", 1), ("Finsbury Park", 1)]}
        next_stops["Baker Street"] = {"bakerloo": [("Marylebone", 1), ("Regent's Park", 1)], "circle": [("Edgware Road (Circle Line)", 2), ("Great Portland Street", 1)], "hammersmith-city": [("Edgware Road (Circle Line)", 2), ("Great Portland Street", 1)], "jubilee": [("St. John's Wood", 2), ("Bond Street", 2)], "metropolitan": [("Finchley Road", 5), ("Great Portland Street", 2)]}
        next_stops["Balham"] = {"northern": [("Clapham South", 2), ("Tooting Bec", 1)]}
        next_stops["Bank"] = {"central": [("Liverpool Street", 2), ("St. Paul's", 1)], "northern": [("Moorgate", 2), ("London Bridge", 1)], "waterloo-city": [("End", 0), ("Waterloo", 3)]}
        next_stops["Barbican"] = {"circle": [("Farringdon", 1), ("Moorgate", 1)], "metropolitan": [("Farringdon", 1), ("Moorgate", 1)], "hammersmith-city": [("Farringdon", 1), ("Moorgate", 1)]}
        next_stops["Barking"] = {"district": [("East Ham", 3), ("Upney", 2)], "hammersmith-city": [("East Ham", 3), ("End", 0)], "suffragette": [("End", 0), ("Walthamstow Central", 15)], "c2c": [("Upminster", 8), ("West Ham", 5)]}
        next_stops["Barkingside"] = {"central": [("Fairlop", 1), ("Newbury Park", 1)]}
        next_stops["Barons Court"] = {"district": [("Hammersmith (Dist&Picc Line)", 1), ("West Kensington", 1)], "piccadilly": [("Hammersmith (Dist&Picc Line)", 2), ("Earl's Court", 3)]}
        next_stops["Battersea Power Station"] = {"northern": [("Nine Elms", 2), ("End", 0)], "bus": [("Vauxhall", 8)]}
        next_stops["Bayswater"] = {"district": [("Notting Hill Gate", 1), ("Paddington", 2)], "circle": [("Notting Hill Gate", 1), ("Paddington", 2)], "foot": [("Queensway", 1)]}
        next_stops["Becontree"] = {"district": [("Upney", 2), ("Dagenham Heathway", 2)]}
        next_stops["Belsize Park"] = {"northern": [("Hampstead", 2), ("Chalk Farm", 1)]}
        next_stops["Bermondsey"] = {"jubilee": [("London Bridge", 2), ("Canada Water", 1)]}
        next_stops["Bethnal Green"] = {"central": [("Mile End", 2), ("Liverpool Street", 3)]}
        next_stops["Blackfriars"] = {"circle": [("Temple", 1), ("Mansion House", 2)], "district": [("Temple", 1), ("Mansion House", 2)]}
        next_stops["Blackhorse Road"] = {"victoria": [("Walthamstow Central", 2), ("Tottenham Hale", 2)]}
        next_stops["Bond Street"] = {"central": [("Oxford Circus", 1), ("Marble Arch", 1)], "jubilee": [("Baker Street", 2), ("Green Park", 1)]}
        next_stops["Borough"] = {"northern": [("London Bridge", 1), ("Elephant & Castle", 2)]}
        next_stops["Boston Manor"] = {"piccadilly": [("Osterley", 3), ("Northfields", 2)]}
        next_stops["Bounds Green"] = {"piccadilly": [("Wood Green", 2), ("Arnos Grove", 3)]}
        next_stops["Bow Road"] = {"district": [("Mile End", 1), ("Bromley-by-Bow", 2)], "hammersmith-city": [("Mile End", 1), ("Bromley-by-Bow", 2)]}
        next_stops["Brent Cross"] = {"northern": [("Hendon Central", 2), ("Golders Green", 2)]}
        next_stops["Brixton"] = {"victoria": [("Stockwell", 2), ("End", 0)]}
        next_stops["Bromley-by-Bow"] = {"district": [("Bow Road", 2), ("West Ham", 2)], "hammersmith-city": [("Bow Road", 2), ("West Ham", 2)]}
        next_stops["Buckhurst Hill"] = {"central": [("Loughton", 2), ("Woodford", 2)]}
        next_stops["Burnt Oak"] = {"northern": [("Edgware", 2), ("Colindale", 2)]}
        next_stops["Caledonian Road"] = {"piccadilly": [("King's Cross St. Pancras", 3), ("Holloway Road", 1)]}
        next_stops["Camden Town"] = {"northern": [("Chalk Farm", 1), ("Mornington Crescent", 1), ("Kentish Town", 1), ("Euston", 3)]}
        next_stops["Canada Water"] = {"jubilee": [("Bermondsey", 1), ("Canary Wharf", 2)]}
        next_stops["Canary Wharf"] = {"jubilee": [("Canada Water", 2), ("North Greenwich", 2)]}
        next_stops["Canning Town"] = {"jubilee": [("North Greenwich", 2), ("West Ham", 2)]}
        next_stops["Cannon Street"] = {"circle": [("Mansion House", 1), ("Monument", 1)], "district": [("Mansion House", 1), ("Monument", 1)]}
        next_stops["Canons Park"] = {"jubilee": [("Stanmore", 2), ("Queensbury", 2)], "foot": [("Edgware", 8)], "bus": [("Edgware", 8)]}
        next_stops["Chalfont & Latimer"] = {"metropolitan": [("Amersham", 4), ("Chorleywood", 3), ("Chesham", 8)], "chiltern": [("Amersham", 4), ("Chorleywood", 3)]}
        next_stops["Chalk Farm"] = {"northern": [("Belsize Park", 1), ("Camden Town", 1)]}
        next_stops["Chancery Lane"] = {"central": [("St. Paul's", 1), ("Holborn", 1)], "foot": [("Farringdon", 3)]}
        next_stops["Charing Cross"] = {"bakerloo": [("Piccadilly Circus", 2), ("Embankment", 1)], "northern": [("Leicester Square", 1), ("Embankment", 1)], "foot": [("Embankment", 1)]}
        next_stops["Chesham"] = {"metropolitan": [("End", 0), ("Chalfont & Latimer", 8)]}
        next_stops["Chigwell"] = {"central": [("Roding Valley", 3), ("Grange Hill", 2)]}
        next_stops["Chiswick Park"] = {"district": [("Acton Town", 2), ("Turnham Green", 2)], "foot": [("Gunnersbury", 4)]}
        next_stops["Chorleywood"] = {"metropolitan": [("Chalfont & Latimer", 4), ("Rickmansworth", 4)], "chiltern": [("Chalfont & Latimer", 4), ("Rickmansworth", 4)]}
        next_stops["Clapham Common"] = {"northern": [("Clapham North", 1), ("Clapham South", 1)]}
        next_stops["Clapham North"] = {"northern": [("Stockwell", 1), ("Clapham Common", 1)]}
        next_stops["Clapham South"] = {"northern": [("Clapham Common", 1), ("Balham", 2)]}
        next_stops["Cockfosters"] = {"piccadilly": [("Oakwood", 2), ("End", 0)], "bus": [("High Barnet", 27)]}
        next_stops["Colindale"] = {"northern": [("Burnt Oak", 2), ("Hendon Central", 2)]}
        next_stops["Colliers Wood"] = {"northern": [("Tooting Broadway", 2), ("South Wimbledon", 2)]}
        next_stops["Covent Garden"] = {"piccadilly": [("Leicester Square", 1), ("Holborn", 2)]}
        next_stops["Croxley"] = {"metropolitan": [("Watford", 3), ("Moor Park", 4)]}
        next_stops["Dagenham East"] = {"district": [("Dagenham Heathway", 2), ("Elm Park", 3)]}
        next_stops["Dagenham Heathway"] = {"district": [("Becontree", 2), ("Dagenham East", 2)]}
        next_stops["Debden"] = {"central": [("Theydon Bois", 3), ("Loughton", 3)]}
        next_stops["Dollis Hill"] = {"jubilee": [("Neasden", 1), ("Willesden Green", 2)]}
        next_stops["Ealing Broadway"] = {"district": [("End", 0), ("Ealing Common", 3)], "central": [("West Acton", 2), ("End", 0)], "foot": [("Ealing Common", 6)], "bus": [("South Ealing", 13)]}
        next_stops["Ealing Common"] = {"district": [("Ealing Broadway", 3), ("Acton Town", 2)], "piccadilly": [("North Ealing", 2), ("Acton Town", 2)], "foot": [("Ealing Broadway", 6)]}
        next_stops["Earl's Court"] = {"district": [("West Kensington", 2), ("Gloucester Road", 1), ("West Brompton", 2), ("High Street Kensington", 2), ("Kensington (Olympia)", 3)], "piccadilly": [("Barons Court", 3), ("Gloucester Road", 2)]}
        next_stops["East Acton"] = {"central": [("White City", 3), ("North Acton", 2)]}
        next_stops["East Finchley"] = {"northern": [("Finchley Central", 3), ("Highgate", 2)]}
        next_stops["East Ham"] = {"district": [("Upton Park", 2), ("Barking", 3)], "hammersmith-city": [("Upton Park", 2), ("Barking", 3)]}
        next_stops["East Putney"] = {"district": [("Southfields", 2), ("Putney Bridge", 2)]}
        next_stops["Eastcote"] = {"metropolitan": [("Ruislip Manor", 2), ("Rayners Lane", 3)], "piccadilly": [("Ruislip Manor", 2), ("Rayners Lane", 3)]}
        next_stops["Edgware"] = {"northern": [("End", 0), ("Burnt Oak", 2)], "foot": [("Canons Park", 8)], "bus": [("Canons Park", 8)]}
        next_stops["Edgware Road (Bakerloo)"] = {"bakerloo": [("Paddington", 2), ("Marylebone", 1)], "foot": [("Edgware Road (Circle Line)", 1)]}
        next_stops["Edgware Road (Circle Line)"] = {"circle": [("Paddington (H&C Line)", 2), ("Baker Street", 2), ("Paddington", 2)], "district": [("fill", 0), ("End", 0), ("Paddington", 2)], "hammersmith-city": [("Paddington (H&C Line)", 2), ("Baker Street", 2)], "foot": [("Edgware Road (Bakerloo)", 1)]}
        next_stops["Elephant & Castle"] = {"bakerloo": [("Lambeth North", 2), ("End", 0)], "northern": [("Borough", 2), ("Kennington", 1)]}
        next_stops["Elm Park"] = {"district": [("Dagenham East", 3), ("Hornchurch", 2)]}
        next_stops["Embankment"] = {"bakerloo": [("Charing Cross", 1), ("Waterloo", 2)], "circle": [("Westminster", 1), ("Temple", 1)], "district": [("Westminster", 1), ("Temple", 1)], "northern": [("Charing Cross", 1), ("Waterloo", 1)], "foot": [("Charing Cross", 1)]}
        next_stops["Epping"] = {"central": [("End", 0), ("Theydon Bois", 2)]}
        next_stops["Euston"] = {"northern": [("Mornington Crescent", 2), ("Warren Street", 1), ("Camden Town", 3), ("King's Cross St. Pancras", 1)], "victoria": [("King's Cross St. Pancras", 1), ("Warren Street", 1)], "foot": [("Euston Square", 3)]}
        next_stops["Euston Square"] = {"circle": [("Great Portland Street", 1), ("King's Cross St. Pancras", 2)], "hammersmith-city": [("Great Portland Street", 1), ("King's Cross St. Pancras", 2)], "metropolitan": [("Great Portland Street", 1), ("King's Cross St. Pancras", 2)], "foot": [("Warren Street", 2), ("Euston", 3)]}
        next_stops["Fairlop"] = {"central": [("Hainault", 1), ("Barkingside", 1)]}
        next_stops["Farringdon"] = {"circle": [("King's Cross St. Pancras", 3), ("Barbican", 1)], "hammersmith-city": [("King's Cross St. Pancras", 3), ("Barbican", 1)], "metropolitan": [("King's Cross St. Pancras", 3), ("Barbican", 1)], "foot": [("Chancery Lane", 3)]}
        next_stops["Finchley Central"] = {"northern": [("Mill Hill East", 2), ("East Finchley", 3), ("West Finchley", 2)]}
        next_stops["Finchley Road"] = {"jubilee": [("West Hampstead", 1), ("Swiss Cottage", 1)], "metropolitan": [("Wembley Park", 7), ("Baker Street", 5)]}
        next_stops["Finsbury Park"] = {"piccadilly": [("Arsenal", 1), ("Manor House", 2)], "victoria": [("Seven Sisters", 4), ("Highbury & Islington", 3)]}
        next_stops["Fulham Broadway"] = {"district": [("Parsons Green", 1), ("West Brompton", 2)]}
        next_stops["Gants Hill"] = {"central": [("Newbury Park", 3), ("Redbridge", 1)]}
        next_stops["Gloucester Road"] = {"circle": [("High Street Kensington", 2), ("South Kensington", 1)], "district": [("Earl's Court", 2), ("South Kensington", 1)], "piccadilly": [("Earl's Court", 1), ("South Kensington", 1)]}
        next_stops["Golders Green"] = {"northern": [("Brent Cross", 2), ("Hampstead", 3)]}
        next_stops["Goldhawk Road"] = {"circle": [("Hammersmith (H&C Line)", 2), ("Shepherd's Bush Market", 1)], "hammersmith-city": [("Hammersmith (H&C Line)", 2), ("Shepherd's Bush Market", 1)]}
        next_stops["Goodge Street"] = {"northern": [("Warren Street", 1), ("Tottenham Court Road", 1)]}
        next_stops["Grange Hill"] = {"central": [("Chigwell", 2), ("Hainault", 2)]}
        next_stops["Great Portland Street"] = {"circle": [("Baker Street", 2), ("Euston Square", 1)], "hammersmith-city": [("Baker Street", 2), ("Euston Square", 1)], "metropolitan": [("Baker Street", 2), ("Euston Square", 1)], "foot": [("Regent's Park", 1)]}
        next_stops["Green Park"] = {"jubilee": [("Bond Street", 2), ("Westminster", 2)], "victoria": [("Oxford Circus", 2), ("Victoria", 2)], "piccadilly": [("Hyde Park Corner", 2), ("Piccadilly Circus", 1)]}
        next_stops["Greenford"] = {"central": [("Perivale", 2), ("Northolt", 2)]}
        next_stops["Gunnersbury"] = {"district": [("Kew Gardens", 2), ("Turnham Green", 3)], "foot": [("Chiswick Park", 4)], "mildmay1": [("Kew Gardens", 2), ("End", 0)]}
        next_stops["Hainault"] = {"central": [("Grange Hill", 2), ("Fairlop", 2)]}
        next_stops["Hammersmith (Dist&Picc Line)"] = {"district": [("Ravenscourt Park", 2), ("Barons Court", 1)], "piccadilly": [("Acton Town", 6), ("Barons Court", 1), ("Turnham Green", 4)], "foot": [("Hammersmith (H&C Line)", 1)]}
        next_stops["Hammersmith (H&C Line)"] = {"circle": [("End", 0), ("Goldhawk Road", 2)], "hammersmith-city": [("End", 0), ("Goldhawk Road", 2)], "foot": [("Hammersmith (Dist&Picc Line)", 1)]}
        next_stops["Hampstead"] = {"northern": [("Golders Green", 4), ("Belsize Park", 2)]}
        next_stops["Hanger Lane"] = {"central": [("North Acton", 3), ("Perivale", 2)], "foot": [("Park Royal", 3)]}
        next_stops["Harlesden"] = {"bakerloo": [("Stonebridge Park", 2), ("Willesden Junction", 2)], "lioness": [("Stonebridge Park", 2), ("Willesden Junction", 2)]}
        next_stops["Harrow & Wealdstone"] = {"bakerloo": [("End", 0), ("Kenton", 2)], "lioness": [("End", 0), ("Kenton", 2)], "bus": [("Harrow-on-the-Hill", 10)]}
        next_stops["Harrow-on-the-Hill"] = {"metropolitan": [("West Harrow", 2), ("Northwick Park", 2), ("North Harrow", 3)], "bus": [("Harrow & Wealdstone", 10)]} # , ("Moor Park", 7), ("Wembley Park", 4)
        next_stops["Hatton Cross"] = {"piccadilly": [("Heathrow Terminals 2 & 3", 4), ("Hounslow West", 3), ("Heathrow Terminal 4", 2)]}
        next_stops["Heathrow Terminal 4"] = {"piccadilly": [("Heathrow Terminals 2 & 3", 5), ("End", 0)]}
        next_stops["Heathrow Terminals 2 & 3"] = {"piccadilly": [("Heathrow Terminal 5", 3), ("Hatton Cross", 3)]}
        next_stops["Heathrow Terminal 5"] = {"piccadilly": [("End", 0), ("Heathrow Terminals 2 & 3", 3)]}
        next_stops["Hendon Central"] = {"northern": [("Colindale", 2), ("Brent Cross", 2)]}
        next_stops["High Barnet"] = {"northern": [("End", 0), ("Totteridge & Whetstone", 3)], "bus": [("Cockfosters", 27)], "bus": [("Oakwood", 23)]}
        next_stops["High Street Kensington"] = {"district": [("Earl's Court", 3), ("Notting Hill Gate", 1)], "circle": [("Gloucester Road", 2), ("Notting Hill Gate", 1)]}
        next_stops["Highbury & Islington"] = {"victoria": [("Finsbury Park", 2), ("King's Cross St. Pancras", 2)], "great_northern": [("End", 0), ("Old Street", 5)]}
        next_stops["Highgate"] = {"northern": [("East Finchley", 2), ("Archway", 2)]}
        next_stops["Hillingdon"] = {"metropolitan": [("Uxbridge", 4), ("Ickenham", 2)], "piccadilly": [("Uxbridge", 4), ("Ickenham", 2)]}
        next_stops["Holborn"] = {"central": [("Chancery Lane", 1), ("Tottenham Court Road", 1)], "piccadilly": [("Covent Garden", 1), ("Russell Square", 2)]}
        next_stops["Holland Park"] = {"central": [("Notting Hill Gate", 1), ("Shepherd's Bush (Central)", 1)]}
        next_stops["Holloway Road"] = {"piccadilly": [("Caledonian Road", 1), ("Arsenal", 1)]}
        next_stops["Hornchurch"] = {"district": [("Elm Park", 2), ("Upminster Bridge", 2)]}
        next_stops["Hounslow Central"] = {"piccadilly": [("Hounslow West", 2), ("Hounslow East", 1)]}
        next_stops["Hounslow East"] = {"piccadilly": [("Hounslow Central", 1), ("Osterley", 2)]}
        next_stops["Hounslow West"] = {"piccadilly": [("Hatton Cross", 4), ("Hounslow Central", 2)]}
        next_stops["Hyde Park Corner"] = {"piccadilly": [("Knightsbridge", 1), ("Green Park", 2)]}
        next_stops["Ickenham"] = {"metropolitan": [("Hillingdon", 1), ("Ruislip", 2)], "piccadilly": [("Hillingdon", 2), ("Ruislip", 2)], "foot": [("West Ruislip", 6)]}
        next_stops["Kennington"] = {"northern": [("Elephant & Castle", 1), ("Oval", 1), ("Waterloo", 2), ("Nine Elms", 2)]}
        next_stops["Kensal Green"] = {"bakerloo": [("Willesden Junction", 3), ("Queen's Park", 3)], "lioness": [("Willesden Junction", 3), ("Queen's Park", 3)]}
        next_stops["Kensington (Olympia)"] = {"district": [("End", 0), ("Earl's Court", 3)], "foot": [("West Kensington", 6)], "mildmay2": [("Shepherd's Bush (Central)", 3), ("West Brompton", 3)]}
        next_stops["Kentish Town"] = {"northern": [("Tufnell Park", 1), ("Camden Town", 2)]}
        next_stops["Kenton"] = {"bakerloo": [("Harrow & Wealdstone", 2), ("South Kenton", 2)], "lioness": [("Harrow & Wealdstone", 2), ("South Kenton", 2)], "foot": [("Northwick Park", 2)]}
        next_stops["Kew Gardens"] = {"district": [("Richmond", 4), ("Gunnersbury", 3)], "mildmay1": [("Richmond", 4), ("Gunnersbury", 3)]}
        next_stops["Kilburn"] = {"jubilee": [("Willesden Green", 2), ("West Hampstead", 2)]}
        next_stops["Kilburn Park"] = {"bakerloo": [("Queen's Park", 2), ("Maida Vale", 2)]}
        next_stops["King's Cross St. Pancras"] = {"northern": [("Euston", 2), ("Angel", 2)], "piccadilly": [("Russell Square", 2), ("Caledonian Road", 3)], "victoria": [("Highbury & Islington", 2), ("Euston", 1)], "metropolitan": [("Euston Square", 1), ("Farringdon", 3)], "circle": [("Euston Square", 1), ("Farringdon", 3)], "hammersmith-city": [("Euston Square", 1), ("Farringdon", 3)]}
        next_stops["Kingsbury"] = {"jubilee": [("Queensbury", 2), ("Wembley Park", 3)]}
        next_stops["Knightsbridge"] = {"piccadilly": [("South Kensington", 2), ("Hyde Park Corner", 1)]}
        next_stops["Ladbroke Grove"] = {"circle": [("Latimer Road", 1), ("Westbourne Park", 1)], "hammersmith-city": [("Latimer Road", 1), ("Westbourne Park", 1)]}
        next_stops["Lambeth North"] = {"bakerloo": [("Waterloo", 2), ("Elephant & Castle", 3)]}
        next_stops["Lancaster Gate"] = {"central": [("Marble Arch", 1), ("Queensway", 2)]}
        next_stops["Latimer Road"] = {"circle": [("Wood Lane", 1), ("Ladbroke Grove", 1)], "hammersmith-city": [("Wood Lane", 1), ("Ladbroke Grove", 1)]}
        next_stops["Leicester Square"] = {"northern": [("Tottenham Court Road", 1), ("Charing Cross", 1)], "piccadilly": [("Piccadilly Circus", 1), ("Covent Garden", 1)]}
        next_stops["Leyton"] = {"central": [("Leytonstone", 2), ("Stratford", 2)], "bus": [("Walthamstow Central", 20)]}
        next_stops["Leytonstone"] = {"central": [("Snaresbrook", 2), ("Leyton", 2), ("Wanstead", 2)], "suffragette": [("End", 0), ("Walthamstow Central", 10)]}
        next_stops["Liverpool Street"] = {"central": [("Bethnal Green", 3), ("Bank", 2)], "circle": [("Moorgate", 1), ("Aldgate", 1)], "hammersmith-city": [("Moorgate", 1), ("Aldgate East", 2)], "metropolitan": [("Moorgate", 1), ("Aldgate", 1)]}
        next_stops["London Bridge"] = {"northern": [("Bank", 1), ("Borough", 1)], "jubilee": [("Southwark", 1), ("Bermondsey", 2)]}
        next_stops["Loughton"] = {"central": [("Debden", 3), ("Buckhurst Hill", 2)]}
        next_stops["Maida Vale"] = {"bakerloo": [("Kilburn Park", 2), ("Warwick Avenue", 1)]}
        next_stops["Manor House"] = {"piccadilly": [("Finsbury Park", 2), ("Turnpike Lane", 3)]}
        next_stops["Mansion House"] = {"circle": [("Blackfriars", 1), ("Cannon Street", 1)], "district": [("Blackfriars", 1), ("Cannon Street", 1)]}
        next_stops["Marble Arch"] = {"central": [("Bond Street", 1), ("Lancaster Gate", 1)]}
        next_stops["Marylebone"] = {"bakerloo": [("Edgware Road (Bakerloo)", 1), ("Baker Street", 1)]}
        next_stops["Mile End"] = {"central": [("Stratford", 3), ("Bethnal Green", 2)], "district": [("Stepney Green", 2), ("Bow Road", 1)], "hammersmith-city": [("Stepney Green", 2), ("Bow Road", 1)]}
        next_stops["Mill Hill East"] = {"northern": [("End", 0), ("Finchley Central", 2)]}
        next_stops["Monument"] = {"circle": [("Cannon Street", 1), ("Tower Hill", 1)], "district": [("Cannon Street", 1), ("Tower Hill", 1)]}
        next_stops["Moor Park"] = {"metropolitan": [("Rickmansworth", 3), ("Northwood", 2), ("Croxley", 4)]} # , ("fill", 0), ("Harrow-on-the-Hill", 9)
        next_stops["Moorgate"] = {"circle": [("Barbican", 1), ("Liverpool Street", 1)], "hammersmith-city": [("Barbican", 1), ("Liverpool Street", 1)], "metropolitan": [("Barbican", 1), ("Liverpool Street", 1)], "northern": [("Old Street", 1), ("Bank", 2)]}
        next_stops["Morden"] = {"northern": [("South Wimbledon", 2), ("End", 0)], "tram": [("Wimbledon", 10)]}
        next_stops["Mornington Crescent"] = {"northern": [("Camden Town", 1), ("Euston", 1)]}
        next_stops["Neasden"] = {"jubilee": [("Wembley Park", 3), ("Dollis Hill", 1)]}
        next_stops["Newbury Park"] = {"central": [("Barkingside", 1), ("Gants Hill", 3)]}
        next_stops["Nine Elms"] = {"northern": [("Kennington", 2), ("Battersea Power Station", 2)]}
        next_stops["North Acton"] = {"central": [("East Acton", 1), ("Hanger Lane", 3), ("fill", 0), ("West Acton", 2)]}
        next_stops["North Ealing"] = {"piccadilly": [("Park Royal", 2), ("Ealing Common", 2)], "foot": [("West Acton", 4)]}
        next_stops["North Greenwich"] = {"jubilee": [("Canary Wharf", 2), ("Canning Town", 2)]}
        next_stops["North Harrow"] = {"metropolitan": [("Pinner", 2), ("Harrow-on-the-Hill", 3)], "foot": [("Rayners Lane", 7)]}
        next_stops["North Wembley"] = {"bakerloo": [("South Kenton", 2), ("Wembley Central", 2)], "lioness": [("South Kenton", 2), ("Wembley Central", 2)]}
        next_stops["Northfields"] = {"piccadilly": [("Boston Manor", 1), ("South Ealing", 1)]}
        next_stops["Northolt"] = {"central": [("Greenford", 2), ("South Ruislip", 2)]}
        next_stops["Northwick Park"] = {"metropolitan": [("Harrow-on-the-Hill", 2), ("Preston Road", 2)], "foot": [("Kenton", 2)]}
        next_stops["Northwood"] = {"metropolitan": [("Moor Park", 2), ("Northwood Hills", 2)]}
        next_stops["Northwood Hills"] = {"metropolitan": [("Northwood", 2), ("Pinner", 2)]}
        next_stops["Notting Hill Gate"] = {"central": [("Queensway", 1), ("Holland Park", 1)], "circle": [("High Street Kensington", 2), ("Bayswater", 1)], "district": [("High Street Kensington", 2), ("Bayswater", 1)]}
        next_stops["Oakwood"] = {"piccadilly": [("Southgate", 2), ("Cockfosters", 2)], "bus": [("High Barnet", 23)]}
        next_stops["Old Street"] = {"northern": [("Angel", 2), ("Moorgate", 1)], "great_northern": [("Highbury & Islington", 5), ("End", 0)]}
        next_stops["Osterley"] = {"piccadilly": [("Hounslow East", 2), ("Boston Manor", 3)]}
        next_stops["Oval"] = {"northern": [("Kennington", 1), ("Stockwell", 2)]}
        next_stops["Oxford Circus"] = {"bakerloo": [("Regent's Park", 2), ("Piccadilly Circus", 2)], "central": [("Tottenham Court Road", 1), ("Bond Street", 1)], "victoria": [("Warren Street", 1), ("Green Park", 1)]}
        next_stops["Paddington"] = {"bakerloo": [("Warwick Avenue", 2), ("Edgware Road (Bakerloo)", 1)], "circle": [("Bayswater", 2), ("Edgware Road (Circle Line)", 2)], "district": [("Bayswater", 2), ("Edgware Road (Circle Line)", 2)], "foot": [("Paddington (H&C Line)", 2)]}
        next_stops["Paddington (H&C Line)"] = {"circle": [("Royal Oak", 1), ("Edgware Road (Circle Line)", 2)], "hammersmith-city": [("Royal Oak", 1), ("Edgware Road (Circle Line)", 2)], "foot": [("Paddington", 2)]}
        next_stops["Park Royal"] = {"piccadilly": [("Alperton", 2), ("North Ealing", 2)], "foot": [("Hanger Lane", 3)]}
        next_stops["Parsons Green"] = {"district": [("Putney Bridge", 2), ("Fulham Broadway", 1)]}
        next_stops["Perivale"] = {"central": [("Hanger Lane", 2), ("Greenford", 2)]}
        next_stops["Piccadilly Circus"] = {"bakerloo": [("Oxford Circus", 2), ("Charing Cross", 1)], "piccadilly": [("Green Park", 1), ("Leicester Square", 1)]}
        next_stops["Pimlico"] = {"victoria": [("Victoria", 2), ("Vauxhall", 1)]}
        next_stops["Pinner"] = {"metropolitan": [("Northwood Hills", 2), ("North Harrow", 2)]}
        next_stops["Plaistow"] = {"district": [("West Ham", 2), ("Upton Park", 2)], "hammersmith-city": [("West Ham", 2), ("Upton Park", 2)]}
        next_stops["Preston Road"] = {"metropolitan": [("Northwick Park", 2), ("Wembley Park", 2)]}
        next_stops["Putney Bridge"] = {"district": [("East Putney", 2), ("Parsons Green", 2)]}
        next_stops["Queen's Park"] = {"bakerloo": [("Kensal Green", 3), ("Kilburn Park", 1)], "lioness": [("Kensal Green", 3), ("End", 0)]}
        next_stops["Queensbury"] = {"jubilee": [("Canons Park", 2), ("Kingsbury", 2)]}
        next_stops["Queensway"] = {"central": [("Lancaster Gate", 2), ("Notting Hill Gate", 1)], "foot": [("Bayswater", 1)]}
        next_stops["Ravenscourt Park"] = {"district": [("Stamford Brook", 1), ("Hammersmith (Dist&Picc Line)", 2)]}
        next_stops["Rayners Lane"] = {"metropolitan": [("Eastcote", 3), ("West Harrow", 2)], "piccadilly": [("Eastcote", 3), ("South Harrow", 3)], "foot": [("North Harrow", 7)]}
        next_stops["Redbridge"] = {"central": [("Gants Hill", 2), ("Wanstead", 2)]}
        next_stops["Regent's Park"] = {"bakerloo": [("Baker Street", 2), ("Oxford Circus", 2)], "foot": [("Great Portland Street", 1)]}
        next_stops["Richmond"] = {"district": [("End", 0), ("Kew Gardens", 3)], "mildmay1": [("End", 0), ("Kew Gardens", 3)]}
        next_stops["Rickmansworth"] = {"metropolitan": [("Chorleywood", 3), ("Moor Park", 3), ("fill", 0), ("Croxley", 4)], "chiltern": [("Chorleywood", 3), ("End", 0)]} # ("fill", 0), 
        next_stops["Roding Valley"] = {"central": [("Woodford", 2), ("Chigwell", 3)]}
        next_stops["Royal Oak"] = {"circle": [("Westbourne Park", 2), ("Paddington (H&C Line)", 2)], "hammersmith-city": [("Westbourne Park", 2), ("Paddington (H&C Line)", 2)]}
        next_stops["Ruislip"] = {"metropolitan": [("Ickenham", 2), ("Ruislip Manor", 1)], "piccadilly": [("Ickenham", 2), ("Ruislip Manor", 1)]}
        next_stops["Ruislip Gardens"] = {"central": [("South Ruislip", 1), ("West Ruislip", 2)]}
        next_stops["Ruislip Manor"] = {"metropolitan": [("Ruislip", 1), ("Eastcote", 2)], "piccadilly": [("Ruislip", 1), ("Eastcote", 2)]}
        next_stops["Russell Square"] = {"piccadilly": [("Holborn", 1), ("King's Cross St. Pancras", 2)]}
        next_stops["Seven Sisters"] = {"victoria": [("Tottenham Hale", 1), ("Finsbury Park", 3)]}
        next_stops["Shepherd's Bush (Central)"] = {"central": [("Holland Park", 1), ("White City", 3)], "mildmay2": [("End", 0), ("Kensington (Olympia)", 3)]}
        next_stops["Shepherd's Bush Market"] = {"circle": [("Goldhawk Road", 1), ("Wood Lane", 1)], "hammersmith-city": [("Goldhawk Road", 1), ("Wood Lane", 1)]}
        next_stops["Sloane Square"] = {"district": [("South Kensington", 2), ("Victoria", 2)], "circle": [("South Kensington", 2), ("Victoria", 2)]}
        next_stops["Snaresbrook"] = {"central": [("South Woodford", 2), ("Leytonstone", 2)]}
        next_stops["South Ealing"] = {"piccadilly": [("Northfields", 1), ("Acton Town", 3)], "bus": [("Ealing Broadway", 13)]}
        next_stops["South Harrow"] = {"piccadilly": [("Rayners Lane", 3), ("Sudbury Hill", 2)]}
        next_stops["South Kensington"] = {"district": [("Gloucester Road", 1), ("Sloane Square", 2)], "circle": [("Gloucester Road", 1), ("Sloane Square", 2)], "piccadilly": [("Gloucester Road", 1), ("Knightsbridge", 2)]}
        next_stops["South Kenton"] = {"bakerloo": [("Kenton", 2), ("North Wembley", 2)], "lioness": [("Kenton", 2), ("North Wembley", 2)]}
        next_stops["South Ruislip"] = {"central": [("Northolt", 2), ("Ruislip Gardens", 1)]}
        next_stops["South Wimbledon"] = {"northern": [("Colliers Wood", 2), ("Morden", 2)], "bus": [("Wimbledon", 11)]}
        next_stops["South Woodford"] = {"central": [("Woodford", 2), ("Snaresbrook", 2)]}
        next_stops["Southfields"] = {"district": [("Wimbledon Park", 2), ("East Putney", 2)]}
        next_stops["Southgate"] = {"piccadilly": [("Arnos Grove", 4), ("Oakwood", 3)]}
        next_stops["Southwark"] = {"jubilee": [("Waterloo", 1), ("London Bridge", 2)]}
        next_stops["St. James's Park"] = {"circle": [("Victoria", 1), ("Westminster", 1)], "district": [("Victoria", 1), ("Westminster", 1)]}
        next_stops["St. John's Wood"] = {"jubilee": [("Swiss Cottage", 1), ("Baker Street", 2)]}
        next_stops["St. Paul's"] = {"central": [("Bank", 2), ("Chancery Lane", 2)]}
        next_stops["Stamford Brook"] = {"district": [("Turnham Green", 1), ("Ravenscourt Park", 1)]}
        next_stops["Stanmore"] = {"jubilee": [("End", 0), ("Canons Park", 2)]}
        next_stops["Stepney Green"] = {"district": [("Whitechapel", 2), ("Mile End", 2)], "hammersmith-city": [("Whitechapel", 2), ("Mile End", 2)]}
        next_stops["Stockwell"] = {"northern": [("Oval", 2), ("Clapham North", 1)] , "victoria": [("Vauxhall", 2), ("Brixton", 1)]}
        next_stops["Stonebridge Park"] = {"bakerloo": [("Wembley Central", 2), ("Harlesden", 2)], "lioness": [("Wembley Central", 2), ("Harlesden", 2)]}
        next_stops["Stratford"] = {"central": [("Leyton", 2), ("Mile End", 3)], "jubilee": [("West Ham", 2), ("End", 0)]}
        next_stops["Sudbury Hill"] = {"piccadilly": [("South Harrow", 2), ("Sudbury Town", 2)]}
        next_stops["Sudbury Town"] = {"piccadilly": [("Sudbury Hill", 2), ("Alperton", 2)]}
        next_stops["Swiss Cottage"] = {"jubilee": [("Finchley Road", 1), ("St. John's Wood", 1)]}
        next_stops["Temple"] = {"circle": [("Embankment", 1), ("Blackfriars", 1)], "district": [("Embankment", 1), ("Blackfriars", 1)]}
        next_stops["Theydon Bois"] = {"central": [("Epping", 2), ("Debden", 3)]}
        next_stops["Tooting Bec"] = {"northern": [("Balham", 1), ("Tooting Broadway", 2)]}
        next_stops["Tooting Broadway"] = {"northern": [("Tooting Bec", 1), ("Colliers Wood", 2)]}
        next_stops["Tottenham Court Road"] = {"central": [("Holborn", 2), ("Oxford Circus", 1)], "northern": [("Goodge Street", 1), ("Leicester Square", 1)]}
        next_stops["Tottenham Hale"] = {"victoria": [("Blackhorse Road", 1), ("Seven Sisters", 2)]}
        next_stops["Totteridge & Whetstone"] = {"northern": [("High Barnet", 3), ("Woodside Park", 2)]}
        next_stops["Tower Hill"] = {"circle": [("Monument", 1), ("Aldgate", 2)], "district": [("Monument", 1), ("Aldgate East", 2)]}
        next_stops["Tufnell Park"] = {"northern": [("Archway", 1), ("Kentish Town", 1)]}
        next_stops["Turnham Green"] = {"district": [("Chiswick Park", 1), ("Stamford Brook", 1), ("Gunnersbury", 3)], "piccadilly": [("Acton Town", 3), ("Hammersmith (Dist&Picc Line)", 5)]}
        next_stops["Turnpike Lane"] = {"piccadilly": [("Manor House", 3), ("Wood Green", 2)]}
        next_stops["Upminster"] = {"district": [("Upminster Bridge", 2), ("End", 0)], "c2c": [("End", 0), ("Barking", 8)]}
        next_stops["Upminster Bridge"] = {"district": [("Hornchurch", 2), ("Upminster", 2)]}
        next_stops["Upney"] = {"district": [("Barking", 2), ("Becontree", 2)]}
        next_stops["Upton Park"] = {"district": [("Plaistow", 2), ("East Ham", 2)], "hammersmith-city": [("Plaistow", 2), ("East Ham", 2)]}
        next_stops["Uxbridge"] = {"metropolitan": [("End", 0), ("Hillingdon", 2)], "piccadilly": [("End", 0), ("Hillingdon", 2)]}
        next_stops["Vauxhall"] = {"victoria": [("Pimlico", 1), ("Stockwell", 2)], "bus": [("Battersea Power Station", 8)]}
        next_stops["Victoria"] = {"district": [("Sloane Square", 2), ("St. James's Park", 1)], "circle": [("Sloane Square", 2), ("St. James's Park", 1)], "victoria": [("Green Park", 1), ("Pimlico", 1)]}
        next_stops["Walthamstow Central"] = {"victoria": [("End", 0), ("Blackhorse Road", 2)], "suffragette": [("Leytonstone", 10), ("End", 0)], "bus": [("Leyton", 20)]}
        next_stops["Wanstead"] = {"central": [("Redbridge", 2), ("Leytonstone", 2)]}
        next_stops["Warren Street"] = {"northern": [("Euston", 1), ("Goodge Street", 1)], "victoria": [("Euston", 1), ("Oxford Circus", 1)], "foot": [("Euston Square", 2)]}
        next_stops["Warwick Avenue"] = {"bakerloo": [("Maida Vale", 1), ("Paddington", 2)]}
        next_stops["Waterloo"] = {"bakerloo": [("Embankment", 1), ("Lambeth North", 1)], "jubilee": [("Westminster", 1), ("Southwark", 1)], "northern": [("Embankment", 1), ("Kennington", 2)], "waterloo-city": [("Bank", 4), ("End", 0)]}
        next_stops["Watford"] = {"metropolitan": [("End", 0), ("Croxley", 2)]}
        next_stops["Wembley Central"] = {"bakerloo": [("North Wembley", 2), ("Stonebridge Park", 2)], "lioness": [("North Wembley", 2), ("Stonebridge Park", 2)]}
        next_stops["Wembley Park"] = {"jubilee": [("Kingsbury", 3), ("Neasden", 2)], "metropolitan": [("Preston Road", 2), ("Finchley Road", 7)]} # , ("Harrow-on-the-Hill", 5)
        next_stops["West Acton"] = {"central": [("North Acton", 3), ("Ealing Broadway", 2)], "foot": [("North Ealing", 4)]}
        next_stops["West Brompton"] = {"district": [("Fulham Broadway", 2), ("Earl's Court", 2)], "mildmay2": [("Kensington (Olympia)", 3), ("End", 0)]}
        next_stops["West Finchley"] = {"northern": [("Woodside Park", 1), ("Finchley Central", 2)]}
        next_stops["West Ham"] = {"district": [("Bromley-by-Bow", 2), ("Plaistow", 1)], "hammersmith-city": [("Bromley-by-Bow", 2), ("Plaistow", 1)], "jubilee": [("Canning Town", 2), ("Stratford", 3)], "c2c": [("Barking", 5), ("End", 0)]}
        next_stops["West Hampstead"] = {"jubilee": [("Kilburn", 1), ("Finchley Road", 1)]}
        next_stops["West Harrow"] = {"metropolitan": [("Rayners Lane", 2), ("Harrow-on-the-Hill", 2)]}
        next_stops["West Kensington"] = {"district": [("Barons Court", 1), ("Earl's Court", 2)], "foot": [("Kensington (Olympia)", 6)]}
        next_stops["West Ruislip"] = {"central": [("Ruislip Gardens", 2), ("End", 0)], "foot": [("Ickenham", 6)]}
        next_stops["Westbourne Park"] = {"circle": [("Ladbroke Grove", 1), ("Royal Oak", 2)], "hammersmith-city": [("Ladbroke Grove", 1), ("Royal Oak", 2)]}
        next_stops["Westminster"] = {"circle": [("St. James's Park", 1), ("Embankment", 1)], "district": [("St. James's Park", 1), ("Embankment", 1)], "jubilee": [("Green Park", 2), ("Waterloo", 1)]}
        next_stops["White City"] = {"central": [("Shepherd's Bush (Central)", 2), ("East Acton", 2)], "foot": [("Wood Lane", 1)]}
        next_stops["Whitechapel"] = {"district": [("Aldgate East", 2), ("Stepney Green", 2)], "hammersmith-city": [("Aldgate East", 2), ("Stepney Green", 2)]}
        next_stops["Willesden Green"] = {"jubilee": [("Dollis Hill", 1), ("Kilburn", 1)]}
        next_stops["Willesden Junction"] = {"bakerloo": [("Harlesden", 2), ("Kensal Green", 2)], "lioness": [("Harlesden", 2), ("Kensal Green", 2)]}
        next_stops["Wimbledon"] = {"district": [("End", 0), ("Wimbledon Park", 2)], "tram": [("Morden", 8)], "bus": [("South Wimbledon", 11)]}
        next_stops["Wimbledon Park"] = {"district": [("Wimbledon", 3), ("Southfields", 2)]}
        next_stops["Wood Green"] = {"piccadilly": [("Turnpike Lane", 1), ("Bounds Green", 2)]}
        next_stops["Wood Lane"] = {"circle": [("Shepherd's Bush Market", 1), ("Latimer Road", 1)], "hammersmith-city": [("Shepherd's Bush Market", 1), ("Latimer Road", 1)], "foot": [("White City", 1)]}
        next_stops["Woodford"] = {"central": [("Buckhurst Hill", 2), ("South Woodford", 2), ("fill", 0), ("Roding Valley", 2)]}
        next_stops["Woodside Park"] = {"northern": [("Totteridge & Whetstone", 2), ("West Finchley", 1)]}
    except Exception as e:
        print(e)

    _next_stops = dict(next_stops).copy()

    # lines.append("foot")
    # lines.append("lioness")
    # lines.append("mildmay1")
    # lines.append("mildmay2")
    # lines.append("suffragette")
    # lines.append("tram")
    # lines.append("c2c")
    # lines.append("chiltern")
    # lines.append("bus")

    # for key in _next_stops:
    #     next_stops[key] = {}
    #     for line in lines:
    #         try:
    #             next_line_stops = _next_stops[key][line]
    #             next_stops[key][line] = next_line_stops
    #         except:
    #             (next_stops.pop(key, None) if next_stops[key] == {} else None) if line == lines[-1] else None

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
