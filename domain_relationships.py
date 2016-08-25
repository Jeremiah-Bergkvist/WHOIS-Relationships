#!/usr/bin/env python

# Import graphviz
import sys
from igraph import *
import re
import os

########################################################################
# Import pygraph
########################################################################
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

########################################################################
# Main Program Logic
########################################################################
if __name__ == "__main__":
    email_pattern   = re.compile('([\w\-\.]+\@[\w\-\.]+\.[\w\-\.]+)')
    node_dict       = {}
    domain_dict     = {}
    email_dict      = {}
    email_domains   = []
    emails          = []
    domains         = []
    edge_list       = []
    domain_list     = []
    checked_domains = []
    g               = Graph(0)
    ctr             = 0

    #===================================================================
    # Argument processing
    #===================================================================
    if len(sys.argv) != 3:
        print "Usage: %s [directory] [outfile.gml]" % (sys.argv[0])
        exit(0)

    #===================================================================
    # Pull records for all files in directory
    #===================================================================
    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            filepath = "%s%s" % (subdir, file)
            f=open(filepath, 'r')
            lines = f.readlines()

            #-----------------------------------------------------------
            # Scan each line for unique email addresses
            #-----------------------------------------------------------
            for line in lines:
                line = line.lower()
                    
                for email in email_pattern.findall(line):
                    if email not in emails:
                        emails.append(email)

            #-----------------------------------------------------------
            # Close the open file
            #-----------------------------------------------------------
            f.close()

            #-----------------------------------------------------------
            # Add domain and email to record list
            #-----------------------------------------------------------
            if emails:
                if file not in domains:
                    domains.append(file)
                domain_dict.setdefault(file, emails)
                emails = []

    #===================================================================
    # Build a dict for unique emails
    #===================================================================
    for domain in domain_dict:
        for domain_email in domain_dict[domain]:
            #-----------------------------------------------------------
            # Unique email, add it
            #-----------------------------------------------------------
            if domain_email not in emails:
                emails.append(domain_email)
    for email in emails:
        #---------------------------------------------------------------
        # Go through all domains searching for current email
        #---------------------------------------------------------------
        for domain in domain_dict:
            for domain_email in domain_dict[domain]:        
                if email == domain_email:
                    domain = domain.lower()
                    email_domains.append(domain)
                    break;

        #---------------------------------------------------------------
        # Add email and associated domains to record list
        #---------------------------------------------------------------
        if email_domains:
            email_dict.setdefault(email, email_domains)
            email_domains = []

    #===================================================================
    # Build vertices list
    #===================================================================
    vertices = []
    for domain in domain_dict:
        node_dict.setdefault(domain, ctr)
        vertices.append(domain)
        g.add_vertices(1)
        ctr += 1
    for email in email_dict:
        node_dict.setdefault(email, ctr)
        vertices.append(email)
        g.add_vertices(1)
        ctr += 1

    #===================================================================
    # Building graph: Add edge
    #===================================================================
    '''
    for domain in domain_dict:
        for domain_email in domain_dict[domain]:
            if domain in email_dict[domain_email]:
                g.add_edges((node_dict[domain], node_dict[domain_email]))
    '''
    for domain in domain_dict:
        for domain_email in domain_dict[domain]:
            g.add_edges((node_dict[domain], node_dict[domain_email]))

    #===================================================================
    # Create graph visualization
    #===================================================================
    print g
    g.vs["label"] = vertices
    g.write_gml(sys.argv[2])
    exit(0)
