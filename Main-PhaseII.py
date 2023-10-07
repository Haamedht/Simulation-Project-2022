"""
We want to simulate a 24/7 call-center.
There are 8 hours shifts and 3 types of servers that serve normal and VIP types of users:
   . Expert server (2)
   . Rookie server (3)
   . Technical server (2)
VIP users have a higher priority than normal users. they're also being served only by
expert servers, whereas normal users are served by both expert and rookie servers.
Users first get served by expert and rookie servers, then they may have a technical
question; that's exactly when technical servers enter.
Each user gets in its own queue which has a FIFO discipline. he may use the re-call button 
so that whenever a server is free, shall call him. but some cannot wait and may get tired
and leave the queue for good. also, there can be an interruption in the system.
Input distributions:
    1- Users' interarrival time in the first shift: Exp(1/3)
    2- Users' interarrival time in the second shift: Exp(1)
    3- Users' interarrival time in the third shift: Exp(1/2)
    4- Users' interarrival time in the first shift in interruption days: Exp(1/2)
    5- Users' interarrival time in the second shift in interruption days: Exp(2)
    6- Users' interarrival time in the third shift in interruption days: Exp(1)
    7- Expert servers' time service: Exp(1/3)
    8- Rookie servers' time service: Exp(1/7)
    9- Technical servers' time service: Exp(1/10)
Outputs:
    1- Average time VIP users spend in the system
    2- Percentage of VIP users that never wait in queues
    3- Maximum and average length and waiting time in each queue, based on user and server type
    4- Each type of servers' utilization
    5- The shift in which more users get tired and leave the queue
    6- Got tired users' average waiting time till leaving
Authors: Hamed Hatami, Mobina Hassanzade Azar
Date: Spring 2022
"""

import random
import math
import pandas as pd


def exponential(lambd):
    r = random.random()
    return -(1 / lambd) * math.log(r)


def uniform(a, b):
    r = random.random()
    return a + (b - a) * r


# To save data for all the replications
total_VIP_users_average_time_in_system = list()

total_VIP_users_zero_waiting_time_in_system = list()

total_maximum_NU_NQ_length = list()
total_maximum_VIPU_NQ_length = list()
total_maximum_NU_RQ_length = list()
total_maximum_VIPU_RQ_length = list()
total_maximum_NU_TQ_length = list()
total_maximum_VIPU_TQ_length = list()

total_average_NU_NQ_length = list()
total_average_VIPU_NQ_length = list()
total_average_NU_RQ_length = list()
total_average_VIPU_RQ_length = list()
total_average_NU_TQ_length = list()
total_average_VIPU_TQ_length = list()

total_maximum_NU_NQ_waiting_time = list()
total_maximum_VIPU_NQ_waiting_time = list()
total_maximum_NU_RQ_waiting_time = list()
total_maximum_VIPU_RQ_waiting_time = list()
total_maximum_NU_TQ_waiting_time = list()
total_maximum_VIPU_TQ_waiting_time = list()

total_average_NU_NQ_waiting_time = list()
total_average_VIPU_NQ_waiting_time = list()
total_average_NU_RQ_waiting_time = list()
total_average_VIPU_RQ_waiting_time = list()
total_average_NU_TQ_waiting_time = list()
total_average_VIPU_TQ_waiting_time = list()

total_expert_servers_utilization = list()
total_rookie_servers_utilization = list()
total_technical_servers_utilization = list()

total_average_number_of_got_tired_users_shift_1 = list()
total_average_number_of_got_tired_users_shift_2 = list()
total_average_number_of_got_tired_users_shift_3 = list()

total_got_tired_waiting_time = list()

#-----------

def starting_state():

    # State variables
    state = dict()
    state['Expert Server Status'] = 0                # 0: 0 Busy, 1: 1 Busy, 2: 2 Busy
    state['Rookie Server Status'] = 0                # 0: 0 Busy, 1: 1 Busy, 2: 2 Busy, 3: 3 Busy
    state['Technical Server Status'] = 0             # 0: 0 Busy, 1: 1 Busy, 2: 2 Busy
    state['NormalUsers-NormalQueue'] = 0             # Number of normal users in normal queue
    state['VIPUsers-NormalQueue'] = 0                # Number of VIP users in normal queue
    state['NormalUsers-RecallQueue'] = 0             # Number of normal users in re-call queue
    state['VIPUsers-RecallQueue'] = 0                # Number of VIP users in re-call queue
    state['NormalUsers-TechnicalQueue'] = 0          # Number of normal users in technical queue
    state['VIPUsers-TechnicalQueue'] = 0             # Number of VIP users in technical queue
    state['Shift'] = 1                               # Number of shift

    # Data: will save everything
    data = dict()
    data['Users'] = dict()                                           # To track each user
    
    data['Last Time NormalUsers-NormalQueue Length Changed'] = 0     # Needed to calculate area under normal queue for normal users length curve
    data['Last Time VIPUsers-NormalQueue Length Changed'] = 0        # Needed to calculate area under normal queue for VIP users length curve
    data['Last Time NormalUsers-RecallQueue Length Changed'] = 0     # Needed to calculate area under re-call queue for normal users length curve
    data['Last Time VIPUsers-RecallQueue Length Changed'] = 0        # Needed to calculate area under re-call queue for VIP length curve
    data['Last Time NormalUsers-TechnicalQueue Length Changed'] = 0  # Needed to calculate area under technical queue for normal users length curve
    data['Last Time VIPUsers-TechnicalQueue Length Changed'] = 0     # Needed to calculate area under technical queue for VIP users length curve
    
    data['NormalUsers-NormalQueue'] = dict()                         # Used to find first normal user in normal queue
    data['VIPUsers-NormalQueue'] = dict()                            # Used to find first VIP user in normal queue
    data['NormalUsers-RecallQueue'] = dict()                         # Used to find first normal user in re-call queue
    data['VIPUsers-RecallQueue'] = dict()                            # Used to find first VIP user in re-call queue
    data['NormalUsers-TechnicalQueue'] = dict()                      # Used to find first normal user in technical queue
    data['VIPUsers-TechnicalQueue'] = dict()                         # Used to find first VIP user in technical queue

    # Cumulative Stats
    data['Cumulative Stats'] = dict()
    data['Cumulative Stats']['Expert Servers Busy Time'] = 0         # Used to find utilization
    data['Cumulative Stats']['Rookie Servers Busy Time'] = 0         # Used to find utilization
    data['Cumulative Stats']['Technical Servers Busy Time'] = 0      # Used to find utilization
    
    data['Cumulative Stats']['NormalUsers-NormalQueue Waiting Time'] = 0
    data['Cumulative Stats']['VIPUsers-NormalQueue Waiting Time'] = 0
    data['Cumulative Stats']['NormalUsers-RecallQueue Waiting Time'] = 0
    data['Cumulative Stats']['VIPUsers-RecallQueue Waiting Time'] = 0
    data['Cumulative Stats']['NormalUsers-TechnicalQueue Waiting Time'] = 0
    data['Cumulative Stats']['VIPUsers-TechnicalQueue Waiting Time'] = 0
    
    data['Cumulative Stats']['Time VIP Users Spend In System']  = 0     # To calculate Average spending time for VIP users in system
    
    data['Cumulative Stats']['VIP Service Starters'] = set()            # This and the next are for finding VIP users that don't wait in queue
    data['Cumulative Stats']['Technical VIP Service Starters'] = set()  # ^
    
    data['Cumulative Stats']['Max NormalUsers-NormalQueue Length'] = 0
    data['Cumulative Stats']['Max VIPUsers-NormalQueue Length'] = 0
    data['Cumulative Stats']['Max NormalUsers-RecallQueue Length'] = 0
    data['Cumulative Stats']['Max VIPUsers-RecallQueue Length'] = 0
    data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Length'] = 0
    data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Length'] = 0
    
    data['Cumulative Stats']['Cum. NormalUsers-RecallQueue Length'] = 0
    data['Cumulative Stats']['Cum. VIPUsers-RecallQueue Length'] = 0
    data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'] = 0
    data['Cumulative Stats']['Cum. VIPUsers-TechnicalQueue Length'] = 0
    
    data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] = 0
    data['Cumulative Stats']['Max VIPUsers-NormalQueue Waiting Time'] = 0
    data['Cumulative Stats']['Max NormalUsers-RecallQueue Waiting Time'] = 0
    data['Cumulative Stats']['Max VIPUsers-RecallQueue Waiting Time'] = 0
    data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Waiting Time'] = 0
    data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Waiting Time'] = 0
    
    data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] = 0     # Needed to calculate Average length of normal queue for normal users
    data['Cumulative Stats']['Area Under VIPUsers-NormalQueue Length Curve'] = 0        # Needed to calculate Average length of normal queue for VIP users
    data['Cumulative Stats']['Area Under NormalUsers-RecallQueue Length Curve'] = 0     # Needed to calculate Average length of re-call queue for normal users
    data['Cumulative Stats']['Area Under VIPUsers-RecallQueue Length Curve'] = 0        # Needed to calculate Average Average of re-call queue for VIP users
    data['Cumulative Stats']['Area Under NormalUsers-TechnicalQueue Length Curve'] = 0  # Needed to calculate Average length of technical queue for normal users
    data['Cumulative Stats']['Area Under VIPUsers-TechnicalQueue Length Curve'] = 0     # Needed to calculate Average Average of technical queue for VIP users
    
    data['Cumulative Stats']['Got Tired Users In Shift 1'] = 0  # Number of users that got tired and left the queue in first shift
    data['Cumulative Stats']['Got Tired Users In Shift 2'] = 0  # Number of users that got tired and left the queue in second shift
    data['Cumulative Stats']['Got Tired Users In Shift 3'] = 0  # Number of users that got tired and left the queue in third shift
    
    data['Cumulative Stats']['Got tired waiting time'] = 0
    
    # Starting FEL
    future_event_list = list()
    future_event_list.append({'Event Type': 'A', 'Event Time': 0, 'User': 'U1'})
    return state, future_event_list, data


