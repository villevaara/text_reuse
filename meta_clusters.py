
class MetaCluster:

    def __init__(self, estc_ids, cluster_ids):
        self.estc_ids = estc_ids
        self.cluster_ids = cluster_ids

    def get_cluster_amount(self):
        size = len(self.cluster_ids)
        return size

    def get_book_amount(self):
        size = len(self.estc_ids)
        return size

    def get_meta_cluster_id(self):
        eids = list(self.estc_ids)
        eids_sorted = sorted(eids)
        meta_cluster_id = ''.join(eids_sorted)
        return meta_cluster_id

    def get_estc_ids_str(self):
        return ' '.join(list(self.estc_ids))

    def get_cluster_ids_str(self):
        return ' '.join(list(self.cluster_ids))

    def __repr__(self):
        estc_ids_str = self.get_estc_ids_str()
        cluster_ids_str = self.get_cluster_ids_str()
        return_str = ("ESTC ids: " + estc_ids_str + "\n" +
                      "clusters: " + cluster_ids_str)
        return return_str

    def get_dict_for_dump(self):
        key = self.get_meta_cluster_id()
        estc_ids_str = self.get_estc_ids_str()
        cluster_ids_str = self.get_cluster_ids_str()
        ret_dict = {'key': key,
                    'estc_ids': estc_ids_str,
                    'cluster_ids': cluster_ids_str}
        return ret_dict



# TODO
# -create cluster-object
# -create object enriched book metadata & quote text
