# Call Center Simulation Project
The purpose of this code is to simulate a casual call center with 
two experts, three amateurs, and two technical servers. we prepared
this for the "Introduction to Simulation" course project; which was 
instructed by Dr. Nafise Sedghi. For this code to be completed we 
also appreciate Mr. Shahmoradi for his constructive and helpful 
advice.

In this simulation, all service times are based on exponential 
distribution, and all inter-arrival times are Poisson distributions 
with different mean parameters. In the presented call center, we
have three subsystems. The first one is when a user calls and with attention
to the fact that the user type (whether he/she is a normal or special
user) and queue are different, one of the experts or amateur servers will serve him/her.
The second subsystem is the call-back mechanism. In a specific condition, the user can 
leave the queue and require a call-back option; this option will make servers call him 
on the 2nd or 3rd shift of the day, whenever they are idle. The third subsystem
is the technical call. when a user ends their call with one of the servers (
expert or amateur) he/she can demand to be connected to technical servers
to solve his/her technical issues.

On a random day of each month, disruption occurs. As a result users inter
arrival times change that should be modeled.

In this phase, we calculate these evaluation criteria:
    1- Average time VIP users spend in the system
    2- Percentage of VIP users that never wait in queues
    3- Maximum and average length and waiting time in each queue, based on user and server type
    4- Each type of servers' utilization
    5- The shift in which more users get tired and leave the queue
    6- Got-tired users' average waiting time till leaving
And then in the second phase, we need to make a statistical comparison between 
two configurations of the system.