def fel_maker(data, state, future_event_list, event_type, clock, simulation_time, user = None, IntDay = None):  # Why?
    event_time = 0
    S(clock, state, future_event_list, simulation_time)
    if event_type == 'A':
        if (int(clock / (24 * 60)) + 1) != IntDay:
            if state['Shift'] % 3 == 1:
                event_time = clock + exponential(1 / 3)
            elif state['Shift'] % 3 == 2:
                event_time = clock + exponential(1)
            elif state['Shift'] % 3 == 0:
                event_time = clock + exponential(1 / 2)
        else:
            if state['Shift'] % 3 == 1:
                event_time = clock + exponential(1 / 2)
            elif state['Shift'] % 3 == 2:
                event_time = clock + exponential(2)
            else:
                event_time = clock + exponential(1)
    elif event_type == 'C':
        if data['Users'][user]['Technical Service?'] == 'Yes':
            event_time = clock + exponential(1 / 10)
        else:
            if data['Users'][user]['Assigned Server In First'] == 'Expert Server':
                event_time = clock + exponential(1 / 3)
            elif data['Users'][user]['Assigned Server In First'] == 'Rookie Server':
                event_time = clock + exponential(1 / 7)
        if event_time >= simulation_time:
            data['Cumulative Stats']['Time VIP Users Spend In System'] += simulation_time - data['Users'][user]['Arrival Time']
    elif event_type == 'O':
        if data['Users'][user]['User Type'] == 'VIP':
            x = max(25, (state['VIPUsers-NormalQueue'] - 1))
        elif data['Users'][user]['User Type'] == 'Normal':
            x = max(25, (state['NormalUsers-NormalQueue'] - 1))
        event_time = clock + uniform(25, x)

    new_event = {'Event Type': event_type, 'Event Time': event_time, 'User': user}
    future_event_list.append(new_event)



def S(clock, state, future_event_list, simulation_time):
    state['Shift'] = int(clock / 480) + 1
    if (not ({'Event Type': 'S', 'Event Time': ((int(clock / 480) + 1) * 480), 'User': None} in future_event_list)):
        future_event_list.append({'Event Type': 'S', 'Event Time': ((int(clock / 480) + 1) * 480), 'User': None})
                
    
def A(future_event_list, state, clock, data, user, IntDay, simulation_time):  # Arrival Event
    data['Users'][user] = dict()
    rn2 = uniform(0, 1)
    if rn2 < 0.7:
        data['Users'][user]['User Type'] = 'Normal'
    else:
        data['Users'][user]['User Type'] = 'VIP'
    data['Users'][user]['Arrival Time'] = clock  # Track every move of this user
    data['Users'][user]['Technical Service?'] = ''
    data['Users'][user]['Assigned Server In First'] = ''
    if data['Users'][user]['User Type'] == 'VIP':
        if state['Expert Server Status'] != 2:  # If there is at least 1 available expert server...
            state['Expert Server Status'] += 1
            data['Users'][user]['Assigned Server In First'] = 'Expert Server'
            fel_maker(data, state, future_event_list, 'C', clock, simulation_time, user, IntDay)
            data['Users'][user]['Time Service Begins'] = clock  # Track every move of this user            
            data['Cumulative Stats']['VIP Service Starters'].add(user)

        else:  # If all expert servers are busy -then> Wait in queue or use re-cal or get tired of waiting and leave the queue
            if state['VIPUsers-NormalQueue'] > 4: # User may use re-call
                rn4 = uniform(0, 1)
                if rn4 > 0.5: # User won't use re-call
                    data['Cumulative Stats']['Area Under VIPUsers-NormalQueue Length Curve'] += state['VIPUsers-NormalQueue'] * (clock - data['Last Time VIPUsers-NormalQueue Length Changed'])
                    state['VIPUsers-NormalQueue'] += 1
                    data['VIPUsers-NormalQueue'][user] = clock
                    data['Last Time VIPUsers-NormalQueue Length Changed'] = clock
                    if data['Cumulative Stats']['Max VIPUsers-NormalQueue Length'] < state['VIPUsers-NormalQueue']:
                        data['Cumulative Stats']['Max VIPUsers-NormalQueue Length'] = state['VIPUsers-NormalQueue']
                    if uniform(0, 1) <= 0.15: # User will get tired of waiting after a while
                        fel_maker(data, state, future_event_list, 'O', clock, simulation_time, user, IntDay)
                    else: # User won't get tired and will wait in queue                    
                        True    
                else: # User uses re-call
                    data['Cumulative Stats']['Area Under VIPUsers-RecallQueue Length Curve'] += state['VIPUsers-RecallQueue'] * (clock - data['Last Time VIPUsers-RecallQueue Length Changed'])
                    state['VIPUsers-RecallQueue'] += 1
                    data['VIPUsers-RecallQueue'][user] = clock
                    data['Cumulative Stats']['Cum. VIPUsers-RecallQueue Length'] += 1
                    data['Last Time VIPUsers-RecallQueue Length Changed'] = clock
                    if data['Cumulative Stats']['Max VIPUsers-RecallQueue Length'] < state['VIPUsers-RecallQueue']:
                        data['Cumulative Stats']['Max VIPUsers-RecallQueue Length'] = state['VIPUsers-RecallQueue']
            else: # User won't use re-call
                data['Cumulative Stats']['Area Under VIPUsers-NormalQueue Length Curve'] += state['VIPUsers-NormalQueue'] * (clock - data['Last Time VIPUsers-NormalQueue Length Changed'])
                state['VIPUsers-NormalQueue'] += 1
                data['VIPUsers-NormalQueue'][user] = clock
                data['Last Time VIPUsers-NormalQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max VIPUsers-NormalQueue Length'] < state['VIPUsers-NormalQueue']:
                    data['Cumulative Stats']['Max VIPUsers-NormalQueue Length'] = state['VIPUsers-NormalQueue']
                if uniform(0, 1) <= 0.15: # User will get tired of waiting after a while
                    fel_maker(data, state, future_event_list, 'O', clock, simulation_time, user, IntDay)
                else: # User won't get tired and will wait in queue                    
                    True           
    elif data['Users'][user]['User Type'] == 'Normal':
        if state['Rookie Server Status'] != 3: # If there is at least 1 available rookie server...
            state['Rookie Server Status'] += 1
            data['Users'][user]['Assigned Server In First'] = 'Rookie Server'
            fel_maker(data, state, future_event_list, 'C', clock, simulation_time, user, IntDay)
            data['Users'][user]['Time Service Begins'] = clock  # Track every move of this user            
        else: # There is no available rookie server
            if state['Expert Server Status'] != 2:  # If there is at least 1 available expert server...
                state['Expert Server Status'] += 1
                data['Users'][user]['Assigned Server In First'] = 'Expert Server'
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, user, IntDay)
                data['Users'][user]['Time Service Begins'] = clock  # Track every move of this user                
            else: # If there isn't neither an available expert server nor a rookie one...
                if state['NormalUsers-NormalQueue'] > 4: # User may use re-call
                    rn5 = uniform(0, 1)
                    if rn5 > 0.5: # User won't use re-call
                        data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] += state['NormalUsers-NormalQueue'] * (clock - data['Last Time NormalUsers-NormalQueue Length Changed'])
                        state['NormalUsers-NormalQueue'] += 1
                        data['NormalUsers-NormalQueue'][user] = clock
                        data['Last Time NormalUsers-NormalQueue Length Changed'] = clock
                        if data['Cumulative Stats']['Max NormalUsers-NormalQueue Length'] < state['NormalUsers-NormalQueue']:
                            data['Cumulative Stats']['Max NormalUsers-NormalQueue Length'] = state['NormalUsers-NormalQueue']
                        if uniform(0, 1) <= 0.15: # User will get tired of waiting after a while
                            fel_maker(data, state, future_event_list, 'O', clock, simulation_time, user, IntDay)
                        else: # User won't get tired and will wait in queue                    
                            True    
                    else: # User uses re-call
                        data['Cumulative Stats']['Area Under NormalUsers-RecallQueue Length Curve'] += state['NormalUsers-RecallQueue'] * (clock - data['Last Time NormalUsers-RecallQueue Length Changed'])
                        state['NormalUsers-RecallQueue'] += 1
                        data['NormalUsers-RecallQueue'][user] = clock
                        data['Cumulative Stats']['Cum. NormalUsers-RecallQueue Length'] += 1
                        data['Last Time NormalUsers-RecallQueue Length Changed'] = clock
                        if data['Cumulative Stats']['Max NormalUsers-RecallQueue Length'] < state['NormalUsers-RecallQueue']:
                            data['Cumulative Stats']['Max NormalUsers-RecallQueue Length'] = state['NormalUsers-RecallQueue']
                else: # User won't use re-call
                    data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] += state['NormalUsers-NormalQueue'] * (clock - data['Last Time NormalUsers-NormalQueue Length Changed'])
                    state['NormalUsers-NormalQueue'] += 1
                    data['NormalUsers-NormalQueue'][user] = clock
                    data['Last Time NormalUsers-NormalQueue Length Changed'] = clock
                    if data['Cumulative Stats']['Max NormalUsers-NormalQueue Length'] < state['NormalUsers-NormalQueue']:
                        data['Cumulative Stats']['Max NormalUsers-NormalQueue Length'] = state['NormalUsers-NormalQueue']
                    if uniform(0, 1) <= 0.15: # User will get tired of waiting after a while
                        fel_maker(data, state, future_event_list, 'O', clock, simulation_time, user, IntDay)
                    else: # User won't get tired and will wait in queue                    
                        True
    # Scheduling the next arrival
    next_user = 'U' + str(int(user[1:]) + 1)   
    fel_maker(data, state, future_event_list, 'A', clock, simulation_time, next_user, IntDay)


