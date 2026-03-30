# =============================================================================
# Testing PawPal+
# =============================================================================
#
# Run all tests with:
#   python -m pytest tests/test_pawpal.py -v
#
# What these tests cover:
#   - Task lifecycle     : creating, completing, and str-formatting tasks
#   - Owner management   : adding tasks and verifying pet-task relationships
#   - Sorting correctness: generate_schedule orders by priority then duration,
#                          and excludes completed tasks entirely
#   - Recurrence logic   : daily tasks spawn a follow-up due the next day;
#                          one-off tasks produce no follow-up
#   - Conflict detection : overlapping timed tasks are flagged; back-to-back
#                          and untimed tasks are not reported as conflicts
#
# Confidence Level: ★★★★☆ (4/5)
#   Core behaviors are well-covered across happy paths and key edge cases.
#   One point held back because recurring tasks with due_date=None (falls back
#   to date.today()) and the double-complete bug are not yet tested, leaving
#   two known risk areas unverified.
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Owner, Task, Priority, Scheduler


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


# --- Sorting Correctness ---

def test_generate_schedule_sorts_by_priority_then_duration():
    """Tasks should be ordered: HIGH before MEDIUM before LOW,
    and within the same priority, shorter duration comes first."""
    owner = Owner("Hugo")
    t1 = Task(name="Groom", duration=45, priority=Priority.MEDIUM)
    t2 = Task(name="Feed", duration=10, priority=Priority.HIGH)
    t3 = Task(name="Play", duration=20, priority=Priority.MEDIUM)
    t4 = Task(name="Vet visit", duration=60, priority=Priority.LOW)
    for t in [t1, t2, t3, t4]:
        owner.add_task(t)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    names = [t.name for t in scheduler.ordered_tasks]
    assert names == ["Feed", "Play", "Groom", "Vet visit"]


def test_generate_schedule_excludes_completed_tasks():
    """Completed tasks must not appear in the generated schedule."""
    owner = Owner("Hugo")
    done = Task(name="Walk", duration=30, priority=Priority.HIGH)
    done.mark_complete()
    pending = Task(name="Feed", duration=10, priority=Priority.HIGH)
    owner.add_task(done)
    owner.add_task(pending)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    assert all(not t.completed for t in scheduler.ordered_tasks)
    assert len(scheduler.ordered_tasks) == 1


# --- Recurrence Logic ---

def test_daily_recurring_task_creates_next_day_task():
    """Completing a daily task should add a new task due the following day."""
    owner = Owner("Hugo")
    today = date.today()
    task = Task(
        name="Morning walk",
        duration=20,
        priority=Priority.HIGH,
        frequency="daily",
        due_date=today,
    )
    owner.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(owner.tasks) == 2

    next_task = owner.tasks[1]
    assert next_task.name == "Morning walk"
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_non_recurring_task_creates_no_follow_up():
    """Completing a one-off task (frequency=None) must not add a new task."""
    owner = Owner("Hugo")
    task = Task(name="Vet visit", duration=60, priority=Priority.HIGH)
    owner.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(owner.tasks) == 1


# --- Conflict Detection ---

def test_detect_conflicts_flags_overlapping_tasks():
    """Two tasks whose time windows overlap should produce a conflict warning."""
    owner = Owner("Hugo")
    t1 = Task(name="Feed", duration=30, priority=Priority.HIGH, scheduled_time="09:00")
    t2 = Task(name="Groom", duration=30, priority=Priority.MEDIUM, scheduled_time="09:15")
    owner.add_task(t1)
    owner.add_task(t2)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Feed" in conflicts[0]
    assert "Groom" in conflicts[0]


def test_detect_conflicts_ignores_back_to_back_tasks():
    """Tasks that are back-to-back (no gap, no overlap) must not conflict."""
    owner = Owner("Hugo")
    t1 = Task(name="Walk", duration=30, priority=Priority.HIGH, scheduled_time="09:00")
    t2 = Task(name="Feed", duration=15, priority=Priority.HIGH, scheduled_time="09:30")
    owner.add_task(t1)
    owner.add_task(t2)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_detect_conflicts_ignores_untimed_tasks():
    """Tasks without a scheduled_time must be skipped entirely."""
    owner = Owner("Hugo")
    t1 = Task(name="Walk", duration=30, priority=Priority.HIGH, scheduled_time="09:00")
    t2 = Task(name="Feed", duration=15, priority=Priority.HIGH)  # no scheduled_time
    owner.add_task(t1)
    owner.add_task(t2)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []
