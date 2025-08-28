from typing import List, Dict
from datetime import datetime

def calculate_insights(weights_dicts: Dict, goal_weight: float) -> Dict:
    '''
    goal_weight: the user's goal weight
    weights: a list of dicts [{'weight' : REAL, 'entry_date': TEXT}] 
             from a user sorted by enty_date descending

    returns an insights response dictionary outlined in the README
    '''
    
    if len(weights_dicts) < 2:
        return {}
    
    ## Perform calculations
    # Get weights out into a list
    weights = []
    date_entries = []
    for weights_dict in weights_dicts:
        weights.append(weights_dict['weight'])
        date_entries.append(weights_dict['entry_date'])

    initial_weight = weights[-1]
    most_recent_weight = weights[0]
    initial_date = date_entries[-1]
    most_recent_date = date_entries[0]

    total_weight_change = most_recent_weight - initial_weight
    days_tracked = (datetime.fromisoformat(initial_date) - 
                    datetime.fromisoformat(most_recent_date)).days
    
    # Could maybe think of better defaults here?
    average_daily_change = 0
    if days_tracked != 0:
        total_weight_change / days_tracked
    
    # Maybe add linear regression model here?
    projected_days_to_goal = 0

    # First make sure that we haven't already reached the goal!
    if (goal_weight - most_recent_weight) < 0:
        projected_days_to_goal = 0
    elif average_daily_change != 0:
        projected_days_to_goal = (goal_weight - most_recent_weight) / average_daily_change
        
    return {
        'starting_weight': initial_weight,
        'current_weight': most_recent_weight,
        'goal_weight': goal_weight,
        'total_weight_change': total_weight_change,
        'average_daily_change': average_daily_change,
        'projected_days_to_goal': projected_days_to_goal
    }