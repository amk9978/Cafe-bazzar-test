import json
import sys
from abc import ABC, abstractmethod


class City:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_user_input(cls):
        id = int(input("id=?\n"))
        name = input("name=?\n")
        return cls(id=id, name=name)


class Road:
    def __init__(
            self,
            id,
            name,
            from_,
            to,
            through,
            speed_limit,
            length,
            bi_directional,
    ):
        self.id = id
        self.name = name
        self.from_ = from_
        self.to = to
        self.through = through
        self.speed_limit = speed_limit
        self.length = length
        self.bi_directional = bi_directional
        all_cities = [self.from_]
        all_cities.extend(self.through)
        all_cities.append(self.to)
        all_cities = list(dict.fromkeys(all_cities))
        self.all_cities = all_cities

    @classmethod
    def from_user_input(cls):
        id = int(input("id=?\n"))
        name = input("name=?\n")
        from_ = int(input("from=?\n"))
        to = int(input("to=?\n"))
        through = json.loads(input("through=?\n"))
        speed_limit = int(input("speed_limit=?\n"))
        length = int(input("length=?\n"))
        bi_directional = int(input("bi_directional=?\n"))
        return cls(
            id=id,
            name=name,
            from_=from_,
            to=to,
            through=through,
            speed_limit=speed_limit,
            length=length,
            bi_directional=bi_directional,
        )


cities = {}
roads = {}


class CommandStrategy(ABC):
    @abstractmethod
    def execute(self):
        pass


class HelpStrategy(CommandStrategy):
    def execute(self):
        print("Select a number from shown menu and enter. For example 1 is for help.")


def add_city() -> City:
    city = City.from_user_input()
    cities[city.id] = city
    return city


def add_road() -> Road:
    road = Road.from_user_input()
    roads[road.id] = road
    return road


class AddStrategy(CommandStrategy):
    def execute(self):
        choice = input("Select model:\n1. City\n2. Road\n")
        obj = None
        if choice == "1":
            city = add_city()
            obj = city
        elif choice == "2":
            road = add_road()
            obj = road
        try:
            print("{} with id={} added!".format(type(obj).__name__, obj.id))
        except:
            print(id)
        while True:
            choice = input(
                "Select your next action:\n1. Add another {}\n2. Main Menu\n".format(
                    type(obj).__name__
                )
            )
            if choice == "1":
                if isinstance(obj, City):
                    add_city()
                elif isinstance(obj, Road):
                    add_road()
            else:
                break


class DeleteStrategy(CommandStrategy):
    def execute(self):
        choice_map = {"1": "City", "2": "Road"}
        choice = input("Select model:\n1. City\n2. Road\n")
        id = int(input())
        obj = None
        if choice == "1":
            obj = cities.pop(id, None)
            for road_id in list(roads.keys()):
                if id in roads[road_id].all_cities:
                    roads[road_id].all_cities.remove(id)
        elif choice == "2":
            obj = roads.pop(id, None)

        if obj is None:
            print("{} with id {} not found!".format(choice_map[choice], id))
        else:
            print("{}:{} deleted!".format(choice_map[choice], id))


def format_time(time: float) -> str:
    total_minutes = int(time * 60)
    days = total_minutes // (60 * 24)
    hours = (total_minutes // 60) % 24
    minutes = total_minutes % 60

    return f"{days:02d}:{hours:02d}:{minutes:02d}"


def path_finder(origin, dest) -> list:
    result = []
    for road_id, road in roads.items():
        if origin in road.all_cities and dest in road.all_cities:
            cnt1 = 0
            cnt2 = 0
            for index, city in enumerate(road.through):
                if city == origin:
                    cnt1 = index
                elif city == dest:
                    cnt2 = index
            if cnt2 == 0 and road.to == dest:
                cnt2 = len(road.through)
            dist = abs(cnt2 - cnt1)
            if road.bi_directional == 1:
                time = (road.length) / road.speed_limit
                result.append((road, time))
            elif cnt2 > cnt1:
                time = (road.length) / road.speed_limit
                result.append((road, time))

    return sorted(result, key=lambda entry: entry[1], reverse=True)


class PathStrategy(CommandStrategy):
    def execute(self):
        path = input()
        origin = int(path.split(":")[0])
        dest = int(path.split(":")[1])
        paths = path_finder(origin=origin, dest=dest)
        for entry in paths:
            path = entry[0]
            time = entry[1]
            formatted_time = format_time(time=time)
            print(
                "{}:{} via Road {}: Takes {}".format(
                    cities[origin].name, cities[dest].name, path.name, formatted_time
                )
            )


class ExitStrategy(CommandStrategy):
    def execute(self):
        sys.exit()


class CommandContext:
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: CommandStrategy):
        self._strategy = strategy

    def execute_command(self):
        self._strategy.execute()


def main():
    strategy_mapping = {
        "1": HelpStrategy(),
        "2": AddStrategy(),
        "3": DeleteStrategy(),
        "4": PathStrategy(),
        "5": ExitStrategy(),
    }

    context = CommandContext()
    input_template = "Main Menu - Select an action:\n1. Help\n2. Add\n3. Delete\n4. Path\n5. Exit\n"
    while True:
        choice = input(input_template)
        if choice in strategy_mapping:
            strategy = strategy_mapping[choice]
            context.strategy = strategy
            context.execute_command()
        else:
            print("Invalid input. Please enter 1 for more info.")


if __name__ == "__main__":
    main()
