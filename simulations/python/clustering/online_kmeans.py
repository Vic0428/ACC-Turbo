from clustering import cluster, clustering_algorithm
import math

class OnlineKmeans(clustering_algorithm.ClusteringAlgorithm):

    def __init__(self, num_clusters, feature_set):
        self.feature_list = feature_set.split(",") # List of features that we want to use
        clustering_algorithm.ClusteringAlgorithm.__init__(self, num_clusters) 

    # In representative-based, the cluster signature carries the same information (the centroid) in the two tuple values
    # Computes the euclidean distance
    def compute_distance(self, cluster_a, cluster_b):
        sum = 0
        for feature in self.feature_list:
            sum = sum + (abs(cluster_a.signature[feature][0] - cluster_b.signature[feature][0]) ** 2)
        distance = math.sqrt(sum)
        assert (distance >= 0)
        return distance

    # Method to update the centroid of "dst_cluster" with the information of "src_cluster"
    def update_center(self, src_cluster, dst_cluster):
        ratio = 1 / dst_cluster.packets
        for feature in self.feature_list:
           dst_cluster.signature[feature] = ((dst_cluster.signature[feature][0] + ratio*(src_cluster.signature[feature][0]- dst_cluster.signature[feature][0])),  (dst_cluster.signature[feature][1] + ratio*(src_cluster.signature[feature][1] - dst_cluster.signature[feature][1])))
        
    # Method to initialize the centroids with some values (e.g., the offline-clustering result of the previous batch)
    def initialize(self, centroids): 
        
        # We create a cluster for each of the centroids
        for centroid in centroids:
            i = 0
            cluster_signature = {}
            assert len(centroid) == len(self.feature_list)
            for feature in self.feature_list:
                cluster_signature[feature] = (centroid[i],centroid[i])
                i = i + 1

            # Create new cluster for the centroid (we set the bit counter to zero)
            new_cluster = cluster.Cluster(cluster_signature, self.current_cluster_id, self.num_clusters, self.feature_list, 0)
            self.current_cluster_id = self.current_cluster_id + 1
            
            # Append the new cluster directly to the list
            assert len(self.cluster_list) < self.num_clusters
            self.cluster_list.append(new_cluster)

	## Computes the result of clustering one new packet following the exhaustive version of the representative_based clustering algorithm	
    def fit_exhaustive(self, packet, ip_len):

        # It makes no sense to measure distances across existing clusters if num_clusters = 1
        assert self.num_clusters > 1

        i = 0
        packet_signature = {}
        assert len(packet) == len(self.feature_list)
        for feature in self.feature_list:
            packet_signature[feature] = (packet[i],packet[i])
            i = i + 1

        # Create new cluster for the packet
        new_cluster = cluster.Cluster(packet_signature, self.current_cluster_id, self.num_clusters, self.feature_list, ip_len)
        self.current_cluster_id = self.current_cluster_id + 1

        # If the cluster list has less than num_clusters clusters, we can just add the new cluster to the list
        if len(self.cluster_list) < self.num_clusters:

            # Append the new cluster directly to the list
            self.cluster_list.append(new_cluster)
            selected_cluster = new_cluster
            
        else:
            # Compute the distances of the new (virtual) cluster with all existing clusters
            i = 0
            for existing_cluster in self.cluster_list:
                distance = self.compute_distance(existing_cluster, new_cluster)
                if (i == 0):
                    min_distance = distance
                    min_cluster = existing_cluster
                    i = i + 1
                else:
                    if (distance < min_distance):
                        min_distance = distance
                        min_cluster = existing_cluster

            # We need to check the distances across all the existing clusters
            i = 0            
            for j in range(len(self.cluster_list)):
                for k in range(j+1, len(self.cluster_list)):
                    existing_distance = self.compute_distance(self.cluster_list[j], self.cluster_list[k])
                    if (i == 0):
                        existing_min_distance = existing_distance
                        existing_min_cluster_a = self.cluster_list[j]
                        existing_min_cluster_b = self.cluster_list[k]
                        i = i + 1
                    else:
                        if(existing_distance < existing_min_distance):
                            existing_min_distance = existing_distance
                            existing_min_cluster_a = self.cluster_list[j]
                            existing_min_cluster_b = self.cluster_list[k]                                

            # We then use the distances to decide what to merge
            if (min_distance < existing_min_distance):
                self.update_center(new_cluster, min_cluster)
                min_cluster.update_statistics(new_cluster)
                selected_cluster = min_cluster
                
            else:
                # We merge cluster b to cluster a and remove cluster b from the list
                self.update_center(existing_min_cluster_b, existing_min_cluster_a)
                existing_min_cluster_a.update_statistics(existing_min_cluster_b)
                
                # Before removing b from the list, we check which was its id, which we will reuse for the newly created cluster
                id_to_reuse = existing_min_cluster_b.get_id()
                self.cluster_list.remove(existing_min_cluster_b)
                
                # We also re-label all the packets of the removed cluster to the id of the cluster they are merged to
                # This is just so that the purity computation does not get polluted
                for l in range(len(self.labels)):
                    if self.labels[l] == id_to_reuse:
                        self.labels[l] = existing_min_cluster_a.get_id()

                # We then add the new cluster to the list
                new_cluster.set_id(id_to_reuse)
                self.cluster_list.append(new_cluster)
                selected_cluster = new_cluster

        # We append the label (cluster_id) to the list 
        self.append_label(selected_cluster.get_id())
        return selected_cluster


	# Computes the result of clustering one new packet following the fast version of the representative_based clustering algorithm.
    def fit_fast(self, packet, ip_len):

        i = 0
        packet_signature = {}
        assert len(packet) == len(self.feature_list)
        for feature in self.feature_list:
            packet_signature[feature] = (packet[i],packet[i])
            i = i + 1

        # Create new cluster for the packet (note that we do not update current_cluster_id straight away, since we will only use it if thee new_cluster is actually created)
        new_cluster = cluster.Cluster(packet_signature, self.current_cluster_id, self.num_clusters, self.feature_list, ip_len)

        # If the cluster list is empty, we just add the new custer to the list
        if len(self.cluster_list) == 0:

            # Append the new cluster directly to the list
            self.cluster_list.append(new_cluster)
            selected_cluster = new_cluster
            self.current_cluster_id = self.current_cluster_id + 1

        # If it is not empty, we compute the minimum distance (to the clusters in the list)
        else:
            # Compute the distances of the new (virtual) cluster with all existing clusters
            i = 0
            for existing_cluster in self.cluster_list:
                distance = self.compute_distance(existing_cluster, new_cluster)
                if (i == 0):
                    min_distance = distance
                    min_cluster = existing_cluster
                    i = i + 1
                else:
                    if (distance < min_distance):
                        min_distance = distance
                        min_cluster = existing_cluster


            # Then we decide. If the list is already full, then we merge to the closest distance
            if len(self.cluster_list) >= self.num_clusters:

                # Merge the new cluster to the closest one
                self.update_center(new_cluster, min_cluster)
                min_cluster.update_statistics(new_cluster)
                selected_cluster = min_cluster

            # If the list is not full, we decide whether we want to create a new cluster or merge to the closest one.
            else: 

                if (min_distance == 0):

                    # Merge the new cluster to the closest one
                    self.update_center(new_cluster, min_cluster)
                    min_cluster.update_statistics(new_cluster)
                    selected_cluster = min_cluster

                else:

                    # Append the new cluster directly to the list
                    self.cluster_list.append(new_cluster)
                    selected_cluster = new_cluster
                    self.current_cluster_id = self.current_cluster_id + 1

        # We append the label (cluster_id) to the list 
        self.append_label(selected_cluster.get_id())
        return selected_cluster


