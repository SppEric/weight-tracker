from typing import List, Dict
from datetime import date

def calculate_insights(weights: Dict, goal_weight: float) -> Dict:
    '''
    goal_weight: the user's goal weight
    weights: a list of dicts [{'weight' : REAL, 'entry_date': TEXT}] 
             from a user sorted by enty_date descending

    returns an insights response dictionary outlined in the README
    '''

    if len(weights) < 2:
        return {}
    
    # Perform calculations
    initial_entry = weights[-1]
    most_recent_entry = weights[0]
    total_weight_change = most_recent_entry['weight'] - initial_entry['weight']
    days_tracked = (date.fromisoformat(most_recent_entry['entry_date']) - 
                    date.fromisoformat(initial_entry['entry_date'])).days
    
    # Could maybe think of better defaults here?
    average_daily_change = 0
    if days_tracked != 0:
        total_weight_change / days_tracked
    
    # Maybe add linear regression model here?
    projected_days_to_goal = float('inf')
    
    # First make sure that we haven't already reached the goal!
    if (goal_weight - most_recent_entry['weight']) < 0:
        projected_days_to_goal = 0
    elif average_daily_change == 0:
        projected_days_to_goal = (goal_weight - most_recent_entry['weight']) / average_daily_change
        
    return {
        'starting_weight': initial_entry['weight'],
        'current_weight': most_recent_entry['weight'],
        'goal_weight': goal_weight,
        'total_weight_change': total_weight_change,
        'average_daily_change': average_daily_change,
        'projected_days_to_goal': projected_days_to_goal
    }
