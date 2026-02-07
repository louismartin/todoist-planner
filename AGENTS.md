The goal of this project is to help me better tackle my daily tasks and projects.
I like the GTD framework and I use todoist a lot.
My main issue is that I will add a ton of tasks on todoist, but then I end up having too many tasks and it feels daunting to open my todoist app and tackle them, so I just end up ignoring them and they keep piling up.
I would like to create an AI agent that will help me get more regular with tackling my task by being proactive and arranging my tasks in a way that is more actionnable and less daunting.

# Current organization of my todoist
## Projects:
* #Boîte de réception: where quickly added task end up before being triaged
* #Personal: all my personal tasks
* #Mistral: all my work tasks
* #GluGlu: all my tasks related to my couple

## Filters:
In order to better manage my tasks, I use filters and display tasks as a calendar view to see what tasks. All tasks should have a due date.
I usually will open a filter (e.g. personal, work, or mixed), look at tasks that have no due date are not in a project yet, then tackle the ones that are overdue and that are for today (the ones for the future days I just check for visibility but I don't tackle).
* "1. Today": Mix of all tasks for today (e.g. during a workday when I am happy to mix work and personal tasks)`(no due date | overdue | Today | date before: 7 days) & !(@ignore & /Reading List | /Archived Reading List | /Someday Maybe | /Research Ideas | /Reference | @project | /Research Ideas LLMs Safety | /Investissement | /Someday Maybe | /Impots | /Watchlist | @no_due_date | @delegate | /Marengo Meubles | /Reading List)`
* "2. Today - Mistral": All my work tasks (e.g. during a workday to focus on work tasks) `(no due date | overdue | Today | date before: 7 days) & (#mistral  | #Boîte de réception) & !(@ignore | /Someday Maybe | /Reading List | @delegate | /delegate)`
* "Today - Personal": All my personal tasks (e.g. during the weekend to focus on personal tasks) `(no due date | overdue | Today | date before: 7 days) & (#Boîte de réception | #Personal | #GluGlu) & !(@ignore & /Reading List | /Archived Reading List | /Someday Maybe | /Research Ideas | /Reference | @project | /Research Ideas LLMs Safety | /Investissement | /Someday Maybe | /Impots | /Watchlist | @no_due_date | @delegate | /Marengo Meubles)`


Things that the agent could do:
* Make a pass my filters based on the current day of the week (e.g. workday vs. weekend) and try to identify the 2-3 most important tasks to be tackled for the day.
* Send me an email every morning to tell me the tasks I need to tackle for the day.
* Help me triage my tasks by asking me questions to better understand the context of the task and help me make a decision on what to do with it (e.g. when is it due, what's the impact, what's the urgency, is it actionnable enough, should it be split into multiple tasks)
* Identify tasks that seem important but that keep being postponed
* Be an interactive way to access my tasks: e.g. "Give me an easy win task", "Give me a big ambitious task", "What is the thing I could do for the week that would have the biggest impact?". And then the agent could propose tasks, and I can give feedback like "Nah this isn't an easy win because X" or "This task is blocked by Y / until date Z", and then the agent could stored this new information in the task description and potentially postpone it and propose something else.
* The agent should also try to regularly store general information on me and my tasks to get better over time at making informed decisions.


# Misc
Here are some tips I found on reddit:
Every morning I spend 30 minutes planning my day. This is sacred time. I process any inbox things that have appeared overnight (tho, if there were a ton of these, it would encroach too much on the planning time and I would not include it in the 30 minutes).

I use Omnifocus for GTD. So I basically QUICKLY review my list of 10-20 active work projects, and make a decision that morning about what to work on that day. If there's something I know I need to work on but I'm avoiding it, I ask myself why and answer out loud. Sometimes it's self-critical thinking (e.g., "Whatever I come up with won't be right") but also it's often a poorly defined, too-nebulous next action. So in the 30 mins I get small/detailed/clear enough on the true next action, and that helps me break down barriers to getting started.

I pick 3 things from the list that I'll work on that day. I write on a piece of paper that Success today = those three things, and I list them out. Anything else I accomplish (including emergency firefighting my time gets rerouted to against my will or better judgment) is a bonus! 🎉

I have a "Shutdown/Reset" ritual at the end of each workday:


* Zero out my inboxes
* Quickly mind-sweep and put stuff into my GTD inbox, triage it if it's easy to do so
* Look ahead at the calendar for the next day and make a little timeline of my commitments, in my notebook


Do a journal entry where I list three wins from the day; three things that were challenging; and three things I learned.

Then I literally say, out loud, "Shutdown complete!" and close out all my apps and my notebook. That puts a physical ending point to the work day and I then put my attention on family stuff in the evening. (Can't remember if it was Cal Newport or James Clear that gave me that idea. It's corny but it works.)

This whole thing takes about 30 minutes. It's on my calendar every day so I can't forget about it. At some point in the past I just started setting calendar reminders and clearing out that time at the end of the day, and made an appointment with myself to do it, and tracked it. After a couple of months it was an ingrained habit. Now if I don't do this, I am really out of sorts for the rest of the evening.