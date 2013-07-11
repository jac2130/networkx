# -*- coding: utf-8 -*-
"""
Hamming Distance between two graphs and related comparisons.
"""
__author__ = "\n".join(['Johannes Castner (jac2130@columbia.edu)',
                        'Aric Hagberg (hagberg@lanl.gov)',
                        'Dan Schult (dschult@colgate.edu)'])
#    Copyright (C) 2004-2013 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

__all__ = ['hamming_distance', 'generalized_hamming_distance', '2d_generalized_hamming_distance',
        'diversity']

def hamming_distance(G, H):
    """Return the Hamming distance between two (possibly directed) graphs.

    The Hamming distance is the number of edges contained in one 
    but not the other graph.

    Parameters
    ----------
    G, H : NetworkX graph/digraph
       The graphs to be compared

    Returns
    -------
    count : integer
      The hamming distance.
    """
    count = 0
    for e in G.edges_iter():
        if not H.has_edge(*e):
            count+=1
    for e in H.edges_iter():
        if not G.has_edge(*e):
            count+=1
    return count


def generalized_hd(G, H, no_edge_cost=0.5):
    '''
    This function computes a generalized Hamming Distance, of a (possibly weighted and directed) graph, where not having a relation
    has a potentially different cost than having a zero relation
    '''
    count=0
    for e in G.edges_iter():
        if H.has_edge(*e):
            try: count+= abs(nx.get_edge_attributes(G, 'weight')[e]-nx.get_edge_attributes(H, 'weight')[e])
            except: print '%s does not have a weight!' % str(e)
        else:
            try: count+= (abs(nx.get_edge_attributes(G, 'weight')[e]) + no_edge_cost)
            except: print '%s does not have a weight!' % str(e)

    #And now for the edges that are in H but not in G:
    for e in H.edges_iter():
        if not G.has_edge(*e):
            try: count+= (abs(nx.get_edge_attributes(H, 'weight')[e]) + no_edge_cost)
            except: print '%s does not have a weight!' % str(e)

    return count

def two_dim_ghd(G, H, no_edge_params=(0, 2)):
    '''
    This function computes a two-dimensional Generalized Hamming Distance,
    where each link has information on two dimensions (here interpreted as a
    mean and a variance).
    '''
    from numpy import sqrt
    count=0
    for e in G.edges_iter():
        if H.has_edge(*e):
            try: count+= sqrt((nx.get_edge_attributes(G, 'mu')[e]-nx.get_edge_attributes(H, 'mu')[e])**2 + (nx.get_edge_attributes(G, 'sigma')[e]-nx.get_edge_attributes(H, 'sigma')[e])**2)


            except: print '%s does not have a mu or a sigma!' % str(e)
        else:
            try: count+= sqrt((nx.get_edge_attributes(G, 'mu')[e]-no_edge_params[0])**2 + (nx.get_edge_attributes(G, 'sigma')[e]-no_edge_params[1])**2)
            except: print '%s does not have a mu or a sigma!' % str(e)

    #And now for the edges that are in H but not in G:
    for e in H.edges_iter():
        if not G.has_edge(*e):
            try: count+= sqrt((nx.get_edge_attributes(H, 'mu')[e]-no_edge_params[0])**2 + (nx.get_edge_attributes(H, 'sigma')[e]-no_edge_params[1])**2)

            except: print '%s does not have a mu or a sigma!' % str(e)

    return count



def diversity(obj_set, distance=generalized_hd):
    '''
    This function calculates the Weitzman diversity measure (Weitzman 1992) of a set of objects with a distance function defined over any
    two objects in the set.
    '''
    S=set()
    divers=0
    g=obj_set.pop() #Step1: randomly pick an object from the object set
    S.add(g)
    while obj_set:
        set_distance=min([distance(g, h) for g in S for h in obj_set])
        min_elem=[elem for elem in obj_set if min([distance(elem, g) for g in S])==set_distance].pop()

        S.add(min_elem) #Step2: add closest member of the object set to the set, S
        obj_set.remove(min_elem) #and remove it from the object set
        divers+=set_distance #Step3: increment the diversity by the distance between the set S, and the new member.

    #Normalize the diversity by the number of objects:
    return float(divers)/len(S)
