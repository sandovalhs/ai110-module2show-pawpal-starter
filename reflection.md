# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Users should be able to enter basic owner + pet info, add/edit tasks (duration + priority at minimum) and Generate a daily schedule/plan based on constraints and priorities

What information it needs to hold (attributes)
User class
- owner name

Pet Class
- pet name and species

task class
- name of task
- duration
- priority (high, medium, low)

daily schedule class
- ordered list based on priority first then lowest duration

What actions it can perform (methods)
User class
-edit owner name

Pet class
-add/remove pet (includes name and species)

task class
- mark task as complete
- add/edit task

daily schedule class
-generate schedule
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

yes, the ai suggested i move methods that add/edit a pet into the user and i agreed.  it also suggested that users should have a list of pets and tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
my scheduler considers duration and priority, so tasked marked as higher priority are more important and shorter duration is prioritized to be completed first.
- How did you decide which constraints mattered most?

I figured completing as many tasks as possible is better than completing longer tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Shortest-duration tiebreaker (within the same priority) is a greedy heuristic. It minimizes the number of tasks left unfinished if you run out of time, but it ignores whether a longer task has a hard deadline that shorter ones don't.



---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used ai for everything, but i verfied its outputs

- What kinds of prompts or questions were most helpful?

the prompts where i asked about functionality really helped me learn

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

the ai tried to make me track timestamps and time of day instead of keeping my duration functionality so i stopped it

- How did you evaluate or verify what the AI suggested?

Before i accepted the output i noticed it was importing a library that i didnt want so i checked what it was doing and stopped it from changing my system design.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

generate_schedule sorts correctly — incomplete tasks ordered by priority first, then shortest duration. Verify that a HIGH-priority 30-min task ranks before a MEDIUM-priority 10-min task, and that completed tasks are excluded.

mark_task_complete recurrence logic — completing a daily task should add a new task with due_date + 1 day; weekly adds + 7 days; non-recurring tasks should produce no follow-up.

detect_conflicts overlap detection — two timed tasks whose windows overlap should produce a warning; back-to-back tasks (one ends exactly when the next begins) should not. Tasks without scheduled_time must be ignored.

filter_tasks combined filtering — passing both completed=False and pet_name="Buddy" should return only incomplete tasks assigned to that pet. Each filter should work independently too.

Owner.edit_task partial update — calling with only name= should change the name but leave duration and priority unchanged; passing None for a field must be a no-op (not overwrite with None).

- Why were these tests important?

these tests focus on the core functionality of the app.
if they fail, the app would be pretty broken

**b. Confidence**

- How confident are you that your scheduler works correctly?

I think it is mostly correct

- What edge cases would you test next if you had more time?

Recurring task with due_date=None (falls back to date.today())
The double-complete bug (completing a recurring task twice silently adds a duplicate follow-up)

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I like how quickly I was able to make an app from nothing

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I think I want to make the ui a bit nicer and make it more interactive

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned ai is quick, but overly trusting it to make decisions is risky and it will frequently try to go above and beyond what you want to do.
