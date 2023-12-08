a = {'start_pos':(1,2,3), 'goal_pos':(5,5,5)}

b = a.copy()
start_pos_new = a['goal_pos']
goal_pos_new = a['start_pos']

b['start_pos'] = start_pos_new
b['goal_pos'] = goal_pos_new

print(a)
print(b)