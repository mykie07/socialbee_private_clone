# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 10:10:06 2016

@author: Laura Drummer
"""
import networkx as nx
import pandas as pd
import config
from network_builder import get_max_AR_pairs


def get_graph_data(graph):
    """Given a networkx graph, calucluates the average degree and density.

    Keyword arguments:
    graph -- networkx diGraph
    """
    N, K = graph.order(), graph.size()
    avg_deg = float(K) / N
    density = float(K) / (N * (N - 1))
    return(N, K, avg_deg, density)


def global_writer(topic_words,
                  graph,
                  nx_topic_dictionary,
                  may_know_dict):
    """Given SocialBee generated network information, outputs a Global Report.

    Keyword arguments:
    topic_words -- Top 20 word for all n topics generated by SocialBee
    graph -- Global Network Graph generated by SocialBee
    nx_topic_dictionary -- Dictionary where n keys are topic titles and n
                           values is a list of edges for that network.
    may_know_dict -- dictionary for all predicted "may_know" relationships
                     based on topics
    """
    GN, GK, Gavg_deg, Gdensity = get_graph_data(graph)
    with open("GLOBAL_INFO.txt", "w") as gf:
        # Traditional Network Information
        print("===Global Network Report===", file=gf)
        print("Source: {}".format(config.data_path), file=gf)
        print("===Basic Graph Information===", file=gf)
        print("\tNodes: {}".format(GN), file=gf)
        print("\tEdges: {}".format(GK), file=gf)
        print("\tAverage degree: {}".format(Gavg_deg), file=gf)
        print("\tDensity: {}".format(Gdensity), file=gf)
        print("The following topics were extracted from the data:", file=gf)
        # Summary of each n topic generated
        for topic in topic_words:
            n = topic_words.index(topic)
            TN, TK, Tavg_deg, Tdensity = get_graph_data(nx_topic_dictionary[n])
            print("==Topic {}==".format(n), file=gf)
            print("Words:", ",".join(topic), file=gf)
            print("\t===Topic {} Graph Information===".format(n), file=gf)
            print("\tNodes: {}".format(TN), file=gf)
            print("\tEdges: {}".format(TK), file=gf)
            print("\tAverage degree: {}".format(Tavg_deg), file=gf)
            print("\tDensity: {}".format(Tdensity), file=gf)
        print("===Potential Hidden Relationships===", file=gf)
        # All May-Know relationships
        may_know_df = pd.DataFrame(may_know_dict)
        print(may_know_df.to_string(index=False), file=gf)


def network_report(topic, graph, users, fn, node_df, words):
    """Given SocialBee generated information, outputs a topic-specific report.

    Keyword arguments:
    topic -- Topic Number correlating to key in nx_topic_dictionary structure
    graph -- DiGraph of topic-specific network, value in nx_topic_dictionary
    users -- List of interesting users - specified in config file
    fn -- File name specifying where to output the report
    node_df -- DataFrame containing network specific information about users
    words -- Top twenty words corresponding to specifying topic
    """
    N, K, avg_deg, density = get_graph_data(graph)
    # Traditional Network Information
    with open(fn, "w") as f:
        print("Topic {}".format(topic), file=f)
        print("Words: " + "  ".join(words), file=f)
        print("===Basic Graph Information===", file=f)
        print("\tNodes: {}".format(N), file=f)
        print("\tEdges: {}".format(K), file=f)
        print("\tAverage degree: {}".format(avg_deg), file=f)
        print("\tDensity: {}".format(density), file=f)
        # Summary of top three author recipient pairs
        print("===Top 3 Author/Recipient Pairs for Topic", file=f)
        max_pairs = get_max_AR_pairs(graph)
        for pair in max_pairs:
            print(str(pair[0][0]) + '-----' +
                  str(pair[0][1]) + "\t" + str(pair[1]), file=f)
        print("===Network Data for Selected Users===", file=f)
        print(node_df.to_string(na_rep='0', index=False), file=f)
