import ast
from collections import defaultdict
from datetime import timedelta
from typing import List, Dict, DefaultDict


class City:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Road:
    def __init__(
        self,
        id: int,
        name: str,
        from_: int,
        to: int,
        through: List[int],
        speed_limit: int,
        length: int,
        bi_directional: int,
    ):
        self.id = id
        self.name = name
        self.from_ = from_
        self.to = to
        self.through = through
        self.speed_limit = speed_limit
        self.length = length
        self.bi_directional = bi_directional
        self.spent_time = self.length / self.speed_limit

    def __gt__(self, other):
        return self.spent_time > other.spent_time

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


city_storage: Dict[int, City] = {}
road_storage: Dict[int, Road] = {}
city_roads: DefaultDict[int, List[Road]] = defaultdict(list)


def add_city() -> int:
    inp_id = int(input("id=?\n"))
    name_inp = input("name=?\n")

    city = City(id=inp_id, name=name_inp)
    city_storage[inp_id] = city
    return inp_id


def add_road() -> int:
    inp_id = int(input("id=?\n"))
    name_inp = input("name=?\n")
    from_inp = int(input("from=?\n"))
    to_inp = int(input("to=?\n"))
    th_cities = {from_inp}
    through_inp = input("through=?\n")
    through_list = ast.literal_eval(through_inp)
    for city_id in through_list:
        th_cities.add(int(city_id))
    th_cities.add(to_inp)
    speed_limit = int(input("speed_limit=?\n"))
    length = int(input("length=?\n"))
    bi_directional = int(input("bi_directional=?\n"))

    road = Road(
        id=inp_id,
        name=name_inp,
        from_=from_inp,
        to=to_inp,
        through=list(th_cities),
        speed_limit=speed_limit,
        length=length,
        bi_directional=bi_directional,
    )

    if inp_id in road_storage:
        prev_road = road_storage[inp_id]
        for city in prev_road.through:
            city_roads[city].remove(prev_road)

    for city in road.through:
        city_roads[city].append(road)

    road_storage[inp_id] = road
    return inp_id


def run_add(add_command: int):
    if add_command == 1:
        id = add_city()
        output_text = "City with id=%d added!\nSelect your next action\n1. Add another City\n2. Main Menu\n" % id
    else:
        id = add_road()
        output_text = "Road with id=%d added!\nSelect your next action\n1. Add another Road\n2. Main Menu\n" % id
    new_command = int(input(output_text))
    if new_command == 1:
        run_add(add_command=add_command)


def delete_city() -> int:
    city_id = int(input())
    if city_id in city_storage:
        for road_id, road in road_storage.items():
            road.through = [-1 if city == city_id else city for city in road.through]

        del city_roads[city_id]
        del city_storage[city_id]

    else:
        raise ValueError("City with id %d not found!" % city_id)
    return city_id


def del_road(road_id: int) -> int:
    if road_id in road_storage.keys():
        road = road_storage[road_id]
        del road_storage[road_id]
        for city in road.through:
            city_roads[city].remove(road)
    else:
        raise ValueError("Road with id %d not found!" % road_id)

    return road_id


def delete_road() -> int:
    inp_id = int(input())
    return del_road(road_id=inp_id)


def run_delete(del_command: int):
    try:
        if del_command == 1:
            id = delete_city()
            print("City:%d deleted!" % id)
        else:
            id = delete_road()
            print("Road:%d deleted!" % id)

    except ValueError as e:
        print(e)


def find_roads(origin: int, dest: int) -> List[Road]:
    origin_roads = city_roads[origin]
    valid_roads = []

    for road in origin_roads:
        if dest in road.through:
            origin_index = road.through.index(origin)
            dest_index = road.through.index(dest)
            null_indices = [index for index, value in enumerate(road.through) if value == -1]

            if any(origin < index < dest or dest < index < origin for index in null_indices):
                continue

            if origin_index < dest_index or (road.bi_directional and dest_index < origin_index):
                valid_roads.append(road)
    return valid_roads


def format_time(spent_time: float) -> str:
    deltas = timedelta(hours=spent_time)
    days = deltas.days
    hours, remainder = divmod(deltas.seconds, 3600)
    minutes = remainder // 60
    return f"{days:02}:{hours:02}:{minutes:02}"


def run_path(origin: int, dest: int):
    roads = find_roads(origin=origin, dest=dest)
    roads = sorted(roads, reverse=False)
    for road in roads:
        print(
            "%s:%s via Road %s: Takes %s"
            % (city_storage[origin].name, city_storage[dest].name, road.name, format_time(spent_time=road.spent_time))
        )


while True:
    command_inp = input("Main Menu - Select an action:\n1. Help\n2. Add\n3. Delete\n4. Path\n5. Exit\n")

    if command_inp == "1":
        print("Select a number from shown menu and enter. For example 1 is for help.")
    elif command_inp == "2":
        command = int(input("Select model:\n1. City\n2. Road\n"))
        run_add(add_command=command)
    elif command_inp == "3":
        command = int(input("Select model:\n1. City\n2. Road\n"))
        run_delete(del_command=command)
    elif command_inp == "4":
        cities = input().split(":")
        run_path(origin=int(cities[0]), dest=int(cities[1]))
    elif command_inp == "5":
        break
    else:
        print("Invalid input. Please enter 1 for more info.")