def C(future_event_list, state, clock, data, user, IntDay, simulation_time): # End of Service Event
    S(clock, state, future_event_list, simulation_time)
    if data['Users'][user]['Technical Service?'] == 'Yes':
        data['Cumulative Stats']['Technical Servers Busy Time'] += clock - data['Users'][user]['Technical Time Service Begins']
        if data['Users'][user]['User Type'] == 'VIP':
            data['Cumulative Stats']['Time VIP Users Spend In System'] += clock - data['Users'][user]['Arrival Time']
        # Check the queue
        if state['VIPUsers-TechnicalQueue'] != 0: # First check the VIP users' queue
            first_user_in_queue = min(data['VIPUsers-TechnicalQueue'], key = data['VIPUsers-TechnicalQueue'].get)
            data['Users'][first_user_in_queue]['Technical Time Service Begins'] = clock # Start getting technical service for this user
            data['Cumulative Stats']['VIPUsers-TechnicalQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time To Technical']
            data['Cumulative Stats']['Area Under VIPUsers-TechnicalQueue Length Curve'] += state['VIPUsers-TechnicalQueue'] * (clock - data['Last Time VIPUsers-TechnicalQueue Length Changed'])
            state['VIPUsers-TechnicalQueue'] -= 1
            data['VIPUsers-TechnicalQueue'].pop(first_user_in_queue, None)
            data['Last Time VIPUsers-TechnicalQueue Length Changed'] = clock
            if data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time To Technical']:
                    data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time To Technical']
            fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
        elif state['NormalUsers-TechnicalQueue'] != 0: # Then check the normal users' queue
            first_user_in_queue = min(data['NormalUsers-TechnicalQueue'], key = data['NormalUsers-TechnicalQueue'].get)
            data['Users'][first_user_in_queue]['Technical Time Service Begins'] = clock # Start getting technical service for this user
            data['Cumulative Stats']['NormalUsers-TechnicalQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time To Technical']
            data['Cumulative Stats']['Area Under NormalUsers-TechnicalQueue Length Curve'] += state['NormalUsers-TechnicalQueue'] * (clock - data['Last Time NormalUsers-TechnicalQueue Length Changed'])
            state['NormalUsers-TechnicalQueue'] -= 1
            data['NormalUsers-TechnicalQueue'].pop(first_user_in_queue, None)
            data['Last Time NormalUsers-TechnicalQueue Length Changed'] = clock
            if data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time To Technical']:
                    data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time To Technical']
            fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
        else: # Nobody there? then make one of the technical servers free
            state['Technical Server Status'] -= 1
    else:
        if data['Users'][user]['Assigned Server In First'] == 'Expert Server':
            if data['Users'][user]['User Type'] == 'VIP':
                data['Cumulative Stats']['Expert Servers Busy Time'] += clock - data['Users'][user]['Time Service Begins']
                if uniform(0, 1) <= 0.15: # User will use technical service                    
                    data['Users'][user]['Technical Service?'] = 'Yes'
                    data['Users'][user]['Arrival Time To Technical'] = clock                    
                    if state['Technical Server Status'] != 2: # Starts technical service immediately
                        state['Technical Server Status'] += 1
                        fel_maker(data, state, future_event_list, 'C', clock, simulation_time, user, IntDay) # Schedule End of Service event for this user
                        data['Users'][user]['Technical Time Service Begins'] = clock
                        data['Cumulative Stats']['Cum. VIPUsers-TechnicalQueue Length'] += 1
                        data['Cumulative Stats']['Technical VIP Service Starters'].add(user)
                    else: # Waits in technical service queue                        
                        data['Cumulative Stats']['Area Under VIPUsers-TechnicalQueue Length Curve'] += state['VIPUsers-TechnicalQueue'] * (clock - data['Last Time VIPUsers-TechnicalQueue Length Changed'])
                        state['VIPUsers-TechnicalQueue'] += 1
                        data['VIPUsers-TechnicalQueue'][user] = clock
                        data['Cumulative Stats']['Cum. VIPUsers-TechnicalQueue Length'] += 1
                        data['Last Time VIPUsers-TechnicalQueue Length Changed'] = clock                        
                        if data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Length'] < state['VIPUsers-TechnicalQueue']:
                            data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Length'] = state['VIPUsers-TechnicalQueue']
                else: # User won't use technical service 
                    data['Cumulative Stats']['Time VIP Users Spend In System'] += clock - data['Users'][user]['Arrival Time']
            elif data['Users'][user]['User Type'] == 'Normal':
                data['Cumulative Stats']['Expert Servers Busy Time'] += clock - data['Users'][user]['Time Service Begins']
                if uniform(0, 1) <= 0.15: # User will use technical service
                    data['Users'][user]['Technical Service?'] = 'Yes'
                    data['Users'][user]['Arrival Time To Technical'] = clock
                    if state['Technical Server Status'] < 2: # Starts technical service immediately
                        state['Technical Server Status'] += 1
                        fel_maker(data, state, future_event_list, 'C', clock, simulation_time, user, IntDay) # Schedule End of Service event for this user
                        data['Users'][user]['Technical Time Service Begins'] = clock
                        data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'] += 1
                    else: # Waits in technical service queue
                        data['Cumulative Stats']['Area Under NormalUsers-TechnicalQueue Length Curve'] += state['NormalUsers-TechnicalQueue'] * (clock - data['Last Time NormalUsers-TechnicalQueue Length Changed'])
                        state['NormalUsers-TechnicalQueue'] += 1
                        data['NormalUsers-TechnicalQueue'][user] = clock
                        data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'] += 1
                        data['Last Time NormalUsers-TechnicalQueue Length Changed'] = clock
                        if data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Length'] < state['NormalUsers-TechnicalQueue']:
                            data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Length'] = state['NormalUsers-TechnicalQueue']
                else: # User won't use technical service
                    True
            # Check the queue
            if state['VIPUsers-NormalQueue'] > 0: # First check the VIP users' queue
                first_user_in_queue = min(data['VIPUsers-NormalQueue'], key = data['VIPUsers-NormalQueue'].get)
                data['Users'][first_user_in_queue]['Time Service Begins'] = clock
                data['Cumulative Stats']['VIPUsers-NormalQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time']
                data['Cumulative Stats']['Area Under VIPUsers-NormalQueue Length Curve'] += state['VIPUsers-NormalQueue'] * (clock - data['Last Time VIPUsers-NormalQueue Length Changed'])
                state['VIPUsers-NormalQueue'] -= 1
                data['Users'][first_user_in_queue]['Assigned Server In First'] = 'Expert Server'
                data['VIPUsers-NormalQueue'].pop(first_user_in_queue, None)
                data['Last Time VIPUsers-NormalQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max VIPUsers-NormalQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time']:
                    data['Cumulative Stats']['Max VIPUsers-NormalQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time']
                for event in future_event_list: # Remove the getting tired event for this user, if already scheduled
                    if event['Event Type'] == 'O' and event['User'] == first_user_in_queue:
                        future_event_list.remove(event)
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
            elif state['NormalUsers-NormalQueue'] > 0:
                first_user_in_queue = min(data['NormalUsers-NormalQueue'], key = data['NormalUsers-NormalQueue'].get)
                data['Users'][first_user_in_queue]['Time Service Begins'] = clock
                data['Cumulative Stats']['NormalUsers-NormalQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time']
                data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] += state['NormalUsers-NormalQueue'] * (clock - data['Last Time NormalUsers-NormalQueue Length Changed'])
                state['NormalUsers-NormalQueue'] -= 1
                data['Users'][first_user_in_queue]['Assigned Server In First'] = 'Expert Server'
                data['NormalUsers-NormalQueue'].pop(first_user_in_queue, None)
                data['Last Time NormalUsers-NormalQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time']:
                    data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time']
                for event in future_event_list: # Remove the getting tired event for this user, if already scheduled
                    if event['Event Type'] == 'O' and event['User'] == first_user_in_queue:
                        future_event_list.remove(event)
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
            elif (state['Shift'] % 3) != 1 and state['VIPUsers-RecallQueue'] > 0: # Nobody in queue? then re-call a VIP user if there is any
                first_user_in_queue = min(data['VIPUsers-RecallQueue'], key = data['VIPUsers-RecallQueue'].get)
                data['Users'][first_user_in_queue]['Time Service Begins'] = clock
                data['Cumulative Stats']['VIPUsers-RecallQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time']
                data['Cumulative Stats']['Area Under VIPUsers-RecallQueue Length Curve'] += state['VIPUsers-RecallQueue'] * (clock - data['Last Time VIPUsers-RecallQueue Length Changed'])
                state['VIPUsers-RecallQueue'] -= 1
                data['Users'][first_user_in_queue]['Assigned Server In First'] = 'Expert Server'
                data['VIPUsers-RecallQueue'].pop(first_user_in_queue, None)
                data['Last Time VIPUsers-RecallQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max VIPUsers-RecallQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time']:
                    data['Cumulative Stats']['Max VIPUsers-RecallQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time']
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
            elif (state['Shift'] % 3) != 1 and state['NormalUsers-RecallQueue'] > 0:
                first_user_in_queue = min(data['NormalUsers-RecallQueue'], key = data['NormalUsers-RecallQueue'].get)
                data['Users'][first_user_in_queue]['Time Service Begins'] = clock
                data['Cumulative Stats']['NormalUsers-RecallQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time']
                data['Cumulative Stats']['Area Under NormalUsers-RecallQueue Length Curve'] += state['NormalUsers-RecallQueue'] * (clock - data['Last Time NormalUsers-RecallQueue Length Changed'])
                state['NormalUsers-RecallQueue'] -= 1
                data['Users'][first_user_in_queue]['Assigned Server In First'] = 'Expert Server'
                data['NormalUsers-RecallQueue'].pop(first_user_in_queue, None)
                data['Last Time NormalUsers-RecallQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max NormalUsers-RecallQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time']:
                    data['Cumulative Stats']['Max NormalUsers-RecallQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time']
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
            else: # None of them? then make one of the expert servers free
                state['Expert Server Status'] -= 1

                
        elif data['Users'][user]['Assigned Server In First'] == 'Rookie Server':
            data['Cumulative Stats']['Rookie Servers Busy Time'] += clock - data['Users'][user]['Time Service Begins']
            if uniform(0, 1) <= 0.15: # User will use technical service
                data['Users'][user]['Technical Service?'] = 'Yes'
                data['Users'][user]['Arrival Time To Technical'] = clock
                if state['Technical Server Status'] < 2: # Starts technical service immediately
                    state['Technical Server Status'] += 1
                    fel_maker(data, state, future_event_list, 'C', clock, simulation_time, user, IntDay) # Schedule End of Service event for this user
                    data['Users'][user]['Technical Time Service Begins'] = clock
                    data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'] += 1
                else: # Waits in technical service queue
                    data['Cumulative Stats']['Area Under NormalUsers-TechnicalQueue Length Curve'] += state['NormalUsers-TechnicalQueue'] * (clock - data['Last Time NormalUsers-TechnicalQueue Length Changed'])
                    state['NormalUsers-TechnicalQueue'] += 1
                    data['NormalUsers-TechnicalQueue'][user] = clock
                    data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'] += 1
                    data['Last Time NormalUsers-TechnicalQueue Length Changed'] = clock
                    if data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Length'] < state['NormalUsers-TechnicalQueue']:
                        data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Length'] = state['NormalUsers-TechnicalQueue']
            else: # User won't use technical service
                True
            # Check the queue
            if state['NormalUsers-NormalQueue'] > 0:
                first_user_in_queue = min(data['NormalUsers-NormalQueue'], key = data['NormalUsers-NormalQueue'].get)
                data['Users'][first_user_in_queue]['Time Service Begins'] = clock
                data['Cumulative Stats']['NormalUsers-NormalQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time']
                data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] += state['NormalUsers-NormalQueue'] * (clock - data['Last Time NormalUsers-NormalQueue Length Changed'])
                state['NormalUsers-NormalQueue'] -= 1
                data['Users'][first_user_in_queue]['Assigned Server In First'] = 'Rookie Server'
                data['NormalUsers-NormalQueue'].pop(first_user_in_queue, None)
                data['Last Time NormalUsers-NormalQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time']:
                    data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time']
                for event in future_event_list: # Remove the getting tired event for this user, if already scheduled
                    if event['Event Type'] == 'O' and event['User'] == first_user_in_queue:
                        future_event_list.remove(event)
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
            elif (state['Shift'] % 3) != 1 and state['NormalUsers-RecallQueue'] > 0:
                first_user_in_queue = min(data['NormalUsers-RecallQueue'], key = data['NormalUsers-RecallQueue'].get)
                data['Users'][first_user_in_queue]['Time Service Begins'] = clock
                data['Cumulative Stats']['NormalUsers-RecallQueue Waiting Time'] += clock - data['Users'][first_user_in_queue]['Arrival Time']
                data['Cumulative Stats']['Area Under NormalUsers-RecallQueue Length Curve'] += state['NormalUsers-RecallQueue'] * (clock - data['Last Time NormalUsers-RecallQueue Length Changed'])
                state['NormalUsers-RecallQueue'] -= 1
                data['Users'][first_user_in_queue]['Assigned Server In First'] = 'Rookie Server'
                data['NormalUsers-RecallQueue'].pop(first_user_in_queue, None)
                data['Last Time NormalUsers-RecallQueue Length Changed'] = clock
                if data['Cumulative Stats']['Max NormalUsers-RecallQueue Waiting Time'] < clock - data['Users'][first_user_in_queue]['Arrival Time']:
                    data['Cumulative Stats']['Max NormalUsers-RecallQueue Waiting Time'] = clock - data['Users'][first_user_in_queue]['Arrival Time']
                fel_maker(data, state, future_event_list, 'C', clock, simulation_time, first_user_in_queue, IntDay) # Schedule End of Service event for this user
            else: # None of them? then make one of the rookie servers free
                state['Rookie Server Status'] -= 1

