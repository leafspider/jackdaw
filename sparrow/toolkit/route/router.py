import osmnx as ox
import networkx as nx
from networkx.readwrite import json_graph
import os, json
from shapely.geometry import shape, LineString


class Router():

    def __init__(self, origin_address, dist=10000, network_type='bike', max_journey_time=20):

        self.folder = os.getcwd() + '/data/route/'
        self.graph_file = self.folder + "graph.json"
        self.route_file = self.folder + "route.png"

        self.network_type = network_type
        self.origin_point = self.address_to_point(origin_address)
        self.hood_graph = self.graph(dist, self.origin_point, network_type)
        self.max_journey_time = max_journey_time

    def graph(self, origin_point, dist, network_type):
        if os.path.exists(self.graph_file):
            hood_graph = self.load_graph(self.graph_file)
        else:
            hood_graph = ox.graph_from_point(origin_point, dist=dist, network_type=network_type)
            self.save_graph(self.hood_graph, self.graph_file)
        return hood_graph

    def address_to_point(self, address):
        return ox.geocode(address)

    def distance_and_time(self, origin_point, destination_point):
        origin_node = ox.nearest_nodes(self.hood_graph, origin_point[1], origin_point[0])
        destination_node = ox.nearest_nodes(self.hood_graph, destination_point[1], destination_point[0])
        shortest_path_length = nx.shortest_path_length(self.hood_graph, origin_node, destination_node, weight='length')
        
        distance_km = shortest_path_length / 1000
    
        if self.network_type == "drive":
            average_speed_m_per_s = 3.95
        elif self.network_type == "bike":
            average_speed_m_per_s = 3.35
        elif self.network_type == "walk":
            average_speed_m_per_s = 1.39

        time_seconds = shortest_path_length / average_speed_m_per_s
        time_mins = time_seconds / 60

        return distance_km, time_mins

    def travel_time(self, origin_point, destination_point):
        origin_node = ox.nearest_nodes(self.hood_graph, origin_point[1], origin_point[0])
        destination_node = ox.nearest_nodes(self.hood_graph, destination_point[1], destination_point[0])
        shortest_path_length = nx.shortest_path_length(self.hood_graph, origin_node, destination_node, weight='length')
    
        if self.network_type == "drive":
            average_speed_m_per_s = 3.95
        elif self.network_type == "bike":
            average_speed_m_per_s = 3.35
        elif self.network_type == "walk":
            average_speed_m_per_s = 1.39

        time_seconds = shortest_path_length / average_speed_m_per_s
        time_mins = time_seconds / 60

        return time_mins

    def route(self, origin_point, destination_point):
        origin_node = ox.nearest_nodes(self.hood_graph, origin_point[1], origin_point[0])
        destination_node = ox.nearest_nodes(self.hood_graph, destination_point[1], destination_point[0])
        return nx.shortest_path(self.hood_graph, origin_node, destination_node, weight='length')

    def map(self, route):
        fig, ax = ox.plot_graph_route(self.hood_graph, route)
        return fig, ax

    class LineStringEncoder(json.JSONEncoder):
        def default(self, obj):
            return obj.__geo_interface__

    def lineString_decoder(obj):
        if 'type' in obj and 'coordinates' in obj:
            return LineString(obj['coordinates'])
        return obj

    def save_graph(self, filename):

        # data = {
        #     "nodes": [{**{"id": n}, **G.nodes[n]} for n in G.nodes],
        #     "edges": [
        #         {
        #             "source": u,
        #             "target": v,
        #             "key": k,
        #             **d
        #         }
        #         for u, v, k, d in G.edges(keys=True, data=True)
        #     ],
        #     "graph": dict(G.graph)
        # }
                                    
        for u, v, k, data in self.hood_graph.edges(keys=True, data=True):
            if 'geometry' in data:
                data['geometry'] = data['geometry'].__geo_interface__

        data = json_graph.node_link_data(self.hood_graph)
        
        with open(filename, 'w') as f:
            # json.dump(data, f, indent=2, default=lambda o: o.__geo_interface__)
            json.dump(data, f, indent=2, cls=self.LineStringEncoder)

    def load_graph(self, filename):

        # with open( filename, "r") as f:
        #   data = json.load(f, object_hook=lineString_decoder)
        with open(filename, 'r') as f:
            data = json.load(f)

        the_graph = json_graph.node_link_graph(data, directed=True, multigraph=True, edges="links")

        for u, v, k, data in the_graph.edges(keys=True, data=True):
            if 'geometry' in data and isinstance(data['geometry'], dict):
                data['geometry'] = shape(data['geometry'])

        return the_graph

    def save_route(self, origin_point, destination_point):
        
        self.route_nodes = self.route( origin_point, destination_point )
        fig, ax = self.map( self.route_nodes)
        fig.savefig( self.folder + "route_map.png")


if __name__ == '__main__':

    pass

    # folder = os.getcwd() + '/data/routes/'

    # origin_address = "64 Mavety St, Toronto, ON"

    # origin_point = address_to_point(origin_address)

    # filename = folder + "graph.json"

    # if not os.path.exists(filename):
    #     hood_graph = graph(origin_point)
    #     save_graph(hood_graph, filename)
    # else:
    #     hood_graph = load_graph(filename)

    # destination_address = "23 Glenlake Ave, Toronto, ON"
    # # destination_address = "1246 Yonge St, Toronto, ON"
    # destination_point = address_to_point(destination_address)
    # # # print(f"Origin: {origin_point}", f"Destination: {destination_point}")

    # distance = distance( hood_graph, origin_point, destination_point )
    # print(f"Distance: {distance:.3f} km")

    # bike_time = travel_time( hood_graph, origin_point, destination_point, "bike" )
    # print(f"Bike: {bike_time:.3f} min")

    # # drive_time = travel_time( hood_graph, origin_point, destination_point, "drive" )
    # # print(f"Drive: {drive_time:.3f} min")

    # # walk_time = travel_time( hood_graph, origin_point, destination_point, "walk" )
    # # print(f"Walk: {walk_time:.3f} min")

    # route_nodes = route( hood_graph, origin_point, destination_point )
    # # print(f"Route nodes: {route_nodes}")

    # fig, ax = map( hood_graph, route_nodes)
    # fig.savefig( folder + "route_map.png")
