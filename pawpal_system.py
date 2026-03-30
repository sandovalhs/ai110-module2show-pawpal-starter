from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
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
    frequency: str = None      # "daily", "weekly", or None
    due_date: date = None      # next occurrence date; None = no due date
    scheduled_time: str = None # "HH:MM" 24-hour start time; None = untimed

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def __str__(self):
        """Return a formatted one-line summary of the task."""
        pet_label = f" [{self.pet}]" if self.pet else ""
        status = "✓" if self.completed else "○"
        due_label = f" (due {self.due_date})" if self.due_date else ""
        freq_label = f" [{self.frequency}]" if self.frequency else ""
        return f"{status} {self.name}{pet_label}{due_label}{freq_label} | {self.priority.name} | {self.duration} min"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.ordered_tasks: list[Task] = []

    def generate_schedule(self):
        """Sort incomplete tasks by priority then shortest duration."""
        incomplete = [t for t in self.owner.tasks if not t.completed]
        self.ordered_tasks = sorted(incomplete, key=lambda t: (t.priority.value, t.duration))

    def mark_task_complete(self, task: Task):
        """Mark a task complete and schedule its next occurrence if it recurs.

        For tasks with a frequency of "daily" or "weekly", a new Task is created
        with the same name, duration, priority, pet, and frequency, and its due_date
        set to due_date + 1 day (daily) or + 7 days (weekly). The new task is added
        directly to owner.tasks. Non-recurring tasks (frequency=None) are simply
        marked done with no follow-up created.
        """
        task.mark_complete()
        if task.frequency is None:
            return
        delta = timedelta(days=1) if task.frequency == "daily" else timedelta(weeks=1)
        next_due = (task.due_date or date.today()) + delta
        next_task = Task(
            name=task.name,
            duration=task.duration,
            priority=task.priority,
            pet=task.pet,
            frequency=task.frequency,
            due_date=next_due,
        )
        self.owner.add_task(next_task)

    def detect_conflicts(self) -> list[str]:
        """Check every pair of timed tasks in ordered_tasks for overlapping time windows.

        Two tasks conflict when one starts before the other finishes. Tasks that are
        back-to-back (one ends exactly when the next begins) are not considered conflicts.
        Tasks without a scheduled_time are ignored entirely.

        Returns a list of warning strings — one per conflicting pair found. Returns an
        empty list if there are no conflicts or no timed tasks.

        Note: generate_schedule() must be called before detect_conflicts() so that
        ordered_tasks is populated.
        """
        def to_minutes(time_str: str) -> int:
            h, m = time_str.split(":")
            return int(h) * 60 + int(m)

        def overlaps(a: Task, b: Task) -> bool:
            start_a, end_a = to_minutes(a.scheduled_time), to_minutes(a.scheduled_time) + a.duration
            start_b, end_b = to_minutes(b.scheduled_time), to_minutes(b.scheduled_time) + b.duration
            return start_a < end_b and start_b < end_a

        def conflict_message(a: Task, b: Task) -> str:
            pet_a = str(a.pet) if a.pet else "unassigned"
            pet_b = str(b.pet) if b.pet else "unassigned"
            return (
                f"WARNING: '{a.name}' ({pet_a}, {a.scheduled_time}, {a.duration} min) "
                f"conflicts with '{b.name}' ({pet_b}, {b.scheduled_time}, {b.duration} min)"
            )

        timed = [t for t in self.ordered_tasks if t.scheduled_time]
        return [
            conflict_message(timed[i], timed[j])
            for i in range(len(timed))
            for j in range(i + 1, len(timed))
            if overlaps(timed[i], timed[j])
        ]

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> list:
        """Return a filtered subset of owner.tasks based on completion status and/or pet name.

        Both parameters are optional and can be combined. Reads from owner.tasks directly,
        so it includes all tasks regardless of whether generate_schedule() has been called.

        Args:
            completed: True returns only completed tasks, False returns only incomplete
                       tasks, None (default) returns all tasks regardless of status.
            pet_name:  Name string of a pet to filter by (e.g. "Buddy"). Only tasks
                       assigned to a pet with that exact name are returned. None (default)
                       includes tasks for all pets.

        Returns:
            A new list of Task objects matching all supplied filters.
        """
        result = self.owner.tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            result = [t for t in result if t.pet and t.pet.pet_name == pet_name]
        return result

    def sort_by_time(self):
        """Re-sort ordered_tasks by duration, shortest task first.

        Operates on the existing ordered_tasks list produced by generate_schedule(),
        replacing priority-based ordering with a pure duration-based ordering. Useful
        for owners who want to knock out quick tasks first regardless of priority.
        """
        self.ordered_tasks = sorted(self.ordered_tasks, key=lambda t: t.duration)

    def display_schedule(self):
        """Print the ordered schedule to the terminal."""
        if not self.ordered_tasks:
            print("No tasks scheduled.")
            return
        for i, task in enumerate(self.ordered_tasks, start=1):
            print(f"{i}. {task}")
