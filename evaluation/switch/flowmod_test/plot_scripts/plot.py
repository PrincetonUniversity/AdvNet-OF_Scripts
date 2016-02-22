################################################################
# Plot scripts for flow-mod performance measurement data
#  - Author: Hyojoon Kim (joonk@princeton.edu)
################################################################

################################################################
# Copyright (C) 2016 Hyojoon Kim. Princeton University.
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with this
# work for additional information regarding copyright ownership.  The ASF
# licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
################################################################

import argparse
import python_apis.python_api as python_api
import os,sys
import plot_lib
import numpy as np

def plot_data_avg_comp(product_list, rate_list, nflows_list, pmnr_map, output_dir):
    rate_int_list = sorted(map(int,rate_list))

    # For each nflows
    for n in nflows_list:
        for m in ['add','mod']:
            title =  'nflows'+n+'-'+m
            filename = 'nflows'+n+'-'+m+'.png'
            data_llist = []

            for p in sorted(product_list):
                data_list = []

                for r in rate_int_list:
                    tmp_list = pmnr_map[create_key(p,m,n,str(r))]
                    avg = np.average(tmp_list) 
                    if avg < 0 :
                        avg = 1
                    data_list.append(avg)

                # Add to data_llist    
                data_llist.append(data_list)

            # Plot with all products in hand
            plot_lib.plot_avg_bar(data_llist, rate_int_list, output_dir, filename, title)


def plot_data(product_list, rate_list, nflows_list,pmnr_map, output_dir):
 
    rate_int_list = sorted(map(int,rate_list))

    # For each product,
    for p in sorted(product_list):
        # For each nflows
        for n in nflows_list:
            for m in ['add','mod']:
                data_list = []
                title = p + '_nflows'+n+'-'+m
                filename = p + '_nflows'+n+'-'+m+'.png'
                
                for r in rate_int_list:
                    tmp_list = pmnr_map[create_key(p,m,n,str(r))]
                    data_list.append(tmp_list)

                plot_lib.plot_boxplot(data_list, rate_int_list, output_dir, filename, title)

def create_key(product, mode, nflows, rate):

    return '_'.join([product, mode, nflows, rate])

def rate_and_nflows(input_dir, product, mode,pmnr_map):
    
    rate_set = set()
    nflows_set = set()

    dir_list = os.listdir(input_dir)
    for d in dir_list:
        if os.path.isdir(input_dir + d) is False:
            continue
        # Get rate and nflows
        rate, nflows = d.split('_')
        rate_set.add(rate)
        nflows_set.add(nflows)

        # Get rounds
        value_list = [] 
        for r in os.listdir(input_dir + d):
            if os.path.isdir(input_dir + d + '/' + r) is False:
                continue
            fd = open(input_dir + d + '/' + r + '/' + 'sorted_flow_delay.txt', 'r')
            lines_list = fd.readlines()
            fd.close()

            # Get delay values
            for l in lines_list:
                value_list.append(float(l.split(' ')[3].rstrip('\n')))

        pmnr_map[create_key(product,mode,nflows,rate)] = value_list

    return list(rate_set), list(nflows_set)            


## Parse data in input directory    
def parse_data(input_dir,pmnr_map):

    product_list = os.listdir(input_dir)
    rate_list = []
    nflows_list = []

    # Traverse directory
    for p in product_list:
        if os.path.isdir(input_dir + p) is False:
            product_list.remove(p)
            continue

        # Add
        rate_list, nflows_list = rate_and_nflows(input_dir + p + '/' + 'add/', p, 'add',pmnr_map) 
        # Mod 
        rate_and_nflows(input_dir + p + '/' + 'mod/', p, 'mod',pmnr_map) 

    return product_list, rate_list, nflows_list

def main():

    parser = argparse.ArgumentParser(description='Plot measurement data from directory.')
    parser.add_argument('-i', dest='input_dir', action='store', required=True,
                        help='Input directory')
    parser.add_argument('-o', dest='output_dir', action='store', required=True,
                        help='Output directory')


    args = parser.parse_args()

    # Abort if input directory is wrong
    input_dir = python_api.check_directory_and_add_slash(args.input_dir)
    if input_dir == '':
        sys.exit(0)

    # Create output directory if it does not already exist.
    if os.path.isdir(args.output_dir) is False:
        os.mkdir(args.output_dir)
    output_dir = python_api.check_directory_and_add_slash(args.output_dir)

    # Parse data in input directory
    pmnr_map = {}
    product_list, rate_list, nflows_list = parse_data(input_dir,pmnr_map)

    # Plot data from map
#    plot_data(product_list, rate_list, nflows_list, pmnr_map, output_dir)

    # Plot data for average comparison
    plot_data_avg_comp(product_list, rate_list, nflows_list, pmnr_map, output_dir)


if __name__ == '__main__':
    main()
