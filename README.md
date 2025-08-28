# weight-tracker

## How to Run
This requires two terminals to run! For one terminal, `cd` into `/weight-tracker/backend` and for the other, `cd` into `/weight-tracker/frontend/weight-tracker`. Instructions on how to run each side will be in the respective READMEs.


## Time Breakdown:
Minutes 0-10: Planning out tech stack and approach

Minutes 10-20: Create a rough foundation for the project

Minutes 20-90: Create and validate the backend

Minutes 90-115: Create, wire, and slightly style the frontend - stopped in the middle of styling

Minutes 115-120: Polish and document

## Design Decisions:
- Support for multiple users of the application is included, but due to time constraints I chose to forgo a login page and authentication for the frontend and simply assume one user for now

- Chose to use SQLite despite it saving straight to hardware due to the time constraints. I didn't want to have to include starting up a SQL server, and SQLite closely mirrors submitting queries to a cloud server

- More time was spent on the backend than expected, and thus I didn't have enough time to spend on creating a more appealing frontend that I believe would reflect my abilities.

- While I didn't have enough time to get to adding on enhancements, if time permitted, given my background I would've liked to add a simple machine learning model to enhance the weight prediction!

---
### Planning (This was just for my benefit, no need to review further)
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
