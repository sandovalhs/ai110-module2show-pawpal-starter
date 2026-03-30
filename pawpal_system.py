from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Owner:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def edit_owner_name(self, new_name: str):
        """Update the owner's name."""
        self.owner_name = new_name

    def add_pet(self, name: str, species: str):
        """Create a new Pet and add it to the owner's pet list."""
        self.pets.append(Pet(pet_name=name, species=species))

    def remove_pet(self, pet: Pet):
        """Remove an existing Pet from the owner's pet list."""
        self.pets.remove(pet)

    def add_task(self, task: Task):
        """Add a Task to the owner's task list."""
        self.tasks.append(task)

    def edit_task(self, task: Task, name: str = None, duration: int = None, priority: Priority = None):
        """Update one or more fields on an existing Task."""
        if name is not None:
            task.name = name
        if duration is not None:
            task.duration = duration
        if priority is not None:
            task.priority = priority


@dataclass
class Pet:
    pet_name: str
    species: str

    def __str__(self):
        """Return a readable name and species label."""
        return f"{self.pet_name} ({self.species})"


@dataclass
class Task:
    name: str
    duration: int              # minutes
    priority: Priority
    pet: Pet = None
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def __str__(self):
        """Return a formatted one-line summary of the task."""
        pet_label = f" [{self.pet}]" if self.pet else ""
        status = "✓" if self.completed else "○"
        return f"{status} {self.name}{pet_label} | {self.priority.name} | {self.duration} min"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.ordered_tasks: list[Task] = []

    def generate_schedule(self):
        """Sort incomplete tasks by priority then shortest duration."""
        incomplete = [t for t in self.owner.tasks if not t.completed]
        self.ordered_tasks = sorted(incomplete, key=lambda t: (t.priority.value, t.duration))

    def display_schedule(self):
        """Print the ordered schedule to the terminal."""
        if not self.ordered_tasks:
            print("No tasks scheduled.")
            return
        for i, task in enumerate(self.ordered_tasks, start=1):
            print(f"{i}. {task}")