def O(state, clock, data, user): # Getting Tired of Waiting Event
    if data['Users'][user]['User Type'] == 'VIP':
        data['Cumulative Stats']['VIPUsers-NormalQueue Waiting Time'] += clock - data['Users'][user]['Arrival Time']
        data['Cumulative Stats']['Area Under VIPUsers-NormalQueue Length Curve'] += state['VIPUsers-NormalQueue'] * (clock - data['Last Time VIPUsers-NormalQueue Length Changed'])
        state['VIPUsers-NormalQueue'] -= 1
        data['VIPUsers-NormalQueue'].pop(user, None)
        data['Last Time VIPUsers-NormalQueue Length Changed'] = clock
        if data['Cumulative Stats']['Max VIPUsers-NormalQueue Waiting Time'] < clock - data['Users'][user]['Arrival Time']:
            data['Cumulative Stats']['Max VIPUsers-NormalQueue Waiting Time'] = clock - data['Users'][user]['Arrival Time']
        data['Cumulative Stats']['Time VIP Users Spend In System'] += clock - data['Users'][user]['Arrival Time']
        
    elif data['Users'][user]['User Type'] == 'Normal':
        data['Cumulative Stats']['NormalUsers-NormalQueue Waiting Time'] += clock - data['Users'][user]['Arrival Time']
        data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] += state['NormalUsers-NormalQueue'] * (clock - data['Last Time NormalUsers-NormalQueue Length Changed'])
        state['NormalUsers-NormalQueue'] -= 1
        data['NormalUsers-NormalQueue'].pop(user, None)
        data['Last Time NormalUsers-NormalQueue Length Changed'] = clock
        if data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] < clock - data['Users'][user]['Arrival Time']:
            data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time'] = clock - data['Users'][user]['Arrival Time']
          
    if (state['Shift'] % 3) == 1:       
        data['Cumulative Stats']['Got Tired Users In Shift 1'] += 1  
    elif (state['Shift'] % 3) == 2:       
        data['Cumulative Stats']['Got Tired Users In Shift 2'] += 1
    elif (state['Shift'] % 3) == 0:    
        data['Cumulative Stats']['Got Tired Users In Shift 3'] += 1 
        
    data['Cumulative Stats']['Got tired waiting time'] += clock - data['Users'][user]['Arrival Time']
           

