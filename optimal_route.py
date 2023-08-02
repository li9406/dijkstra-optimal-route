
def optimalRoute(start, end, passengers, roads):
    """
    Find the optimal route from the given departure location to the destination
    location with the minimum total travel time using dijkstra

    Approach Description:
    To obtain the optimal route, one approach is to use a layered graph. There 
    will be 2 layers: first layer contains non-carpool lanes, and the second 
    layer contains carpool lanes. 

    At the start, we will be driving on the first layer because there is no
    potential passenger at the departure location. When we pick up a
    passenger, we will enter the second layer because we want to reach the
    destination location as fast as possible and carpool lanes have less or
    equal travel time as non-carpool lanes.

    To create the layered graph, we would need preprocess the roads before
    running Dijkstra algorithm. We would need to break down the road 
    (a,b,c,d) to (a1,b1,c) and (a2,b2,d). The first layer will contain a list
    of (a1,b1,c) and the second one will contain a list of (a2,b2,d).

    In order to enter the second layer from the first layer, we need to add an 
    edge that connect first layer to second layer, i.e. (a1,b2,d). a1 is a 
    location in first layer that has potential passengers and b2 is a location 
    in second layer that is an adjacent location of a1, i.e. there is an edge
    from a to b.
    
    Using this approach, we would only need to do preprocessing the inputs and 
    would not need to modify Dijkstra algorithm or Graph class. 
    
    :Input:
        start: the departure location
        end: the destination location
        passengers: a list of locations where there are passengers
        roads: a list of tuples (a,b,c,d) where a is the starting location, 
               b is the ending location, c is the travel time if alone, and
               d is the travel time if not alone
    
    :Output/return: a list that represents the optimal route from the departure
                    location to the destination location with the minimum total
                    travel time

    :Time complexity: O(|R|) + O(|L| log |L|) + O(|R| log |L|) + O(|R|) +
                      O(|R| + |L|) + O(|R| log |L|) + O(|R|) + O(log|R) 
                      = O(|R| log |L|) 
                      where |R| is the number of roads 
                      and |L| is the number of locations
                      because |R| = |L|^2 for dense graph, |R| = |L|-1 for
                      sparse graph and |P| <= |L|-2
    :Aux space complexity: O(|L| + |R|)
    """
    # find the total number of locations
    # O(|R|) time
    # O(1) aux space
    max_id = roads[0][0]
    for i in range(len(roads)):
        if roads[i][0] > max_id:
            max_id = roads[i][0]
        if roads[i][1] > max_id:
            max_id = roads[i][1]

    total_locations = max_id + 1

    # sort passengers in order to perform binary search
    # O(|L| log |L|) time because |P| <= |L|-2 
    # O(|L|) aux space because |P| <= |L|-2
    passengers.sort()

    # preprocess rooads 
    preprocessed_roads = []

    # connect a location to layer 2 if the location has passengers 
    # O(|R| log |L|) time because |P| <= |L|-2
    has_connection = False
    for road in roads:
        if binarySearch(passengers, road[0]) != -1:   # O(log |P|)
            preprocessed_roads.append((road[0], road[1]+total_locations, road[3]))
            has_connection = True

    # if there are no potential passengers looking for a ride,
    # create a graph with non-carpool lanes only
    # O(|R|) time
    if len(passengers) == 0 or has_connection == False:
        for road in roads:      # (a,b,c,d)
            road_alone = (road[0], road[1], road[2])    # (a,b,c)
            preprocessed_roads.append(road_alone)

    # if there are potential passengers looking for a ride, 
    # create a layered graph
    # O(|R|) time
    elif len(passengers) > 0 and has_connection == True:
        for road in roads:      # (a,b,c,d)
            road_alone = (road[0], road[1], road[2])    # (a,b,c)
            preprocessed_roads.append(road_alone)
            road_carpool = (road[0]+total_locations, road[1]+total_locations, 
                            road[3])                    # (a,b,d)
            preprocessed_roads.append(road_carpool)

    # create graph
    # O(|L| + |R|) time because
    # O(|L| + |R|) aux space
    graph = RouteGraph(preprocessed_roads)
    
    # run dijkstra
    # O(|R| log |L|) time
    # O(|L|) aux space
    graph.dijkstra(start)

    # return optimal route
    shortest_route = [end]

    if len(passengers) == 0 or has_connection == False:
        current = end
    
    # for layered graph, we would have the vertex destination1 in layer 1
    # and destination2 in layer 2, it is better to check which of these
    # two nodes has the least distance
    else:
        if graph.vertices[end].distance \
            <= graph.vertices[end+total_locations].distance:
            current = end
        else:
            current = end + total_locations

    # backtrack to obtain the optimal route
    # starting from the destination location
    # O(|R|) time
    while current != start:
        current = graph.vertices[current].previous.id
        if current > total_locations -1: # for layered graph, we have a1 and a2
            shortest_route.append(current-total_locations) # append a
        else:
            shortest_route.append(current)

    # reverse the list because it start from the destination location
    # O(log |R|) time
    for i in range(len(shortest_route)//2):
        shortest_route[i], shortest_route[len(shortest_route)-i-1] = \
            shortest_route[len(shortest_route)-i-1], shortest_route[i]

    return shortest_route    

def binarySearch(list, target):
    """
    Find the target integer in a sorted list of integers using divide and 
    conquer

    I have referred to the implementation of binary search from FIT1045 
    Lecture 12. 

    :Input:
        list: a list of integers that is sorted
        target: an integer that we want to find 
    
    :Output/return: an integer that represents the index of the target in the 
                    list. If the target is not in the list, it will return -1

    :Time complexity: O(log N) where N is the length of the list
    :Aux space complexity: O(1)
    """
    left = 0
    right = len(list) - 1

    while left <= right:
        mid = (left + right) // 2

        if list[mid] == target:
            return mid

        elif list[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return -1 

"""
A class represents a graph

I have referred to the implementation of Graph class shown in the recording
Lecture04 P1 Graph BFS DFS Lecture05 P1 Dijkstra
"""
class RouteGraph:
    def __init__(self, roads):
        """
        Create a Graph object based on the given roads.

        I have used adjacency list instead of adjacency matrix. This is because
        we cannot assume that the graph is always dense based on the assignment
        specification, and adjacency matrix is faster when the graph is dense
        compared to when it is sparse. 

        :Input:
            self: a reference to the Vertex object
            roads: a list of tuples (u,w,v) where u is the starting location, 
                   v is the ending location, w is the travel time from u to v
    
        :Output/Return: -

        :Time complexity: O(2|L| + 2|R|) = O(|L| + |R|)
        :Aux space complexity: O(|L| + |R|) because a list of size |L| is 
                               created to store the vertices and each vertex
                               has at most |R| edges
        """
        # find the number of locations, |L|
        # which is the number of vertices in the graph
        # O(|R|) time
        max_id = roads[0][0]
        for i in range(len(roads)):
            if roads[i][0] > max_id:
                max_id = roads[i][0]
            if roads[i][1] > max_id:
                max_id = roads[i][1]

        total_vertices = max_id + 1

        # create an adjacency list
        # O(|L|) aux space
        self.vertices = [None] * total_vertices
        
        # add vertices to the graph
        # O(|L|) time
        for i in range(total_vertices):
            self.vertices[i] = Vertex(i)

        # add edges to the graph
        # O(|R|) time
        for road in roads:
            u = road[0]
            v = road[1]
            w = road[2]
            
            edge = Edge(u,v,w)
            self.vertices[u].add_edge(edge)

    def dijkstra(self, source):
        """
        Find the shortest path from the departure location to all other 
        vertices

        I have referred to the implementation of Dijkstra algorithm shown in 
        the recording Lecture04 P1 Graph BFS DFS Lecture05 P1 Dijkstra

        :Input:
            self: a reference to the Vertex object
            source: an integer that represents the departure location

        :Output/Return: -

        :Time complexity: O(|R| log |L|)
        :Aux space complexity: O(|L|)
        """
        # find number of vertices
        total_vertices = len(self.vertices)
        
        # initialzie heap of size total_vertices
        heap = MinHeap(total_vertices + 1)
        
        # add source to heap 
        source = self.vertices[source]
        source.distance = 0
        heap.add((source.id, 0))

        while heap.length > 0:
            element = heap.serve()      # element in heap is (vertex id, distance)
            
            # get vertex by vertex id
            u = self.vertices[element[0]]
            u.visited = True

            # for every adjacent vertices of u
            for edge in u.edges:
                v = edge.v
                v = self.vertices[v]

                if v.discovered == False:
                    v.discovered = True
                    v.distance = u.distance + edge.w
                    v.previous = u
                    heap.add((v.id, v.distance))

                elif v.visited == False:
                    if v.distance > u.distance + edge.w:
                        v.distance = u.distance + edge.w
                        v.previous = u
                        heap.update(v.id, v.distance)

    def __str__(self):
        """
        Display the graph

        :Input:
            self: a reference to the Vertex object
        
        :Output/Return: a string containing all the vertices and edges in the 
                        graph

        :Time complexity: O(|L|) because there are |L| vertices
        :Aux space complexity: O(1)
        """
        return_string = ""
        for vertex in self.vertices:
            return_string = return_string + "Vertex " + str(vertex) + "\n"
        return return_string

"""
A class represents a vertex in a graph

I have referred to the implementation of Vertex class shown in the recording
Lecture04 P1 Graph BFS DFS Lecture05 P1 Dijkstra
"""
class Vertex:
    def __init__(self, id):
        """
        Create a new Vertex object

        :Input:
            self: a reference to the Vertex object
            id: an unique identifier for the Vertex object

        :Output/Return: -

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        self.id = id
        self.edges = []
        self.distance = 0
        self.previous = None
        self.visited = False
        self.discovered = False

    def add_edge(self, new_edge):
        """
        Add a edge from a Vertex to its adjacent vertex
        
        :Input:
            self: a reference to the Vertex object

        :Output/return: -

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        self.edges.append(new_edge)

    def check_visited(self):
        """
        Check whether a Vertex is visited or not

        :Input:
            self: a reference to the Vertex object

        :Output/return: a boolean, True if visited, False otherwise

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        return self.visited == True

    def check_discovered(self):
        """
        Check whether a Vertex is discovered or not

        :Input:
            self: a reference to the Vertex object

        :Output/return: a boolean, True if discovered, False otherwise

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        return self.discovered == True

    def __str__(self):
        """
        Display the vertex

        :Input:
            self: a reference to the Vertex object

        :Output/return: a string containing the id of the Vertex and its 
                        adjacent vertices

        :Time complexity: O(|R|) because a Vertex can have at most |R| edges
        :Aux space complexity: O(1)
        """
        output_string = str(self.id) + "\n"
        if len(self.edges) > 0:
            for edge in self.edges:
                output_string += str(edge) + "\n"
        return output_string

"""
A class represents an edge in a graph 

I have referred to the implementation of Edge class shown in the recording
Lecture04 P1 Graph BFS DFS Lecture05 P1 Dijkstra
"""
class Edge:
    def __init__(self, u, v, w):
        """
        Create a new Edge object

        :Input:
            self: a reference to the Edge object
            u: the starting location of the road
            v: the ending location of the road
            w: the travel time from u to v

        :Output/Return: -

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        """
        Display the edge

        :Input:
            self: a reference to the Edge object

        :Output/return: a string containing the starting and ending location of
                        the road and the travel time

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        return "Location " + str(self.u) + " to " + str(self.v) + " with " \
                + str(self.w) + " minutes"

"""
A class represents a heap implemented using array

I have used the implementation of Heap class from FIT1008. I have made some 
modifications to implement the Heap class as a min heap instead of a max heap.
"""
class MinHeap:
    
    def __init__(self, max_size):
        """
        Create a new MinHeap object

        Instead of using array of referential, I have initialized the_array 
        using Python list. I have added an index array to store the position
        of an element in the heap. 

        :Input:
            self: a reference to the MinHeap object
            max_size: an integer that represent the size of the heap

        :Output/Return: -

        :Time complexity: O(N)
        :Aux space complexity: O(N) where N is the size of the heap
        """
        self.length = 0
        self.the_array = [None] * max_size
        self.index_array = [None] * max_size

    def __len__(self):
        """
        Get the length of the heap

        :Input:
            self: a reference to the MinHeap object
        
        :Output/Return: an integer that represent the length of the heap

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        return self.length

    def is_full(self):
        """
        Check if the heap is full

        :Input:
            self: a reference to the MinHeap object
        
        :Output/Return: a boolean. True if the the heap is full, False 
                        otherwise

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        return self.length + 1 == len(self.the_array)

    def add(self, element):
        """
        Add an element to the heap

        I have modified the add() function from Heap class from FIT1008. When
        an element is added to the heap, I have also added the position of 
        element into the index array. 
        
        :Input:
            self: a reference to the MinHeap object
            element: a tuple (id, value) 
        
        :Output/Return: -

        :Time complexity: O(log N) 
        :Aux space complexity: O(1)
        """
        has_space_left = not self.is_full()

        if has_space_left:
            self.length += 1
            self.the_array[self.length] = element
            self.index_array[element[0]] = self.length 
            self.rise(self.length)

        return has_space_left

    def rise(self, k):
        """
        Rise element at index k to its correct position

        :Input:
            self: a reference to the MinHeap object
            k: the index of the element to be rise
        
        :Output/Return: -

        :Time complexity: O(log N)
        :Aux space complexity: O(1)
        """
        while k > 1 and self.the_array[k][1] < self.the_array[k // 2][1]:
            self.swap(k, k // 2)
            k = k // 2

    def smallest_child(self, k):
        """
        Get the index of the smallest child of an element at index k

        I have modified the largest_child() function from Heap class from 
        FIT1008 to make it return the smallest child instead of the largest
        child.
        
        :Input:
            self: a reference to the MinHeap object
            k: an integer that represents the index of the element

        :Output/Return: index of the left child if the left child is smaller 
                        than the right child

        :Time complexity: O(1)
        :Aux space complexity: O(1) 
        """
        if 2 * k == self.length or \
            self.the_array[2 * k][1] < self.the_array[2 * k + 1][1]:
            return 2*k
        else:
            return 2*k+1
        
    def sink(self, k):
        """
        Make the element at index k sink to correct position

        :Input:
            self: a reference to the MinHeap object
            k: an integer that represents the index of an element
            
        :Output/Return: -

        :Time complexity: O(log N) 
        :Aux space complexity: O(1)
        """
        while 2*k <= self.length:
            child = self.smallest_child(k)
            if self.the_array[k][1] <= self.the_array[child][1]:
                break

            self.swap(child, k)
            k = child

    def swap(self, i, j):
        """
        Swap the element at index i with element at index j

        :Input:
            self: a reference to the MinHeap object
            i: an integer that represents an index of the first element
            j: an integer that represents an index of the second element

        :Output/Return: -

        :Time complexity: O(1) 
        :Aux space complexity: O(1)
        """
        self.index_array[self.the_array[i][0]], \
            self.index_array[self.the_array[j][0]] = \
            j, i
        
        self.the_array[i], self.the_array[j] = \
            self.the_array[j], self.the_array[i]

    def serve(self):
        """
        Remove the root element from the heap

        :Input:
            self: a reference to the MinHeap object

        :Output/Return: the element being served

        :Time complexity: O(log N) 
        :Aux space complexity: O(1)
        """
        # get the root element
        element = self.the_array[1]

        # replace the root element with the last element in the heap
        self.the_array[1] = self.the_array[self.length]

        # reduce the length of the heap by 1
        self.the_array[self.length] = None
        self.index_array[element[0]] = None
        self.length -= 1
        
        # sink new root element to correct position
        self.sink(1)
        
        return element
    
    def update(self, element_id, new_value):
        """
        Change the value of an element in the heap

        :Input:
            self: a reference to the MinHeap object
            element_id: the id of the element to be update
            new_value: the new value of the element

        :Output/Return: -

        :Time complexity: O(log N) 
        :Aux space complexity: O(1)
        """
        # change value of the element
        element_length = self.index_array[element_id]
        self.the_array[element_length] = (element_id, new_value)
        
        # rise the element with new value to correct position
        self.rise(element_length)
