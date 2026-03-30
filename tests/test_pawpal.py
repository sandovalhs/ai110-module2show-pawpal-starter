import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Owner, Task, Priority


def test_mark_complete_changes_status():
    task = Task(name="Walk Buddy", duration=30, priority=Priority.HIGH)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_owner_task_count():
    owner = Owner("Hugo")
    owner.add_pet("Buddy", "Dog")
    buddy = owner.pets[0]

    task = Task(name="Feed Buddy", duration=10, priority=Priority.HIGH, pet=buddy)
    owner.add_task(task)

    pet_tasks = [t for t in owner.tasks if t.pet == buddy]
    assert len(pet_tasks) == 1