def create_row(step, current_event, state, data, future_event_list):
    # This function will create a list, which will eventually become a row of the output Excel file

    sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])

    # What should this row contain?
    # 1. Step, Clock, Event Type and Event Customer
    row = [step, current_event['Event Time'], current_event['Event Type'], current_event['User']]
    # 2. All state variables
    row.extend(list(state.values()))
    # 3. All Cumulative Stats
    row.extend(list(data['Cumulative Stats'].values()))

    # 4. All events in fel ('Event Time', 'Event Type' & 'Event User' for each event)
    for event in sorted_fel:
        row.append(event['Event Time'])
        row.append(event['Event Type'])
        row.append(event['User'])
    return row


def justify(table):
    # This function adds blanks to short rows in order to match their lengths to the maximum row length

    # Find maximum row length in the table
    row_max_len = 0
    for row in table:
        if len(row) > row_max_len:
            row_max_len = len(row)

    # For each row, add enough blanks
    for row in table:
        row.extend([""] * (row_max_len - len(row)))


def create_main_header(state, data):
    # This function creates the main part of header (returns a list)
    # A part of header which is used for future events will be created in create_excel()

    # Header consists of ...
    # 1. Step, Clock, Event Type and Event Customer
    header = ['Step', 'Clock', 'Event Type', 'Event User']
    # 2. Names of the state variables
    header.extend(list(state.keys()))
    # 3. Names of the cumulative stats
    header.extend(list(data['Cumulative Stats'].keys()))
    return header


def create_excel(table, header):
    # This function creates and fine-tunes the Excel output file

    # Find length of each row in the table
    row_len = len(table[0])

    # Find length of header (header does not include cells for fel at this moment)
    header_len = len(header)

    # row_len exceeds header_len by (max_fel_length * 3) (Event Type, Event Time & Customer for each event in FEL)
    # Extend the header with 'Future Event Time', 'Future Event Type', 'Future Event Customer'
    # for each event in the fel with maximum size
    i = 1
    for col in range((row_len - header_len) // 3):
        header.append('Future Event Time ' + str(i))
        header.append('Future Event Type ' + str(i))
        header.append('Future Event User ' + str(i))
        i += 1

    # Dealing with the output
    # First create a pandas DataFrame
    df = pd.DataFrame(table, columns=header, index=None)

    # Create a handle to work on the Excel file
    writer = pd.ExcelWriter('Simulation-Output.xlsx', engine='xlsxwriter')

    # Write out the Excel file to the hard drive
    df.to_excel(writer, sheet_name='Output', header=False, startrow=1, index=False)

    workbook = writer.book

    # Get the sheet we want to work on
    worksheet = writer.sheets['Output']

    # Create a cell-formatter object (this will be used for the cells in the header, hence: header_formatter!)
    header_formatter = workbook.add_format()
    header_formatter.set_align('center')
    header_formatter.set_align('vcenter')
    header_formatter.set_font('Times New Roman')
    header_formatter.set_bold('True')

    # Write out the column names and apply the format to the cells in the header row
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_formatter)

    # Auto-fit columns
    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i - 1, i - 1, width)

    # Create a cell-formatter object for the body of excel file
    main_formatter = workbook.add_format()
    main_formatter.set_align('center')
    main_formatter.set_align('vcenter')
    main_formatter.set_font('Times New Roman')

    # Apply the format to the body cells
    for row in range(1, len(df) + 1):
        worksheet.set_row(row, None, main_formatter)

    # Save your edits
    writer.save()


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def simulation(simulation_time):
    state, future_event_list, data = starting_state()
    clock = 0
