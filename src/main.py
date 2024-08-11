from collections import defaultdict
from datetime import timedelta
from typing import List


class City:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Road:

    def __init__(self, id: int, name: str, from_: int, to: int, through: List[int], speed_limit: int, length: int,
                 bi_directional: int):
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


city_storage = dict()
road_storage = dict()
city_roads = defaultdict(list)


def add_city() -> int:
    id_inp = int(input("id=?\n"))
    name_inp = input("name=?\n")
    city = City(id=id_inp, name=name_inp)
    city_storage[id_inp] = city
    return id_inp


def add_road() -> int:
    id_inp = int(input("id=?\n"))
    name_inp = input("name=?\n")
    from_inp = int(input("from=?\n"))
    to_inp = int(input("to=?\n"))
    th_cities = {from_inp}
    through_inp = input("through=?\n")[1:-1].strip().split(",")
    if len(through_inp) > 1:
        for city_id in through_inp:
            th_cities.add(int(city_id))
    th_cities.add(to_inp)
    speed_limit = int(input("speed_limit=?\n"))
    length = int(input("length=?\n"))
    bi_directional = int(input("bi_directional=?\n"))

    road = Road(id=id_inp, name=name_inp, from_=from_inp, to=to_inp, through=list(th_cities), speed_limit=speed_limit,
                length=length, bi_directional=bi_directional)

    road_storage[id_inp] = road
    for city in road.through:
        city_roads[city].append(road)

    return id_inp


def run_add(command: int):
    if command == 1:
        id = add_city()
        model = "City"
    else:
        id = add_road()
        model = "Road"
    output_text = "%s with id=%d added!\nSelect your next action\n1. Add another %s\n2. Main Menu\n" % (
        model, id, model)
    new_command = int(input(output_text))
    if new_command == 1:
        run_add(command=command)


def delete_city():
    id_inp = int(input())
    if id_inp in city_storage:
        ss = list(road_storage.keys())
        for road_id in ss:
            road = road_storage[road_id]
            for city in road.through:
                if city == id_inp:
                    del_road(road_id)
                    break

        del city_roads[id_inp]
        del city_storage[id_inp]
    else:
        raise Exception("City with id %d not found!" % id_inp)
    return id_inp


def del_road(id_inp):
    if id_inp in road_storage.keys():
        road = road_storage[id_inp]
        del road_storage[id_inp]
        for city in road.through:
            city_roads[city].remove(road)
    else:
        raise Exception("Road with id %d not found!" % id_inp)

    return id_inp


def delete_road():
    id_inp = int(input())
    return del_road(id_inp)


def run_delete(command: int):
    try:
        if command == 1:
            id = delete_city()
            model = "City"
        else:
            id = delete_road()
            model = "Road"
        print("%s:%d deleted!" % (model, id))
    except Exception as e:
        print(e)


def find_roads(origin: int, dest: int) -> List[Road]:
    origin_roads = city_roads[origin]
    dest_roads = city_roads[dest]

    common_roads = set(origin_roads).intersection(dest_roads)
    final_roads = set()
    initial = -1
    finish = -1
    for road in common_roads:
        for city in road.through:
            if city == -1:
                break
            if city == origin:
                initial = origin
                if finish != -1 and road.bi_directional == 1:
                    final_roads.add(road)
                    break
            elif city == dest:
                if initial != -1:
                    final_roads.add(road)
                    break

    return list(final_roads)


def format_time(spent_time):
    deltas = timedelta(hours=spent_time)
    days = deltas.days
    hours, remainder = divmod(deltas.seconds, 3600)
    minutes = remainder // 60
    return f"{days:02}:{hours:02}:{minutes:02}"


def run_path(origin: int, dest: int):
    roads = find_roads(origin, dest)
    roads = sorted(roads, reverse=False)
    for road in roads:
        print("%s:%s via Road %s: Takes %s"
              % (city_storage[origin].name, city_storage[dest].name, road.name, format_time(road.spent_time)))


while True:
    command_inp = input('Main Menu - Select an action:\n1. Help\n2. Add\n3. Delete\n4. Path\n5. Exit\n')

    if command_inp == "1":
        print("Select a number from shown menu and enter. For example 1 is for help.")
    elif command_inp == "2":
        command = int(input("Select model:\n1. City\n2. Road\n"))
        run_add(command)
    elif command_inp == "3":
        command = int(input("Select model:\n1. City\n2. Road\n"))
        run_delete(command)
    elif command_inp == "4":
        cities = input().split(":")
        run_path(int(cities[0]), int(cities[1]))
    elif command_inp == "5":
        break
    else:
        print("Invalid input. Please enter 1 for more info.")
