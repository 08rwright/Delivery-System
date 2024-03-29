# Cite: Reference for hash table zyBooks: Figure 7.8.2: Hash table using chaining.
class PackageHashTable:
    def __init__(self, initial_capacity=40):
        self.table = {i: [] for i in range(initial_capacity)}

    def hash_function(self, key):
        return hash(key) % len(self.table)

     # Inserts, updates and retrieves the bucket list where item will go.
    def insert(self, key, item):
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Lookup items in hash table
    def lookup(self, key):
        bucket = hash(key) % len(self.table)  # corrected from self.list to self.table
        bucket_list = self.table[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None  # no pair[0] matches key 0

    # Hash remove method - removes item from hash table
    def hash_remove(self, key):
        slot = hash(key) % len(self.table)    # corrected from self.list to self.table
        destination = self.table[slot]        # corrected from self.list to self.table

        # If the key is found in the hash table then remove the item
        if key in destination:
            destination.remove(key)