#    table = []  # A list of lists. Each inner list will be a row in the Excel output
#    step = 1  # Every event counts as a step
    
    # To determine which day in each month, there will be a network interruption
    IntDays = dict()
    for j in range(0, int(simulation_time / (30 * 24 * 60)) + 1):
        IntDays[j + 1] = int(uniform(0.033334, 1.033333) * 30) + j * 30
        while IntDays[j + 1] > (int((simulation_time * 24 * 60) / (24 * 60))):
            IntDays[j + 1] = int(uniform(0.033334, 1.033333) * 30) + j * 30
    future_event_list.append({'Event Type': 'End of Simulation', 'Event Time': simulation_time, 'User': None})

    while clock < simulation_time:
        sorted_fel = sorted(future_event_list, key = lambda x: x['Event Time'])
        current_event = sorted_fel[0]
        clock = current_event['Event Time']
        user = current_event['User']
        IntDay = IntDays[int(clock / (30 * 24 * 60)) + 1]
        
        if clock < simulation_time:  # = if current_event['Event Type'] != 'End of Simulation'
            if current_event['Event Type'] == 'A':
                A(future_event_list, state, clock, data, user, IntDay, simulation_time)
            elif current_event['Event Type'] == 'C':
                C(future_event_list, state, clock, data, user, IntDay, simulation_time)
            elif current_event['Event Type'] == 'O':
                O(state, clock, data, user)              
            future_event_list.remove(current_event)
        else:
            future_event_list.clear()
#        table.append(create_row(step, current_event, state, data, future_event_list))
#        step += 1
#        
#    excel_main_header = create_main_header(state, data)
#    justify(table)
#    create_excel(table, excel_main_header)        

    total_number_of_normal_users_partial = 0
    total_number_of_VIP_users_partial = 0
    for user in list(data['Users'].keys()):
        if data['Users'][user]['User Type'] == 'Normal':
            total_number_of_normal_users_partial += 1
        elif data['Users'][user]['User Type'] == 'VIP':
            total_number_of_VIP_users_partial += 1
            
    total_number_of_VIP_users_without_waiting_partial = 0
    for suww in list(data['Cumulative Stats']['VIP Service Starters']):
        if data['Users'][suww]['Technical Service?'] != 'Yes':
            total_number_of_VIP_users_without_waiting_partial += 1
        else:
            if suww in list(data['Cumulative Stats']['Technical VIP Service Starters']):
                total_number_of_VIP_users_without_waiting_partial += 1
    
    # To prevent potential division by zero
#    for t in [data['Cumulative Stats']['Cum. NormalUsers-RecallQueue Length'], data['Cumulative Stats']['Cum. VIPUsers-RecallQueue Length'], data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'], data['Cumulative Stats']['Cum. VIPUsers-TechnicalQueue Length'],
#                data['Cumulative Stats']['Got Tired Users In Shift 1'], data['Cumulative Stats']['Got Tired Users In Shift 2'], data['Cumulative Stats']['Got Tired Users In Shift 3']]:
#        if t == 0:
#            t = 1
    
    VIP_users_average_time_in_system_partial = (data['Cumulative Stats']['Time VIP Users Spend In System'] / total_number_of_VIP_users_partial)
    
    percentage_of_VIP_users_without_waiting_partial = (total_number_of_VIP_users_without_waiting_partial / total_number_of_VIP_users_partial) * 100    
    
    Max_NormalUsers_NormalQueue_Length_partial = data['Cumulative Stats']['Max NormalUsers-NormalQueue Length']
    Max_VIPUsers_NormalQueue_Length_partial = data['Cumulative Stats']['Max VIPUsers-NormalQueue Length']
    Max_NormalUsers_RecallQueue_Length_partial = data['Cumulative Stats']['Max NormalUsers-RecallQueue Length']
    Max_VIPUsers_RecallQueue_Length_partial = data['Cumulative Stats']['Max VIPUsers-RecallQueue Length']
    Max_NormalUsers_TechnicalQueue_Length_partial = data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Length']
    Max_VIPUsers_TechnicalQueue_Length_partial = data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Length']
    
    Average_NormalUsers_NormalQueue_Length_partial = (data['Cumulative Stats']['Area Under NormalUsers-NormalQueue Length Curve'] / simulation_time)
    Average_VIPUsers_NormalQueue_Length_partial = (data['Cumulative Stats']['Area Under VIPUsers-NormalQueue Length Curve'] / simulation_time)
    Average_NormalUsers_RecallQueue_Length_partial = (data['Cumulative Stats']['Area Under NormalUsers-RecallQueue Length Curve'] / simulation_time)
    Average_VIPUsers_RecallQueue_Length_partial = (data['Cumulative Stats']['Area Under VIPUsers-RecallQueue Length Curve'] / simulation_time)
    Average_NormalUsers_TechnicalQueue_Length_partial = (data['Cumulative Stats']['Area Under NormalUsers-TechnicalQueue Length Curve'] / simulation_time)
    Average_VIPUsers_TechnicalQueue_Length_partial = (data['Cumulative Stats']['Area Under VIPUsers-TechnicalQueue Length Curve'] / simulation_time)
        
    Max_NormalUsers_NormalQueue_Waiting_Time_partial = data['Cumulative Stats']['Max NormalUsers-NormalQueue Waiting Time']
    Max_VIPUsers_NormalQueue_Waiting_Time_partial = data['Cumulative Stats']['Max VIPUsers-NormalQueue Waiting Time']
    Max_NormalUsers_RecallQueue_Waiting_Time_partial = data['Cumulative Stats']['Max NormalUsers-RecallQueue Waiting Time']
    Max_VIPUsers_RecallQueue_Waiting_Time_partial = data['Cumulative Stats']['Max VIPUsers-RecallQueue Waiting Time']
    Max_NormalUsers_TechnicalQueue_Waiting_Time_partial = data['Cumulative Stats']['Max NormalUsers-TechnicalQueue Waiting Time']
    Max_VIPUsers_TechnicalQueue_Waiting_Time_partial = data['Cumulative Stats']['Max VIPUsers-TechnicalQueue Waiting Time']
    
    try:
        Average_NormalUsers_NormalQueue_Waiting_Time_partial = (data['Cumulative Stats']['NormalUsers-NormalQueue Waiting Time'] / (total_number_of_normal_users_partial - data['Cumulative Stats']['Cum. NormalUsers-RecallQueue Length']))
    except:
        Average_NormalUsers_NormalQueue_Waiting_Time_partial = 0
    try:
        Average_VIPUsers_NormalQueue_Waiting_Time_partial = (data['Cumulative Stats']['VIPUsers-NormalQueue Waiting Time'] / (total_number_of_VIP_users_partial - data['Cumulative Stats']['Cum. VIPUsers-RecallQueue Length']))
    except:
        Average_VIPUsers_NormalQueue_Waiting_Time_partial = 0
    try:
        Average_NormalUsers_RecallQueue_Waiting_Time_partial = (data['Cumulative Stats']['NormalUsers-RecallQueue Waiting Time'] / data['Cumulative Stats']['Cum. NormalUsers-RecallQueue Length'])
    except:
        Average_NormalUsers_RecallQueue_Waiting_Time_partial = 0
    try:
        Average_VIPUsers_RecallQueue_Waiting_Time_partial = (data['Cumulative Stats']['VIPUsers-RecallQueue Waiting Time'] / data['Cumulative Stats']['Cum. VIPUsers-RecallQueue Length'])
    except:
        Average_VIPUsers_RecallQueue_Waiting_Time_partial = 0
    try:
        Average_NormalUsers_TechnicalQueue_Waiting_Time_partial = (data['Cumulative Stats']['NormalUsers-TechnicalQueue Waiting Time'] / data['Cumulative Stats']['Cum. NormalUsers-TechnicalQueue Length'])
    except:
        Average_NormalUsers_TechnicalQueue_Waiting_Time_partial = 0
    try:
        Average_VIPUsers_TechnicalQueue_Waiting_Time_partial = (data['Cumulative Stats']['VIPUsers-TechnicalQueue Waiting Time'] / data['Cumulative Stats']['Cum. VIPUsers-TechnicalQueue Length'])
    except:
        Average_VIPUsers_TechnicalQueue_Waiting_Time_partial = 0
    
    expert_servers_utilization_partial = (data['Cumulative Stats']['Expert Servers Busy Time'] / (2 * simulation_time))
    rookie_servers_utilization_partial = (data['Cumulative Stats']['Rookie Servers Busy Time'] / (3 * simulation_time))
    technical_servers_utilization_partial = (data['Cumulative Stats']['Technical Servers Busy Time'] / (2 * simulation_time))
    
    got_tired_users_in_shift_1_partial = data['Cumulative Stats']['Got Tired Users In Shift 1']
    got_tired_users_in_shift_2_partial = data['Cumulative Stats']['Got Tired Users In Shift 2']
    got_tired_users_in_shift_3_partial = data['Cumulative Stats']['Got Tired Users In Shift 3']
    
    
    try:
        got_tired_waiting_time_partial = (data['Cumulative Stats']['Got tired waiting time'] / (data['Cumulative Stats']['Got Tired Users In Shift 1'] + data['Cumulative Stats']['Got Tired Users In Shift 2'] + data['Cumulative Stats']['Got Tired Users In Shift 3']))
    except:
        got_tired_waiting_time_partial = 0
    
