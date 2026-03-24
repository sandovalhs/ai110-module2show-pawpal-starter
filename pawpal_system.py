from dataclasses import dataclass


class User:
    def __init__(self, owner_name):
        self.owner_name = owner_name

    def edit_owner_name(self, new_name):
        pass


@dataclass
class Pet:
    pet_name: str
    species: str

    def add_pet(self, name, species):
        pass

    def remove_pet(self):
        pass


@dataclass
class Task:
    name: str
    duration: int          # minutes
    priority: str          # "high", "medium", or "low"
    completed: bool = False

    def mark_complete(self):
        pass

    def add_task(self):
        pass

    def edit_task(self):
        pass


class DailySchedule:
    def __init__(self):
        self.ordered_tasks = []       # List of Task, sorted by priority then duration

    def generate_schedule(self):
        pass
