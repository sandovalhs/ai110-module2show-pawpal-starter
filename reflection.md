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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
