import dpkt
import datetime
import os
import multiprocessing 
import socket 
import sys
import matplotlib
import random
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from clustering import range_based_clustering, representative_based_clustering, online_kmeans
from sklearn.cluster import KMeans
import numpy as np


# To make it 100 Gbps
SPEED_UP_RATIO = 125
# EPoch_granularity
GRANULARITY_IN_US = 100

class Analyzer():

    def __init__(self, simulation_id, input_pcap_list, input_pcap_range_enabled, input_pcap_time_adjustment, input_pcap_time_start, input_pcap_time_end, clustering_type, num_clusters, reset_clusters_window, learning_rate, feature_set, normalize_feature_values, prioritizing_type, update_priorities_window, monitoring_window, throughput_logging, traffic_distributions_logging, traffic_distributions_histogram_logging, clustering_performance_logging, clustering_performance_time_logging, priority_performance_logging, priority_performance_time_logging, throughput_priorities_logging, signature_evaluation_logging, output_logfiles_seed, output_pcap, output_pcap_seed):
       
        # Input-file configuration
        self.simulation_id = simulation_id
        self.input_pcap_list = input_pcap_list
        self.input_pcap_range_enabled = input_pcap_range_enabled
        self.input_pcap_time_adjustment = input_pcap_time_adjustment
        self.input_pcap_time_start = input_pcap_time_start
        self.input_pcap_time_end = input_pcap_time_end
        
        # Clustering-algorithm configuration
        self.clustering_type = clustering_type
        self.num_clusters = num_clusters
        self.reset_clusters_window = reset_clusters_window
        self.learning_rate = learning_rate
        self.feature_set = feature_set
        self.normalize_feature_values = normalize_feature_values

        # Prioritization configuration
        self.prioritizing_type = prioritizing_type
        self.update_priorities_window = update_priorities_window

        # Logging configuration
        self.monitoring_window = monitoring_window
        self.throughput_logging = throughput_logging
        self.traffic_distributions_logging = traffic_distributions_logging
        self.traffic_distributions_histogram_logging = traffic_distributions_histogram_logging
        self.clustering_performance_logging = clustering_performance_logging
        self.clustering_performance_time_logging = clustering_performance_time_logging
        self.priority_performance_logging = priority_performance_logging
        self.priority_performance_time_logging = priority_performance_time_logging
        self.throughput_priorities_logging = throughput_priorities_logging
        self.signature_evaluation_logging = signature_evaluation_logging
        
        # Output-files configuration
        self.output_logfiles_seed = output_logfiles_seed
        self.output_pcap = output_pcap
        self.output_pcap_seed = output_pcap_seed

        ##################
        # We print the selected configurations
        ##################

        print("[INFO] ------------------------------------------------------------------------ \n" + 
            "[INFO] Running Analyzer \n"    + 
            "[INFO] ------------------------------------------------------------------------ \n" + 
            "[INFO]  --- # Input-file configuration \n" +
            "[INFO] simulation_id: " + str(simulation_id) + "\n" +
            "[INFO] input_pcap_list[0]: " + str(input_pcap_list[0]) + "\n" +
            "[INFO] input_pcap_range_enabled: " + str(input_pcap_range_enabled) + "\n" +
            "[INFO] input_pcap_time_adjustment: " + str(input_pcap_time_adjustment) + "\n" +
            "[INFO] input_pcap_time_start: " + str(input_pcap_time_start) + "\n" +
            "[INFO] input_pcap_time_end: " + str(input_pcap_time_end) + "\n" +
            "[INFO] ------------------------------------------------------------------------ \n" + 
            "[INFO]  --- # Clustering-algorithm configuration \n" +
            "[INFO] clustering_type: " + str(clustering_type) + "\n" +
            "[INFO] num_clusters: " + str(num_clusters) + "\n" +
            "[INFO] reset_clusters_window: " + str(reset_clusters_window) + "\n" +
            "[INFO] learning_rate: " + str(learning_rate) + "\n" +
            "[INFO] feature_set: " + str(feature_set) + "\n" +
            "[INFO] normalize_feature_values: " + str(normalize_feature_values) + "\n" +
            "[INFO] ------------------------------------------------------------------------ \n" + 
            "[INFO]  --- # Prioritization configuration \n" +
            "[INFO] prioritizing_type: " + str(prioritizing_type) + "\n" +
            "[INFO] update_priorities_window: " + str(update_priorities_window) + "\n" +
            "[INFO] ------------------------------------------------------------------------ \n" + 
            "[INFO]  --- # Logging configuration \n" +
            "[INFO] monitoring_window: " + str(monitoring_window) + "\n" +
            "[INFO] throughput_logging: " + str(throughput_logging) + "\n" +
            "[INFO] traffic_distributions_logging: " + str(traffic_distributions_logging) + "\n" +
            "[INFO] traffic_distributions_histogram_logging: " + str(traffic_distributions_histogram_logging) + "\n" +
            "[INFO] clustering_performance_logging: " + str(clustering_performance_logging) + "\n" +
            "[INFO] clustering_performance_time_logging: " + str(clustering_performance_time_logging) + "\n" +
            "[INFO] priority_performance_logging: " + str(priority_performance_logging) + "\n" +
            "[INFO] priority_performance_time_logging: " + str(priority_performance_time_logging) + "\n" +
            "[INFO] throughput_priorities_logging: " + str(throughput_priorities_logging) + "\n" +
            "[INFO] signature_evaluation_logging: " + str(signature_evaluation_logging) + "\n" +
            "[INFO] ------------------------------------------------------------------------ \n" + 
            "[INFO] # Output-files configuration \n" +
            "[INFO] output_logfiles_seed: " + str(output_logfiles_seed) + "\n" +
            "[INFO] output_pcap: " + str(output_pcap) + "\n" +
            "[INFO] output_pcap_seed: " + str(output_pcap_seed))

    def serial_execute(self):
        for input_pcap_name in self.input_pcap_list:     
            self.analyze(self.simulation_id, input_pcap_name, self.input_pcap_range_enabled, self.input_pcap_time_adjustment, self.input_pcap_time_start, self.input_pcap_time_end, self.clustering_type, self.num_clusters, self.reset_clusters_window, self.learning_rate, self.feature_set, self.normalize_feature_values, self.prioritizing_type, self.update_priorities_window, self.monitoring_window, self.throughput_logging, self.traffic_distributions_logging, self.traffic_distributions_histogram_logging, self.clustering_performance_logging, self.clustering_performance_time_logging, self.priority_performance_logging, self.priority_performance_time_logging, self.throughput_priorities_logging, self.signature_evaluation_logging, self.output_logfiles_seed, self.output_pcap, self.output_pcap_seed)

    def execute(self):
        pool = multiprocessing.Pool(processes=16) # Use 128 cores

        # We start processing the pcap files (individually)
        for input_pcap_name in self.input_pcap_list:     
            pool.apply_async(self.analyze, args=(self.simulation_id, input_pcap_name, self.input_pcap_range_enabled, self.input_pcap_time_adjustment, self.input_pcap_time_start, self.input_pcap_time_end, self.clustering_type, self.num_clusters, self.reset_clusters_window, self.learning_rate, self.feature_set, self.normalize_feature_values, self.prioritizing_type, self.update_priorities_window, self.monitoring_window, self.throughput_logging, self.traffic_distributions_logging, self.traffic_distributions_histogram_logging, self.clustering_performance_logging, self.clustering_performance_time_logging, self.priority_performance_logging, self.priority_performance_time_logging, self.throughput_priorities_logging, self.signature_evaluation_logging, self.output_logfiles_seed, self.output_pcap, self.output_pcap_seed)) 
            
            # TO DEBUG:
            #handler = pool.apply_async(self.analyze, args=(self.simulation_id, input_pcap_name, self.input_pcap_range_enabled, self.input_pcap_time_adjustment, self.input_pcap_time_start, self.input_pcap_time_end, self.clustering_type, self.num_clusters, self.reset_clusters_window, self.learning_rate, self.feature_set, self.normalize_feature_values, self.prioritizing_type, self.update_priorities_window, self.monitoring_window, self.throughput_logging, self.traffic_distributions_logging, self.traffic_distributions_histogram_logging, self.clustering_performance_logging, self.clustering_performance_time_logging, self.priority_performance_logging, self.priority_performance_time_logging, self.throughput_priorities_logging, self.signature_evaluation_logging, self.output_logfiles_seed, self.output_pcap, self.output_pcap_seed))
            #handler.get()
        pool.close()
        pool.join()

    def analyze(self, simulation_id, input_pcap_name, input_pcap_range_enabled, input_pcap_time_adjustment, input_pcap_time_start, input_pcap_time_end, clustering_type, num_clusters, reset_clusters_window, learning_rate, feature_set, normalize_feature_values, prioritizing_type, update_priorities_window, monitoring_window, throughput_logging, traffic_distributions_logging, traffic_distributions_histogram_logging, clustering_performance_logging, clustering_performance_time_logging, priority_performance_logging, priority_performance_time_logging, throughput_priorities_logging, signature_evaluation_logging, output_logfiles_seed, output_pcap, output_pcap_seed):

        ##################
        # We configure the clustering algorithm
        ##################

        # Analyze each pcap file, reading packet by packet
        #print('Started reading file: ' + input_pcap_name)
        read_file = open(input_pcap_name,'rb')
        pcap_reader = dpkt.pcap.Reader(read_file)
        is_first_packet = True

        # Create the clustering-algorithm manager
        if (clustering_type.split("_")[1] == "Range"):
            clustering = range_based_clustering.RangeBasedClustering(num_clusters, feature_set)

        elif (clustering_type.split("_")[1] == "Representative"): 
            clustering = representative_based_clustering.RepresentativeBasedClustering(num_clusters, feature_set)
            
            # We check if we need to periodically initialize centroids with the offline result
            if(len(clustering_type.split("_")) == 4):
                if(clustering_type.split("_")[3] == "Offline-Centroid-Initialization"):
                    batch_packets_offline = []
                    offline = KMeans(n_clusters=num_clusters)
        elif (clustering_type == 'Online_KMeans'):
            clustering = online_kmeans.OnlineKmeans(num_clusters, feature_set)

        elif (clustering_type.split("_")[1] == "KMeans"):
            batch_packets = []
            clustering = KMeans(n_clusters=num_clusters)

        elif (clustering_type == 'Online_Epoch_KMeans'):
            batch_packets = []
            batch_ip_lens = []
            clustering = online_kmeans.OnlineEpochKmeans(num_clusters, feature_set)
        else:
            raise Exception("Clustering algorithm not supported: {}".format(clustering_type))

        ##################
        # We prepare the logging files and the logging configuration
        ##################

        # Create the output files for clustering-performance logging
        if clustering_performance_logging == "True":
            sum_purities = 0
            sum_true_negative_rates = 0
            sum_true_positive_rates = 0
            sum_recall_benign = 0
            sum_recall_malicious = 0
            number_iterations = 0
            original_labels_packets = []

            if input_pcap_range_enabled == "True":

                file_id = input_pcap_name.split('/euler/CICDDoS2019/data/SAT-01-12-2018_0')[1]
                clustering_performance_file = open(output_logfiles_seed + file_id + '_clustering_performance.dat', 'w+')
                if file_id == self.input_pcap_list[0].split('/euler/CICDDoS2019/data/SAT-01-12-2018_0')[1]:
                    clustering_performance_file.write("#Sum_Purities,Sum_True_Negative_Rates,Sum_True_Positive_Rates,Sum_Recall_Benign,Sum_Recall_Malicious,Number_Iterations\n")

                if clustering_performance_time_logging == "True":
                    clustering_performance_time_file = open(output_logfiles_seed + file_id + '_clustering_performance_time.dat', 'w+')
                    if file_id == self.input_pcap_list[0].split('/euler/CICDDoS2019/data/SAT-01-12-2018_0')[1]:
                        clustering_performance_time_file.write("#Date_Time,Purity,True_Negative_Rate,True_Positive_Rate,Recall_Benign,Recall_Malicious\n")

            else:
                clustering_performance_file = open(output_logfiles_seed + '_clustering_performance.dat', 'w+')
                clustering_performance_file.write("#Sum_Purities,Sum_True_Negative_Rates,Sum_True_Positive_Rates,Sum_Recall_Benign,Sum_Recall_Malicious,Number_Iterations\n")
                
                if clustering_performance_time_logging == "True":
                    clustering_performance_time_file = open(output_logfiles_seed + '_clustering_performance_time.dat', 'w+')
                    clustering_performance_time_file.write("#Date_Time,Purity,True_Negative_Rate,True_Positive_Rate,Recall_Benign,Recall_Malicious\n")



        # Throughput logging (actually numpackets)
        if throughput_logging == "True":        

            if input_pcap_range_enabled == "True":
        
                file_id = input_pcap_name.split('/euler/CICDDoS2019/data/SAT-01-12-2018_0')[1]
                throughput_file = open(output_logfiles_seed + file_id + '_throughput.dat', 'w+')
                if file_id == self.input_pcap_list[0].split('/euler/CICDDoS2019/data/SAT-01-12-2018_0')[1]:
                    throughput_file.write("#Time,Benign_throughput,Malicious_throughput\n")

            else:
                throughput_file = open(output_logfiles_seed + '_throughput.dat', 'w+')
                throughput_file.write("#Time,Benign_throughput,Malicious_throughput\n")

            # We initialize the time loggers
            current_throughput_benign = 0
            current_throughput_malicious = 0

        ##################
        # We start processing packets
        ##################

        for timestamp, buf in pcap_reader:

            # Extract the date and time
            if input_pcap_time_adjustment.split(",")[0] == "Remove":
                date_time = datetime.datetime.fromtimestamp(timestamp)-datetime.timedelta(hours=int(input_pcap_time_adjustment.split(",")[1]), minutes=0)
            elif input_pcap_time_adjustment.split(",")[0] == "Add":
                date_time = datetime.datetime.fromtimestamp(timestamp)+datetime.timedelta(hours=int(input_pcap_time_adjustment.split(",")[1]), minutes=0)
            else:
                date_time = datetime.datetime.fromtimestamp(timestamp)

            # Analyze only the parts in which there is attack
            if(simulation_id == "CICDDoS2019"):
                
                # According to the CSV analysis
                ntp_start       = datetime.datetime(2018, 12, 1, 10, 35, 0, 0)
                ntp_end         = datetime.datetime(2018, 12, 1, 10, 51, 39, 813446)

                dns_start       = datetime.datetime(2018, 12, 1, 10, 51, 39, 813448)
                dns_end         = datetime.datetime(2018, 12, 1, 11, 22, 40, 254721)

                ldap_start      = datetime.datetime(2018, 12, 1, 11, 22, 40, 254769)
                ldap_end        = datetime.datetime(2018, 12, 1, 11, 32, 32, 915362)

                mssql_start     = datetime.datetime(2018, 12, 1, 11, 32, 32, 915441)
                mssql_end       = datetime.datetime(2018, 12, 1, 11, 47, 8, 463108)

                netbios_start   = datetime.datetime(2018, 12, 1, 11, 47, 8, 463789)
                netbios_end     = datetime.datetime(2018, 12, 1, 12, 0, 13, 902733)

                snmp_start      = datetime.datetime(2018, 12, 1, 12, 00, 13, 902782)
                snmp_end        = datetime.datetime(2018, 12, 1, 12, 23, 13, 663371)

                ssdp_start      = datetime.datetime(2018, 12, 1, 12, 23, 13, 663425)
                ssdp_end        = datetime.datetime(2018, 12, 1, 12, 36, 57, 627790)

                udp_start       = datetime.datetime(2018, 12, 1, 12, 36, 57, 628026)
                udp_end         = datetime.datetime(2018, 12, 1, 13, 4, 45, 928383)

                udplag_start    = datetime.datetime(2018, 12, 1, 13, 4, 45, 928673)
                udplag_end      = datetime.datetime(2018, 12, 1, 13, 30, 30, 740559)

                syn_start       = datetime.datetime(2018, 12, 1, 13, 30, 30, 741451)
                syn_end         = datetime.datetime(2018, 12, 1, 13, 34, 27, 403192)
                
                tftp_start      = datetime.datetime(2018, 12, 1, 13, 34, 27, 403713)
                tftp_end        = datetime.datetime(2018, 12, 1, 14, 10, 0, 0)

                # We use the input_pcap_time_start field to select the attack that we want to run
                if (input_pcap_time_start == "NTP"):
                    if (date_time < ntp_start or date_time > ntp_end):
                        continue

                elif (input_pcap_time_start == "DNS"):
                    if (date_time < dns_start or date_time > dns_end):
                        continue

                elif (input_pcap_time_start == "LDAP"):
                    if (date_time < ldap_start or date_time > ldap_end):
                        continue

                elif (input_pcap_time_start == "MSSQL"):
                    if (date_time < mssql_start or date_time > mssql_end):
                        continue

                elif (input_pcap_time_start == "NetBIOS"):
                    if (date_time < netbios_start or date_time > netbios_end):
                        continue

                elif (input_pcap_time_start == "SNMP"):
                    if (date_time < snmp_start or date_time > snmp_end):
                        continue

                elif (input_pcap_time_start == "SSDP"):
                    if (date_time < ssdp_start or date_time > ssdp_end):
                        continue

                elif (input_pcap_time_start == "UDP"):
                    if (date_time < udp_start or date_time > udp_end):
                        continue

                elif (input_pcap_time_start == "UDPLag"):
                    if (date_time < udplag_start or date_time > udplag_end):
                        continue
                
                elif (input_pcap_time_start == "SYN"):
                    if (date_time < syn_start or date_time > syn_end):
                        continue
                
                elif (input_pcap_time_start == "TFTP"):
                    if (date_time < tftp_start or date_time > tftp_end):
                        continue
                
                elif (input_pcap_time_start == "Reflection"):

                    # If we want to just look at reflection:
                    reflection = False
                    if ((date_time > ntp_start and date_time < ntp_end) 
                    or (date_time > dns_start and date_time < dns_end)
                    or (date_time > ldap_start and date_time < ldap_end)
                    or (date_time > mssql_start and date_time < mssql_end)
                    or (date_time > netbios_start and date_time < netbios_end)
                    or (date_time > snmp_start and date_time < snmp_end)
                    or (date_time > ssdp_start and date_time < ssdp_end)
                    or (date_time > tftp_start and date_time < tftp_end)):
                        reflection = True

                    if reflection == False:
                        continue


                # We focus on the parts where there is attack going on
                if ((date_time < ntp_start) 
                    or (date_time > tftp_end)):

                    continue

            # We define the initial time reference
            if is_first_packet == True:
                
                # We notify that the time we want to analyze is found (at least) in this file 
                print(str(date_time) + ': Time match in: ' + input_pcap_name)

                # We initialize the time counters
                last_reset_clusters = date_time
                last_monitoring_update = date_time
                last_epoch_update = date_time
                is_first_packet = False

            # Unpack the Ethernet frame
            eth = dpkt.ethernet.Ethernet(buf)

            # Make sure the Ethernet data contains an IP packet
            if not isinstance(eth.data, dpkt.ip.IP):
                continue

            # Unpack the data within the Ethernet frame (the IP packet)
            ip = eth.data
            
            # We only process IPv4 packets
            try:
                src =  socket.inet_ntop(socket.AF_INET, ip.src)
                src0 = int(src.split(".")[0])
                src1 = int(src.split(".")[1])
                src2 = int(src.split(".")[2])
                src3 = int(src.split(".")[3])

            except ValueError:
                src =  socket.inet_ntop(socket.AF_INET6, ip.src)
                continue

            try:
                dst =  socket.inet_ntop(socket.AF_INET, ip.dst)
                dst0 = int(dst.split(".")[0])
                dst1 = int(dst.split(".")[1])
                dst2 = int(dst.split(".")[2])
                dst3 = int(dst.split(".")[3])

            except ValueError:
                dst =  socket.inet_ntop(socket.AF_INET6, ip.dst)
                continue

            # We extract the source and destination port of the transport layer
            if isinstance(ip.data, dpkt.tcp.TCP):
                tcp = ip.data
                sport = tcp.sport
                dport = tcp.dport

            elif isinstance(ip.data, dpkt.udp.UDP): 
                udp = ip.data
                sport = udp.sport
                dport = udp.dport

            else:
                continue

            # We only process packets of the downlink
            if(simulation_id == "CICDDoS2019"):
                if (dst == "172.16.0.5"):
                    continue

                # Correct the source port for the reflection attacks
                if (src == "172.16.0.5"): # if malicious
                    if (date_time > ntp_start and date_time < ntp_end):
                        sport = 123
                    elif (date_time > dns_start and date_time < dns_end):
                        sport = 53
                    elif (date_time > ldap_start and date_time < ldap_end):
                        sport = 389
                    elif (date_time > mssql_start and date_time < mssql_end):
                        pick_from = [1433, 4022, 135, 1434]
                        sport = random.choice(pick_from)
                    elif (date_time > netbios_start and date_time < netbios_end):
                        sport = 137
                    elif (date_time > snmp_start and date_time < snmp_end):
                        sport = 161
                    elif (date_time > ssdp_start and date_time < ssdp_end):
                        sport = 1900
                    elif (date_time > tftp_start and date_time < tftp_end):
                        sport = 69

            # Create the packet feature vector
            full_packet = {
                "len"         : ip.len,
                "id"          : ip.id,
                "frag_offset" : ip._flags_offset,
                "ttl"         : ip.ttl,
                "proto"       : ip.p,
                "src0"        : src0,
                "src1"        : src1,
                "src2"        : src2,
                "src3"        : src3,
                "dst0"        : dst0,
                "dst1"        : dst1,
                "dst2"        : dst2,
                "dst3"        : dst3,
                "sport"       : sport,
                "dport"       : dport
            }

            if normalize_feature_values == "True":
                full_packet = {
                    "len"         : float(ip.len/65535),
                    "id"          : float(ip.id/65535),
                    "frag_offset" : float(ip._flags_offset/8191),
                    "ttl"         : float(ip.ttl/255),
                    "proto"       : float(ip.p/255),
                    "src0"        : float(src0/255),
                    "src1"        : float(src1/255),
                    "src2"        : float(src2/255),
                    "src3"        : float(src3/255),
                    "dst0"        : float(dst0/255),
                    "dst1"        : float(dst1/255),
                    "dst2"        : float(dst2/255),
                    "dst3"        : float(dst3/255),
                    "sport"       : float(sport/65535),
                    "dport"       : float(dport/65535)
                }
                
            packet = []
            for feature in feature_set.split(","):
                packet.append(full_packet[feature])

            # Cluster that packet
            if clustering_type == "Online_Range_Fast_Anime":
                selected_cluster = clustering.fit_fast(packet, ip.len, "anime")

            elif clustering_type == "Online_Range_Fast_Manhattan":
                selected_cluster = clustering.fit_fast(packet, ip.len, "manhattan")

            elif clustering_type == "Online_Range_Exhaustive_Anime":
                selected_cluster = clustering.fit_exhaustive(packet, ip.len, "anime")

            elif clustering_type == "Online_Range_Exhaustive_Manhattan":
                selected_cluster = clustering.fit_exhaustive(packet, ip.len, "manhattan")

            elif clustering_type == "Online_Representative_Fast" or clustering_type == "Online_Representative_Fast_Offline-Centroid-Initialization":
                selected_cluster = clustering.fit_fast(packet, ip.len, learning_rate)

                # We keep track of the packets so that we can later run the offline initialization for the current batch
                if(len(clustering_type.split("_")) == 4):
                    if(clustering_type.split("_")[3] == "Offline-Centroid-Initialization"):
                        batch_packets_offline.append(packet)

            elif clustering_type == "Online_Representative_Exhaustive" or clustering_type == "Online_Representative_Exhaustive_Offline-Centroid-Initialization":
                selected_cluster = clustering.fit_exhaustive(packet, ip.len, learning_rate)

                # We keep track of the packets so that we can later run the offline initialization for the current batch
                if(len(clustering_type.split("_")) == 4):
                    if(clustering_type.split("_")[3] == "Offline-Centroid-Initialization"):
                        batch_packets_offline.append(packet)

            elif clustering_type == "Offline_KMeans":
                # We just append the generated packet to a batch of packets, which we will then cluster together
                batch_packets.append(packet)

            elif clustering_type == "Online_KMeans":
                selected_cluster = clustering.fit_fast(packet, ip.len)
            elif clustering_type == "Online_Epoch_KMeans":
                # We just append the generated packets to a batch of packets
                batch_packets.append(packet)
                batch_ip_lens.append(ip.len)
            else:
                raise Exception("Clustering algorithm not supported: {}".format(clustering_type))
            ##################
            # We perform the per-packet logging
            ##################

            # Clustering-performance logging
            if clustering_performance_logging == "True":

                if(simulation_id == "CICDDoS2019"):

                    # We keep the ground-truth label for the packet so that later we can compute the purity with it
                    if (src == "172.16.0.5"):
                        # Malicious
                        original_labels_packets.append(False)
                    
                    else:
                        # Benign
                        original_labels_packets.append(True)

                elif (simulation_id == "Morphing"):

                    # We keep the ground-truth label for the packet so that later we can compute the purity with it
                    if (src == "192.168.0.5"):
                        # Malicious
                        original_labels_packets.append(False)
                    
                    else:
                        # Benign
                        original_labels_packets.append(True)

                else:
                    raise Exception("Simulation ID not supported: {}".format(simulation_id))


            if throughput_logging == "True":

                if(simulation_id == "CICDDoS2019"):
                    if (src == "172.16.0.5"):
                        current_throughput_malicious = current_throughput_malicious + int(ip.len)*8 + (60*8) + (60*8) # We put the 60 bytes headers that Netbench will add (instead of the original headers)
                    else:
                        current_throughput_benign = current_throughput_benign + int(ip.len)*8 + (60*8) + (60*8)

                elif(simulation_id == "Morphing"):
                    if (src == "192.168.0.5"):
                        current_throughput_malicious = current_throughput_malicious + int(ip.len)*8 + (60*8) + (60*8)
                    else:
                        current_throughput_benign = current_throughput_benign + int(ip.len)*8 + (60*8) + (60*8)

                else:
                    raise Exception("Simulation ID not supported: {}".format(simulation_id))

            ##################
            # We perform the per-monitoring-window logging
            ##################
            if clustering_type == "Online_Epoch_KMeans":
                delta_in_ms = int((date_time - last_epoch_update).total_seconds() * 1000)
                if delta_in_ms >= (SPEED_UP_RATIO * GRANULARITY_IN_US) / 1000 :
                    last_epoch_update = date_time
                    clustering.fit_batch(batch_packets, batch_ip_lens)
                    batch_packets = []
                    batch_ip_lens = []

            # We update time buckets for monitoring
            if (monitoring_window != -1):
                difference_tracking = (date_time-last_monitoring_update).total_seconds()
                if (difference_tracking > monitoring_window):
                    # Clustering-performance logging
                    if clustering_performance_logging == "True":
                    
                        # We initialize the purity and the other statistical metrics that we want to extract
                        purity = 0
                        true_negative_rate = 0
                        true_positive_rate = 0
                        recall_benign = 0
                        recall_malicious = 0

                        majority_benign_counter = {}
                        majority_malicious_counter = {}
                        total_benign_packets_interval = 0
                        total_malicious_packets_interval = 0

                        # We first assign each cluster to the class which is most frequent in the cluster
                        for n in range(num_clusters):
                            majority_benign_counter[n] = 0
                            majority_malicious_counter[n] = 0

                        # We extract the labels allocated to the clustered packets so far and use them to compute purity
                        if (clustering_type == "Online_Range_Fast_Manhattan" or clustering_type == "Online_Range_Fast_Anime" 
                            or clustering_type == "Online_Range_Exhaustive_Manhattan"  or clustering_type == "Online_Range_Exhaustive_Anime"
                            or clustering_type == "Online_Representative_Fast" or clustering_type == "Online_Representative_Fast_Offline-Centroid-Initialization" 
                            or clustering_type == "Online_Representative_Exhaustive" or clustering_type == "Online_Representative_Exhaustive_Offline-Centroid-Initialization" 
                            or clustering_type == "Online_Random_Fast" or clustering_type == "Online_Hash"
                            or clustering_type == "Online_KMeans"):
                            result_labels = clustering.get_labels()
                        elif clustering_type == "Online_Epoch_KMeans":
                            # Fit the avaiable batch packets
                            clustering.fit_batch(batch_packets, batch_ip_lens)
                            batch_packets = []
                            batch_ip_lens = []
                            result_labels = clustering.get_labels()
                        else:
                            # Offline k-means (we need to fit the whole packet batch)
                            if (len(batch_packets) >= num_clusters):
                                array_batch_packets = np.array(batch_packets)
                                clustering.fit(array_batch_packets)
                                result_labels = clustering.labels_
                                batch_packets = []
                            else:
                                # If we don't have enough samples to run kmeans, we just assign each sample to a different cluster
                                result_labels = []
                                for label in range(len(batch_packets)):
                                    result_labels.append(label)
                                batch_packets = []

                        # We count the number of benign and malicious packets clustered in each cluster
                        for p in range(len(result_labels)):
                            if (original_labels_packets[p] == True):
                                majority_benign_counter[result_labels[p]] = majority_benign_counter[result_labels[p]] + 1
                                total_benign_packets_interval = total_benign_packets_interval + 1
                            else:
                                majority_malicious_counter[result_labels[p]] = majority_malicious_counter[result_labels[p]] + 1
                                total_malicious_packets_interval = total_malicious_packets_interval + 1

                        for n in range(num_clusters):
                            if (majority_benign_counter[n] >= majority_malicious_counter[n]):

                                # The cluster is classified as benign
                                purity = purity + majority_benign_counter[n]
                                true_negative_rate = true_negative_rate + majority_benign_counter[n]

                            else:

                                # The cluster is classified as malicious
                                purity = purity + majority_malicious_counter[n]
                                true_positive_rate = true_positive_rate + majority_malicious_counter[n]

                        print("#packes inside this monitoring interval: {}".format(len(result_labels)))
                        # We only study the intervals in which we have both benign and malicious traffic, otherwise the clustering makes no sense
                        if (len(result_labels) != 0) and (total_benign_packets_interval != 0) and (total_malicious_packets_interval != 0):
                            recall_benign = (true_negative_rate/total_benign_packets_interval)*100
                            recall_malicious = (true_positive_rate/total_malicious_packets_interval)*100

                            purity = (purity/len(result_labels))*100
                            true_negative_rate = (true_negative_rate/len(result_labels))*100
                            true_positive_rate = (true_positive_rate/len(result_labels))*100

                            # We log the result for the iteration if temporal logging is enabled                
                            if clustering_performance_time_logging == "True":
                                clustering_performance_time_file.write(str(date_time) + "," + str(purity)+ "," + str(true_negative_rate)+ "," + str(true_positive_rate) + "," + str(recall_benign) + "," + str(recall_malicious) + "\n")
                            
                            # We aggregate the results for overall logging
                            sum_purities = sum_purities + purity
                            sum_true_negative_rates = sum_true_negative_rates + true_negative_rate
                            sum_true_positive_rates = sum_true_positive_rates + true_positive_rate
                            sum_recall_benign = sum_recall_benign + recall_benign
                            sum_recall_malicious = sum_recall_malicious + recall_malicious
                            number_iterations = number_iterations + 1

                        # We reset the analyzed labels and also the labels from the clustering algorithm object (otherwise there will be a missmatch)
                        original_labels_packets.clear()
                        if (clustering_type == "Online_Range_Fast_Manhattan" or clustering_type == "Online_Range_Fast_Anime" 
                            or clustering_type == "Online_Range_Exhaustive_Manhattan"  or clustering_type == "Online_Range_Exhaustive_Anime"
                            or clustering_type == "Online_Representative_Fast" or clustering_type == "Online_Representative_Fast_Offline-Centroid-Initialization" 
                            or clustering_type == "Online_Representative_Exhaustive" or clustering_type == "Online_Representative_Exhaustive_Offline-Centroid-Initialization" 
                            or clustering_type == "Online_Random_Fast" or clustering_type == "Online_Hash"
                            or clustering_type == "Online_KMeans"
                            or clustering_type == "Online_Epoch_KMeans"):
                            clustering.reset_labels() # Note that this does not reset the clusters, nor their centroids
                        else:
                            # Offline k-means
                            clustering = KMeans(n_clusters=num_clusters) # Here we just create a new instance, such that we don't have previous labels

                    
                    # Throughput logging
                    if throughput_logging == "True":
                        throughput_file.write(str(date_time) + "," + str(current_throughput_benign) + "," + str(current_throughput_malicious) + "\n")                    
                        current_throughput_benign = 0
                        current_throughput_malicious = 0

                    
                    # We update the time tracker
                    last_monitoring_update = date_time

            # After having performed the required monitoring (if needed), we reset the clusters if the window has expired
            if reset_clusters_window != -1:

                # If both monitoring and reset_clusters are active, they should be the same value for the program to work correctly
                #if monitoring_window != -1:
                    #assert monitoring_window == reset_clusters_window
                
                difference_reset_clusters = (date_time-last_reset_clusters).total_seconds()
                if (difference_reset_clusters > reset_clusters_window):

                    # We delete all existing clusters
                    if (clustering_type == "Online_Range_Fast_Manhattan" or clustering_type == "Online_Range_Fast_Anime" 
                        or clustering_type == "Online_Range_Exhaustive_Manhattan"  or clustering_type == "Online_Range_Exhaustive_Anime"
                        or clustering_type == "Online_Representative_Fast" or clustering_type == "Online_Representative_Fast_Offline-Centroid-Initialization" 
                        or clustering_type == "Online_Representative_Exhaustive" or clustering_type == "Online_Representative_Exhaustive_Offline-Centroid-Initialization" 
                        or clustering_type == "Online_Random_Fast" or clustering_type == "Online_Hash"
                        or clustering_type == "Online_KMeans"
                        or clustering_type == "Online_Epoch_KMeans"
                        ):
                        clustering.reset_clusters()

                        # If we decided offline initialization, instead of delete the clusters, we create N clusters and initialize them with
                        # the results of the centroids of the offline clustering for the previous batch
                        if(clustering_type.split("_")[1] == "Representative"):
                            if(len(clustering_type.split("_")) == 4): 
                                if (clustering_type.split("_")[3] == "Offline-Centroid-Initialization"):

                                    # We compute the centroids. 
                                    # If we don't have enough samples to run kmeans, we just do not initialize the centroids
                                    if (len(batch_packets_offline) >= num_clusters):
                                        array_batch_packets_offline = np.array(batch_packets_offline)
                                        offline.fit(array_batch_packets_offline)
                                        centroids = offline.cluster_centers_
                                        clustering.initialize(centroids)
                                    
                                    # We clean the batch of packets
                                    batch_packets_offline = []

                    # We update the time tracker
                    last_reset_clusters = date_time

        ##################
        # We close all logging files
        ##################

        # We close the input file
        read_file.close()

        # Clustering-performance logging
        if clustering_performance_logging == "True":
            if (number_iterations > 0):
                clustering_performance_file.write(str(sum_purities) + "," + str(sum_true_negative_rates) + "," + str(sum_true_positive_rates) + "," + str(sum_recall_benign) + "," + str(sum_recall_malicious) + "," + str(number_iterations) + "\n") 
            clustering_performance_file.close()

            # We close the clustering performance logging file
            if clustering_performance_time_logging == "True":
                clustering_performance_time_file.close()
        

