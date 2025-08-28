# weight-tracker

## Planning
Frontend: React, Next.js, Typescript

Backend: Python, Flask, SQLite

## Deliverables:
- Log current day's weight
- View their recent weight history—at least the last 30 entries.
- Gain quick insights:
    - starting weight
    - current weight
    - goal weight
    - total weight change
    - average daily change
    - an estimated timeline to reach their goal based on current progress

## Data Model:
### Weight table
    weight: id (PK), user_id INT (FK), weight REAL (in pounds), date TEXT

`POST weight`: {user_id : INT, weight: REAL}, returns success

`GET weight`: {user_id: INT, amount: INT}, returns (amount) weights of the user (Add sort by date later)

### User table
    user: id (PK), username TEXT, goal_weight REAL, current_weight REAL 

No get or post planned for now! Can maybe add user login and validation later if there's time?

### Insights table
    insights: starting_weight, current_weight, goal_weight, 

`GET insights`: {user_id: INT}, returns insights in the form outlined below

#### Insights response format
`{starting_weight : REAL, current_weight : REAL, goal_weight : REAL, total_weight_change : REAL, average_daily_change: REAL, days_till_goal : INT}`




## Time Used:
