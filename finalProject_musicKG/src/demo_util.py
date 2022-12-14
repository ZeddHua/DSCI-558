from yfiles_jupyter_graphs import GraphWidget
from neo4j import GraphDatabase
import pandas as pd
import numpy as np

def get_data(driver, query):
    with driver.session() as session:
        res = session.run(query).graph()
    return res

def Draw_Graph(graph_obj):
    styles = {
        "Artist": {"color":"red", "shape":"ellipse", "label":"name"},
        "Band": {"color":"orange", "shape":"ellipse", "label":"name"},
        "Genre": {"color":"blue", "shape":"octagon", "label":"name"},
        "Song": {"color":"green", "shape":"rectangle", "label":"name"}
    }
    w = GraphWidget(graph = graph_obj)
    w.set_edge_color_mapping(lambda index, edge : "orange" if edge["properties"]["label"] in ["PERFORMED_BY", 'COMPOSED_BY'] else "black")
    w.set_node_styles_mapping(lambda index, node : styles.get(node["properties"]["label"], {}))
    w.set_node_color_mapping(lambda index, node: styles.get(node["properties"]["label"])["color"])
    w.set_node_label_mapping(lambda index, node : node["properties"][styles.get(node["properties"]["label"], {"label":"label"})["label"]])
    return w

def RECOMMEND(driver, song_name):
    
    def vectorize(song_uri):
        data = driver.session().run("Match (s:Song) WHERE s.uri =" + '"' + song_uri + '"' + " Return s LIMIT 1").data()[0]['s']
        return [data['acousticness'], data['valence'], data['danceability'], data['loudness'], data['energy']]
    
    def euclidean_distance(vec1, vec2):
        return sum((vec1-vec2)**2)**0.5
    
    def print_result(song_name, recommend_list):
        print("Recommend similar song to '{}':".format(song_name))
        song_name_list = [*map(lambda x: x['s.name'], driver.session().run("Match (s:Song) WHERE s.uri IN "+str(recommend_list)+" RETURN s.name").data())]
        idx = 0
        for song in song_name_list:
            idx += 1
            print(idx, song)
    
    cluster_df = pd.read_csv('../kg_data/music_kg_blocked.csv')
    cluster_df = cluster_df[cluster_df['node1'].str.contains('https://www.allmusic.com/song')]
    song_uri = driver.session().run("Match (s:Song) WHERE s.name =" + '"' + song_name + '"' + " Return s.uri LIMIT 1").data()[0]['s.uri']
    song_vec = vectorize(song_uri)
    cluster = cluster_df[cluster_df['node1'] == song_uri]['node2'].array
    
    
    if len(cluster):
        same_community = cluster_df[cluster_df['node2'] == cluster[0]]['node1'].array
        vec_list = [*map(lambda x: vectorize(x), same_community)]
        dist_list = [*map(lambda x: (-1) * euclidean_distance(np.array(song_vec), np.array(x)), vec_list)]
        recommend_list = list(same_community[np.argpartition(dist_list, -5)[-5:]])
    
    else:
        same_community = [*map(lambda x: x['s.uri'], driver.session().run("Match (s:Song) RETURN s.uri LIMIT 300").data())]
        vec_list = [*map(lambda x: vectorize(x), same_community)]
        dist_list = [*map(lambda x: (-1) * euclidean_distance(np.array(song_vec), np.array(x)), vec_list)]
        recommend_list = list(np.array(same_community)[np.argpartition(dist_list, -5)[-5:]])
        
    print_result(song_name, recommend_list)
        
    return recommend_list



