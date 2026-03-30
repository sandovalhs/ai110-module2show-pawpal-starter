from pawpal_system import Owner, Task, Priority, Scheduler

# Create owner and pets
hugo = Owner("Hugo")
hugo.add_pet("Buddy", "Dog")
hugo.add_pet("Mochi", "Cat")

buddy = hugo.pets[0]
mochi = hugo.pets[1]

# Add tasks intentionally out of order (low priority first, long durations first)
hugo.add_task(Task(name="Brush Mochi",      duration=5,  priority=Priority.LOW,    pet=mochi))
hugo.add_task(Task(name="Walk Buddy",       duration=30, priority=Priority.HIGH,   pet=buddy,  scheduled_time="08:00"))
hugo.add_task(Task(name="Clean litter box", duration=15, priority=Priority.MEDIUM, pet=mochi))
hugo.add_task(Task(name="Feed Buddy",       duration=10, priority=Priority.HIGH,   pet=buddy,  scheduled_time="08:15"))  # overlaps Walk Buddy
hugo.add_task(Task(name="Vet checkup",      duration=60, priority=Priority.HIGH,   pet=buddy,  completed=True))

scheduler = Scheduler(hugo)

# --- Default schedule (priority + duration) ---
scheduler.generate_schedule()
print("=== Today's Schedule (priority + duration) ===")
scheduler.display_schedule()

# --- Sorted by duration (shortest first) ---
scheduler.sort_by_time()
print("\n=== Sorted by Duration ===")
scheduler.display_schedule()

# --- Filter: incomplete tasks only ---
incomplete = scheduler.filter_tasks(completed=False)
print("\n=== Incomplete Tasks ===")
for t in incomplete:
    print(f"  {t}")

# --- Filter: completed tasks only ---
done = scheduler.filter_tasks(completed=True)
print("\n=== Completed Tasks ===")
for t in done:
    print(f"  {t}")

# --- Filter: Buddy's tasks only ---
buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
print("\n=== Buddy's Tasks ===")
for t in buddy_tasks:
    print(f"  {t}")

# --- Conflict detection ---
print("\n=== Conflict Detection ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts found.")

# --- Filter: Mochi's incomplete tasks ---
mochi_incomplete = scheduler.filter_tasks(completed=False, pet_name="Mochi")
print("\n=== Mochi's Incomplete Tasks ===")
for t in mochi_incomplete:
    print(f"  {t}")
