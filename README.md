# Optimal Route

As a smart student you are always trying to optimise the driving time to your early morning
algorithms lectures so that you can sleep more. You will be leveraging your algorithms skills
to get an optimal solution.

Some of the roads in your city have carpool lanes that can only be used if there are at least 2
persons in the car, so you have to decide if you will be giving a ride to a fellow student or not.
You have access to precise travel time information among key locations in your city, both with
single car occupancy and with 2 or more persons in the car. And you have a list of locations
in which there are students looking for a ride to the same destination you are going. You can
assume that the potential passengers are always on time at the agreed location and there will
be no additional time incurred for getting them into the car. You will either pickup passenger(s) with the same destination as you, or go alone the whole trip. Your absolute priority
during those very early morning hours is maximising your sleeping time, so you are looking
for the shortest total driving time and will not give a ride if that increases the total driving time.

You are a law-abiding citizen and would never drive in a carpool lane while you
are alone in the car!

There are |L| key location points represented by 0, 1, . . . , |L| − 1. Your algorithm will take as
input the following: a departure location start ∈ {0, 1, . . . , |L| − 1}, a destination location
end ∈ {0, 1, . . . , |L| − 1}, a list passengers of locations where there are potential passengers,
and a list of roads roads with the corresponding travel times. passengers is a list of integers
such that each integer i in it is such that i ∈ {0, 1, . . . , |L| − 1} and indicates that there are
potential passengers at location i looking for a ride to your destination. The list of roads roads
is represented as a list of tuples (a, b, c, d) where:
* a ∈ {0, 1, . . . , |L| − 1} is the starting location of the road.
* b ∈ {0, 1, . . . , |L| − 1} is the ending location of the road.
* c is a positive integer representing how many minutes you would spend to drive from a
to b on that road if you are alone in the car.
* d is a positive integer representing how many minutes you would spend to drive from a
to b on that road if you are there are 2 or more persons in the car.

Regarding those inputs:
* For any tuple in (a, b, c, d) in roads, you can assume that d ≤ c (as you can still use
the non-carpool lanes when there are passengers in the car). For some tuple (a, b, c, d), it
might be the case that c = d (as some roads might not have carpool lanes, or the carpools
lanes might not be improving the actual travel time on that road).
* You can assume that no roads will have only carpool lanes. I.e., if there is a road from a
to b, it will always be possible to travel on it even if you are alone in the car. Therefore
for any tuple (a, b, c, d) in roads the values c and d are well-defined.
* You can assume that for every location {0, 1, . . . , |L| − 1} there is at least one road that
begins of finishes there.
* You can assume that there is a route to go from start to end and that start = end.
* The locations specified by start and end will not have potential passengers.
* You cannot assume that the list passengers is given to you in any specific order, but
you can assume that there will be no repeated integers in passengers.
* You cannot assume that the list of tuples in roads are given to you in any specific order.
* You cannot assume that the roads are 2-way roads.
* The set of locations P specified in passengers can constitute any subset of {0, 1, . . . , |L|−
1} \ {start, end}, therefore you can neither assume |P| is a constant nor assume that
P = Θ(|L|).
* The number of roads |R| might be significantly less than |L|^2, therefore you should not assume that |R| = Θ(|L|^2).

You should implement a function optimalRoute(start, end, passengers, roads) that returns one optimal route to go from start to end with the minimum possible total travel time.
Your function should return the optimal route as a list of integers. If there are multiple route
achieving the optimal time, you can return any one of them.

## Complexity
Given an input with |L| key locations and |R| roads, your solution should have time complexity
O(|R| log |L|) and auxiliary space complexity O(|L| + |R|).

Note that the number |P| of locations where there are potential passengers looking for a ride
to your destination is not stated in the complexity. If your algorithm has time complexity
Ω(|P||R| log |L|), you will be losing a very significant amount of marks for this question.