#   --------------------------------------------------------------------------- 
    
    total_VIP_users_average_time_in_system.append(VIP_users_average_time_in_system_partial)
    
    total_VIP_users_zero_waiting_time_in_system.append(percentage_of_VIP_users_without_waiting_partial)
    
    total_maximum_NU_NQ_length.append(Max_NormalUsers_NormalQueue_Length_partial)
    total_maximum_VIPU_NQ_length.append(Max_VIPUsers_NormalQueue_Length_partial)
    total_maximum_NU_RQ_length.append(Max_NormalUsers_RecallQueue_Length_partial)
    total_maximum_VIPU_RQ_length.append(Max_VIPUsers_RecallQueue_Length_partial)
    total_maximum_NU_TQ_length.append(Max_NormalUsers_TechnicalQueue_Length_partial)
    total_maximum_VIPU_TQ_length.append(Max_VIPUsers_TechnicalQueue_Length_partial)
    
    total_average_NU_NQ_length.append(Average_NormalUsers_NormalQueue_Length_partial)
    total_average_VIPU_NQ_length.append(Average_VIPUsers_NormalQueue_Length_partial)
    total_average_NU_RQ_length.append(Average_NormalUsers_RecallQueue_Length_partial)
    total_average_VIPU_RQ_length.append(Average_VIPUsers_RecallQueue_Length_partial)
    total_average_NU_TQ_length.append(Average_NormalUsers_TechnicalQueue_Length_partial)
    total_average_VIPU_TQ_length.append(Average_VIPUsers_TechnicalQueue_Length_partial)
    
    total_maximum_NU_NQ_waiting_time.append(Max_NormalUsers_NormalQueue_Waiting_Time_partial)
    total_maximum_VIPU_NQ_waiting_time.append(Max_VIPUsers_NormalQueue_Waiting_Time_partial)
    total_maximum_NU_RQ_waiting_time.append(Max_NormalUsers_RecallQueue_Waiting_Time_partial)
    total_maximum_VIPU_RQ_waiting_time.append(Max_VIPUsers_RecallQueue_Waiting_Time_partial)
    total_maximum_NU_TQ_waiting_time.append(Max_NormalUsers_TechnicalQueue_Waiting_Time_partial)
    total_maximum_VIPU_TQ_waiting_time.append(Max_VIPUsers_TechnicalQueue_Waiting_Time_partial)
    
    total_average_NU_NQ_waiting_time.append(Average_NormalUsers_NormalQueue_Waiting_Time_partial)
    total_average_VIPU_NQ_waiting_time.append(Average_VIPUsers_NormalQueue_Waiting_Time_partial)
    total_average_NU_RQ_waiting_time.append(Average_NormalUsers_RecallQueue_Waiting_Time_partial)
    total_average_VIPU_RQ_waiting_time.append(Average_VIPUsers_RecallQueue_Waiting_Time_partial)
    total_average_NU_TQ_waiting_time.append(Average_NormalUsers_TechnicalQueue_Waiting_Time_partial)
    total_average_VIPU_TQ_waiting_time.append(Average_VIPUsers_TechnicalQueue_Waiting_Time_partial)
    
    total_expert_servers_utilization.append(expert_servers_utilization_partial)
    total_rookie_servers_utilization.append(rookie_servers_utilization_partial)
    total_technical_servers_utilization.append(technical_servers_utilization_partial)
    
    total_average_number_of_got_tired_users_shift_1.append(got_tired_users_in_shift_1_partial)
    total_average_number_of_got_tired_users_shift_2.append(got_tired_users_in_shift_2_partial)
    total_average_number_of_got_tired_users_shift_3.append(got_tired_users_in_shift_3_partial)
    
    total_got_tired_waiting_time.append(got_tired_waiting_time_partial)


#simulation(30*24*60)
for b in range(1):
    simulation(30 * 24 * 60)

VIP_users_average_time_in_system = round((sum(total_VIP_users_average_time_in_system) / len(total_VIP_users_average_time_in_system)), 2)

percentage_of_VIP_users_without_waiting = round((sum(total_VIP_users_zero_waiting_time_in_system) / len(total_VIP_users_zero_waiting_time_in_system)), 2)

Max_NormalUsers_NormalQueue_Length = round((sum(total_maximum_NU_NQ_length) / len(total_maximum_NU_NQ_length)), 2)
Max_VIPUsers_NormalQueue_Length = round((sum(total_maximum_VIPU_NQ_length) / len(total_maximum_VIPU_NQ_length)), 2)
Max_NormalUsers_RecallQueue_Length = round((sum(total_maximum_NU_RQ_length) / len(total_maximum_NU_RQ_length)), 2)
Max_VIPUsers_RecallQueue_Length = round((sum(total_maximum_VIPU_RQ_length) / len(total_maximum_VIPU_RQ_length)), 2)
Max_NormalUsers_TechnicalQueue_Length = round((sum(total_maximum_NU_TQ_length) / len(total_maximum_NU_TQ_length)), 2)
Max_VIPUsers_TechnicalQueue_Length = round((sum(total_maximum_VIPU_TQ_length) / len(total_maximum_VIPU_TQ_length)), 2)

Average_NormalUsers_NormalQueue_Length = round((sum(total_average_NU_NQ_length) / len(total_average_NU_NQ_length)), 2)
Average_VIPUsers_NormalQueue_Length = round((sum(total_average_VIPU_NQ_length) / len(total_average_VIPU_NQ_length)), 2)
Average_NormalUsers_RecallQueue_Length = round((sum(total_average_NU_RQ_length) / len(total_average_NU_RQ_length)), 2)
Average_VIPUsers_RecallQueue_Length = round((sum(total_average_VIPU_RQ_length) / len(total_average_VIPU_RQ_length)), 2)
Average_NormalUsers_TechnicalQueue_Length = round((sum(total_average_NU_TQ_length) / len(total_average_NU_TQ_length)), 2)
Average_VIPUsers_TechnicalQueue_Length = round((sum(total_average_VIPU_TQ_length) / len(total_average_VIPU_TQ_length)), 2)

Max_NormalUsers_NormalQueue_Waiting_Time = round((sum(total_maximum_NU_NQ_waiting_time) / len(total_maximum_NU_NQ_waiting_time)), 2)
Max_VIPUsers_NormalQueue_Waiting_Time = round((sum(total_maximum_VIPU_NQ_waiting_time) / len(total_maximum_VIPU_NQ_waiting_time)), 2)
Max_NormalUsers_RecallQueue_Waiting_Time = round((sum(total_maximum_NU_RQ_waiting_time) / len(total_maximum_NU_RQ_waiting_time)), 2)
Max_VIPUsers_RecallQueue_Waiting_Time = round((sum(total_maximum_VIPU_RQ_waiting_time) / len(total_maximum_VIPU_RQ_waiting_time)), 2)
Max_NormalUsers_TechnicalQueue_Waiting_Time = round((sum(total_maximum_NU_TQ_waiting_time) / len(total_maximum_NU_TQ_waiting_time)), 2)
Max_VIPUsers_TechnicalQueue_Waiting_Time = round((sum(total_maximum_VIPU_TQ_waiting_time) / len(total_maximum_VIPU_TQ_waiting_time)), 2)

