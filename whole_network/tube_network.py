class Station:

    def __init__(self, name):
        self.name = name
        self.visited = False
        self.platforms = []

    def visit(self, genome, line):
        if self.visited:
            # genome.fitness -= 1e0
            return 0
        elif line in ["foot", "tram", "bus", "great_northern", "c2c", "suffragette", "mildmay2"]:
            return 0
        else:
            # if self.name in ["Kensington (Olympia)"]:
            #     self.visited = True
            #     genome.fitness += 1e4
            #     return 1
            # else:
            #     self.visited = True
            #     genome.fitness += 1e2
            #     return 1
            self.visited = True
            genome.fitness += 1e2
            return 1

    def __repr__(self):
        return self.name
    
    def __eq__(self, other: str):
        return self.name == other
    
    @property
    def num_platforms(self):
        return len(self.platforms)

class Platform:

    def __init__(self, station, next_stop, line, direction="up", end=False):
        self.line = line
        self.station = station
        self.next_stop = next_stop
        self.time_to_next_stop = 0
        self.departure_times = []
        self.direction = direction
        self.end = end

        station.platforms.append(self)

    def __repr__(self):
        if self.line == "foot":
            return f"{self.station} to {self.next_stop} on foot"
        elif self.line in ["bus", "tram"]:
            return f"{self.station} to {self.next_stop} on the {self.line}."
        else:
            return f"{self.station} to {self.next_stop} on the {self.line.capitalize()} line"