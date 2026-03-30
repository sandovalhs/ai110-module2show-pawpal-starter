from pawpal_system import Owner, Task, Priority, Scheduler

# Create owner and pets
hugo = Owner("Hugo")
hugo.add_pet("Buddy", "Dog")
hugo.add_pet("Mochi", "Cat")

buddy = hugo.pets[0]
mochi = hugo.pets[1]

# Add tasks with different priorities and durations
hugo.add_task(Task(name="Feed Buddy",       duration=10, priority=Priority.HIGH,   pet=buddy))
hugo.add_task(Task(name="Clean litter box", duration=15, priority=Priority.MEDIUM, pet=mochi))
hugo.add_task(Task(name="Walk Buddy",       duration=30, priority=Priority.HIGH,   pet=buddy))
hugo.add_task(Task(name="Brush Mochi",      duration=5,  priority=Priority.LOW,    pet=mochi))

# Generate and display schedule
scheduler = Scheduler(hugo)
scheduler.generate_schedule()

print("=== Today's Schedule ===")
scheduler.display_schedule()