Average_NormalUsers_NormalQueue_Waiting_Time = round((sum(total_average_NU_NQ_waiting_time) / len(total_average_NU_NQ_waiting_time)), 2)
Average_VIPUsers_NormalQueue_Waiting_Time = round((sum(total_average_VIPU_NQ_waiting_time) / len(total_average_VIPU_NQ_waiting_time)), 2)
Average_NormalUsers_RecallQueue_Waiting_Time = round((sum(total_average_NU_RQ_waiting_time) / len(total_average_NU_RQ_waiting_time)), 2)
Average_VIPUsers_RecallQueue_Waiting_Time = round((sum(total_average_VIPU_RQ_waiting_time) / len(total_average_VIPU_RQ_waiting_time)), 2)
Average_NormalUsers_TechnicalQueue_Waiting_Time = round((sum(total_average_NU_TQ_waiting_time) / len(total_average_NU_TQ_waiting_time)), 2)
Average_VIPUsers_TechnicalQueue_Waiting_Time = round((sum(total_average_VIPU_TQ_waiting_time) / len(total_average_VIPU_TQ_waiting_time)), 2)

expert_servers_utilization = round(((sum(total_expert_servers_utilization) / len(total_expert_servers_utilization)) * 100), 2)
rookie_servers_utilization = round(((sum(total_rookie_servers_utilization) / len(total_rookie_servers_utilization)) * 100), 2)
technical_servers_utilization = round(((sum(total_technical_servers_utilization) / len(total_technical_servers_utilization)) * 100), 2)

average_got_tired_users_in_shift_1 = round((sum(total_average_number_of_got_tired_users_shift_1) / len(total_average_number_of_got_tired_users_shift_1)), 2)
average_got_tired_users_in_shift_2 = round((sum(total_average_number_of_got_tired_users_shift_2) / len(total_average_number_of_got_tired_users_shift_2)), 2)
average_got_tired_users_in_shift_3 = round((sum(total_average_number_of_got_tired_users_shift_3) / len(total_average_number_of_got_tired_users_shift_3)), 2)
number_of_max_got_tired_shift = max(average_got_tired_users_in_shift_1, average_got_tired_users_in_shift_2, average_got_tired_users_in_shift_3)
if number_of_max_got_tired_shift == average_got_tired_users_in_shift_1:
    max_got_tired_shift = 'first'
elif number_of_max_got_tired_shift == average_got_tired_users_in_shift_2:
    max_got_tired_shift = 'second'
elif number_of_max_got_tired_shift == average_got_tired_users_in_shift_3:
    max_got_tired_shift = 'third'
    
got_tired_waiting_time = round((sum(total_got_tired_waiting_time) / len(total_got_tired_waiting_time)), 2)

print(f'Average time VIP users spend in system is {VIP_users_average_time_in_system} minutes')

print(f'{percentage_of_VIP_users_without_waiting}% of VIP users, never wait in queues')

print(f'Maximum length of normal users in normal queue is {Max_NormalUsers_NormalQueue_Length}')
print(f'Maximum length of VIP users in normal queue is {Max_VIPUsers_NormalQueue_Length}')
print(f'Maximum length of normal users in re-call queue is {Max_NormalUsers_RecallQueue_Length}')
print(f'Maximum length of VIP users in re-call queue is {Max_VIPUsers_RecallQueue_Length}')
print(f'Maximum length of normal users in technical queue is {Max_NormalUsers_TechnicalQueue_Length}')
print(f'Maximum length of VIP users in technical queue is {Max_VIPUsers_TechnicalQueue_Length}')

print(f'Average length of normal users in normal queue is {Average_NormalUsers_NormalQueue_Length}')
print(f'Average length of VIP users in normal queue is {Average_VIPUsers_NormalQueue_Length}')
print(f'Average length of normal users in re-call queue is {Average_NormalUsers_RecallQueue_Length}')
print(f'Average length of VIP users in re-call queue is {Average_VIPUsers_RecallQueue_Length}')
print(f'Average length of normal users in technical queue is {Average_NormalUsers_TechnicalQueue_Length}')
print(f'Average length of VIP users in technical queue is {Average_VIPUsers_TechnicalQueue_Length}')

print(f"Normal users' maximum waiting time in normal queue is {Max_NormalUsers_NormalQueue_Waiting_Time} minutes")
print(f"VIP users' maximum waiting time in normal queue is {Max_VIPUsers_NormalQueue_Waiting_Time} minutes")
print(f"Normal users' maximum waiting time in re-call queue is {Max_NormalUsers_RecallQueue_Waiting_Time} minutes")
print(f"VIP users' maximum waiting time in re-call queue is {Max_VIPUsers_RecallQueue_Waiting_Time} minutes")
print(f"Normal users' maximum waiting time in technical queue is {Max_NormalUsers_TechnicalQueue_Waiting_Time} minutes")
print(f"VIP users' maximum waiting time in technical queue is {Max_VIPUsers_TechnicalQueue_Waiting_Time} minutes")

print(f"Normal users' average waiting time in normal queue is {Average_NormalUsers_NormalQueue_Waiting_Time} minutes")
print(f"VIP users' average waiting time in normal queue is {Average_VIPUsers_NormalQueue_Waiting_Time} minutes")
print(f"Normal users' average waiting time in re-call queue is {Average_NormalUsers_RecallQueue_Waiting_Time} minutes")
print(f"VIP users' average waiting time in re-call queue is {Average_VIPUsers_RecallQueue_Waiting_Time} minutes")
print(f"Normal users' average waiting time in technical queue is {Average_NormalUsers_TechnicalQueue_Waiting_Time} minutes")
print(f"VIP users' average waiting time in technical queue is {Average_VIPUsers_TechnicalQueue_Waiting_Time} minutes")

print(f"Expert server's average utilization is {expert_servers_utilization}%")
print(f"Rookie server's average utilization is {rookie_servers_utilization}%")
print(f"Technical server's average utilization is {technical_servers_utilization}%")

print(f'Users on average got tired and left the queue in {max_got_tired_shift} shift, more than the other shifts')

print(f'The users who got tired, have waited {got_tired_waiting_time} minutes on average till leaving')

# Used to collect data of all times we run the code, in order to calculate confidence intervals
#standard_list = list()
#standard_list.append([VIP_users_average_time_in_system, percentage_of_VIP_users_without_waiting, Max_NormalUsers_NormalQueue_Length, Max_VIPUsers_NormalQueue_Length,
#                    Max_NormalUsers_RecallQueue_Length, Max_VIPUsers_RecallQueue_Length, Max_NormalUsers_TechnicalQueue_Length, Max_VIPUsers_TechnicalQueue_Length, Average_NormalUsers_NormalQueue_Length,
#                    Average_VIPUsers_NormalQueue_Length, Average_NormalUsers_RecallQueue_Length, Average_VIPUsers_RecallQueue_Length, Average_NormalUsers_TechnicalQueue_Length, Average_VIPUsers_TechnicalQueue_Length,
#                    Max_NormalUsers_NormalQueue_Waiting_Time, Max_VIPUsers_NormalQueue_Waiting_Time, Max_NormalUsers_RecallQueue_Waiting_Time, Max_VIPUsers_RecallQueue_Waiting_Time,
#                    Max_NormalUsers_TechnicalQueue_Waiting_Time, Max_VIPUsers_TechnicalQueue_Waiting_Time, Average_NormalUsers_NormalQueue_Waiting_Time, Average_VIPUsers_NormalQueue_Waiting_Time,
#                    Average_NormalUsers_RecallQueue_Waiting_Time, Average_VIPUsers_RecallQueue_Waiting_Time, Average_NormalUsers_TechnicalQueue_Waiting_Time, Average_VIPUsers_TechnicalQueue_Waiting_Time,
#                    expert_servers_utilization, rookie_servers_utilization, technical_servers_utilization, max_got_tired_shift, got_tired_waiting_time])
#final_lists_dataframe = pd.DataFrame(standard_list)
#export_csv = final_lists_dataframe.to_csv(r'D:/Term 6/Fundamentals of Simulation/Project/Codes/100 Replications.csv', index = None, header = True)


    
print('Simulation Ended!\n')