class OnlineEpochKmeans(clustering_algorithm.ClusteringAlgorithm):

    def __init__(self, num_clusters, feature_set):
        self.feature_list = feature_set.split(",") # List of features that we want to use
        self.feature_list = self.feature_list[:-2]
        clustering_algorithm.ClusteringAlgorithm.__init__(self, num_clusters) 

    # In representative-based, the cluster signature carries the same information (the centroid) in the two tuple values
    # Computes the euclidean distance
    def compute_distance(self, cluster_a, cluster_b):
        sum = 0
        for feature in self.feature_list:
            sum = sum + (abs(cluster_a.signature[feature][0] - cluster_b.signature[feature][0]) ** 2)
        distance = math.sqrt(sum)
        assert (distance >= 0)
        return distance

    # Method to update the centroid of "dst_cluster" with the information of "src_cluster"
    def update_center(self, src_cluster, dst_cluster):
        static_shift_offset = 4
        for feature in self.feature_list:
            update_val = (dst_cluster.signature[feature][0] + (src_cluster.packets*(src_cluster.signature[feature][0]- dst_cluster.signature[feature][0])) >> static_shift_offset)
            dst_cluster.signature[feature] = (update_val, update_val)
        
    # Method to initialize the centroids with some values (e.g., the offline-clustering result of the previous batch)
    def initialize(self, centroids): 
        
        # We create a cluster for each of the centroids
        for centroid in centroids:
            i = 0
            cluster_signature = {}
            assert len(centroid) == len(self.feature_list)
            for feature in self.feature_list:
                cluster_signature[feature] = (centroid[i],centroid[i])
                i = i + 1

            # Create new cluster for the centroid (we set the bit counter to zero)
            new_cluster = cluster.Cluster(cluster_signature, self.current_cluster_id, self.num_clusters, self.feature_list, 0)
            self.current_cluster_id = self.current_cluster_id + 1
            
            # Append the new cluster directly to the list
            assert len(self.cluster_list) < self.num_clusters
            self.cluster_list.append(new_cluster)
    
    def fit_batch(self, batch_packets, batch_ip_lens, perfect=True):
        # print("Invoke to fit {} packets".format(len(batch_packets)))
        mp_key = {}
        mp_val = {}
        for packet, ip_len in zip(batch_packets, batch_ip_lens):
            # Use a perfect map to do the epoch-based aggregation 
            ip_val = 0
            for num in packet:
                ip_val += 256 * ip_val + num

            if ip_val not in mp_key:
                mp_key[ip_val] = packet
                mp_val[ip_val] = 1
            else:
                mp_val[ip_val] += 1

        label_mp = {}        
        # Update based on aggregation result
        for ip_val in mp_key.keys():
            packet = mp_key[ip_val]
            pkt_cnt = mp_val[ip_val]
            cid = self.fit_batch_helper(packet, pkt_cnt)
            label_mp[ip_val] = cid

        for packet in batch_packets:
            ip_val = 0
            for num in packet:
                ip_val += 256 * ip_val + num
            self.append_label(label_mp[ip_val])




	# Computes the result of clustering one new packet following the fast version of the representative_based clustering algorithm.
    def fit_batch_helper(self, packet, pkt_cnt):
        i = 0
        packet_signature = {}
        # assert len(packet) == len(self.feature_list)
        for feature in self.feature_list:
            packet_signature[feature] = (packet[i],packet[i])
            i = i + 1

        # Create new cluster for the packet (note that we do not update current_cluster_id straight away, since we will only use it if thee new_cluster is actually created)
        new_cluster = cluster.Cluster(packet_signature, self.current_cluster_id, self.num_clusters, self.feature_list, 0)
        new_cluster.packets = pkt_cnt

        # If the cluster list is empty, we just add the new custer to the list
        if len(self.cluster_list) == 0:

            # Append the new cluster directly to the list
            self.cluster_list.append(new_cluster)
            selected_cluster = new_cluster
            self.current_cluster_id = self.current_cluster_id + 1

        # If it is not empty, we compute the minimum distance (to the clusters in the list)
        else:
            # Compute the distances of the new (virtual) cluster with all existing clusters
            i = 0
            for existing_cluster in self.cluster_list:
                distance = self.compute_distance(existing_cluster, new_cluster)
                if (i == 0):
                    min_distance = distance
                    min_cluster = existing_cluster
                    i = i + 1
                else:
                    if (distance < min_distance):
                        min_distance = distance
                        min_cluster = existing_cluster


            # Then we decide. If the list is already full, then we merge to the closest distance
            if len(self.cluster_list) >= self.num_clusters:

                # Merge the new cluster to the closest one
                self.update_center(new_cluster, min_cluster)
                min_cluster.update_statistics(new_cluster)
                selected_cluster = min_cluster

            # If the list is not full, we decide whether we want to create a new cluster or merge to the closest one.
            else: 

                if (min_distance == 0):

                    # Merge the new cluster to the closest one
                    self.update_center(new_cluster, min_cluster)
                    min_cluster.update_statistics(new_cluster)
                    selected_cluster = min_cluster

                else:

                    # Append the new cluster directly to the list
                    self.cluster_list.append(new_cluster)
                    selected_cluster = new_cluster
                    self.current_cluster_id = self.current_cluster_id + 1

        # We append the label (cluster_id) to the list 
        # self.append_label(selected_cluster.get_id())
        return selected_cluster.get_id()

	# Computes the result of clustering one new packet following the fast version of the representative_based clustering algorithm.
    def fit_fast(self, packet, ip_len):

        i = 0
        packet_signature = {}
        assert len(packet) == len(self.feature_list)
        for feature in self.feature_list:
            packet_signature[feature] = (packet[i],packet[i])
            i = i + 1

        # Create new cluster for the packet (note that we do not update current_cluster_id straight away, since we will only use it if thee new_cluster is actually created)
        new_cluster = cluster.Cluster(packet_signature, self.current_cluster_id, self.num_clusters, self.feature_list, ip_len)

        # If the cluster list is empty, we just add the new custer to the list
        if len(self.cluster_list) == 0:

            # Append the new cluster directly to the list
            self.cluster_list.append(new_cluster)
            selected_cluster = new_cluster
            self.current_cluster_id = self.current_cluster_id + 1

        # If it is not empty, we compute the minimum distance (to the clusters in the list)
        else:
            # Compute the distances of the new (virtual) cluster with all existing clusters
            i = 0
            for existing_cluster in self.cluster_list:
                distance = self.compute_distance(existing_cluster, new_cluster)
                if (i == 0):
                    min_distance = distance
                    min_cluster = existing_cluster
                    i = i + 1
                else:
                    if (distance < min_distance):
                        min_distance = distance
                        min_cluster = existing_cluster


            # Then we decide. If the list is already full, then we merge to the closest distance
            if len(self.cluster_list) >= self.num_clusters:

                # Merge the new cluster to the closest one
                self.update_center(new_cluster, min_cluster)
                min_cluster.update_statistics(new_cluster)
                selected_cluster = min_cluster

            # If the list is not full, we decide whether we want to create a new cluster or merge to the closest one.
            else: 

                if (min_distance == 0):

                    # Merge the new cluster to the closest one
                    self.update_center(new_cluster, min_cluster)
                    min_cluster.update_statistics(new_cluster)
                    selected_cluster = min_cluster

                else:

                    # Append the new cluster directly to the list
                    self.cluster_list.append(new_cluster)
                    selected_cluster = new_cluster
                    self.current_cluster_id = self.current_cluster_id + 1

        # We append the label (cluster_id) to the list 
        self.append_label(selected_cluster.get_id())
        return selected_cluster