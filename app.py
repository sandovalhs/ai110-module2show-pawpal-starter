import streamlit as st
from pawpal_system import Owner, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# Create Owner in session state if it doesn't already exist
if st.button("Create Owner"):
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(owner_name)
        st.success(f"Owner '{owner_name}' created!")
    else:
        st.info(f"Owner already exists: {st.session_state.owner.owner_name}")

# Add a Pet — calls owner.add_pet() from Phase 2
st.markdown("### Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Add Pet"):
    if "owner" not in st.session_state:
        st.warning("Create an owner first.")
    else:
        st.session_state.owner.add_pet(pet_name, species)
        st.success(f"Added {pet_name} the {species}!")

if "owner" in st.session_state and st.session_state.owner.pets:
    st.write("Pets:", ", ".join(str(p) for p in st.session_state.owner.pets))

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"])

# Pet selector — shown only if the owner has pets added
task_pet = None
if "owner" in st.session_state and st.session_state.owner.pets:
    pet_options = {str(p): p for p in st.session_state.owner.pets}
    selected = st.selectbox("Assign to pet", list(pet_options.keys()))
    task_pet = pet_options[selected]

# Add task — calls owner.add_task() with a real Task object from Phase 2
if st.button("Add task"):
    if "owner" not in st.session_state:
        st.warning("Create an owner first.")
    else:
        task = Task(
            name=task_title,
            duration=int(duration),
            priority=Priority[priority],
            pet=task_pet,
        )
        st.session_state.owner.add_task(task)
        st.success(f"Task '{task_title}' added!")

if "owner" in st.session_state and st.session_state.owner.tasks:
    st.write("Current tasks:")
    st.table([
        {"Task": t.name, "Pet": str(t.pet) if t.pet else "—", "Priority": t.priority.name, "Duration (min)": t.duration}
        for t in st.session_state.owner.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button calls your scheduling logic from Phase 2.")

sort_mode = st.radio(
    "Sort order",
    ["By priority (default)", "Quickest first"],
    horizontal=True,
)

# Generate schedule — calls Scheduler.generate_schedule() from Phase 2
if st.button("Generate schedule"):
    if "owner" not in st.session_state or not st.session_state.owner.tasks:
        st.warning("Add an owner and at least one task first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        scheduler.generate_schedule()

        if sort_mode == "Quickest first":
            scheduler.sort_by_time()

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)

        if scheduler.ordered_tasks:
            st.success(f"Today's Schedule — {len(scheduler.ordered_tasks)} task(s)")
            st.table([
                {
                    "#": i,
                    "Task": t.name,
                    "Pet": str(t.pet) if t.pet else "—",
                    "Priority": t.priority.name,
                    "Duration (min)": t.duration,
                    "Time": t.scheduled_time or "—",
                    "Status": "✓ Done" if t.completed else "Pending",
                }
                for i, t in enumerate(scheduler.ordered_tasks, start=1)
            ])
        else:
            st.info("No incomplete tasks to schedule.")
