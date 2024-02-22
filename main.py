# Robert Wright
# Student Id: 010924506


import csv
from datetime import datetime, timedelta
from hashfunction import PackageHashTable

# Cite: SV File Reading and Writing. (n.d.-b). Python Documentation. https://docs.python.org/3/library/csv.html
# Load package data. Indexs over the selected rows.
address_dict = {}
package_row_numbers = set()
with open('packages.csv', 'r') as package1:
    reader_package = csv.reader(package1)
    for idx, package in enumerate(reader_package):
        package_row_numbers.add(str(idx))


package_hash_table = PackageHashTable()


#------------------------Create Package Class-------------------------------------
class Package:
    def __init__(self, id, delivery_address, delivery_deadline, delivery_city, zip_code, weight, status, delivery_time=None, departure_time=None):
        self.id = id
        self.delivery_address = delivery_address
        self.delivery_deadline = self._parse_time(delivery_deadline)
        self.delivery_city = delivery_city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = self._parse_time(delivery_time)
        self.departure_time = self._parse_time(departure_time)

    #Cite: How To Convert a String to a datetime or time Object in Python. DigitalOcean. https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
    # Convert the string in the csv to datetime objects.
    def _parse_time(self, delivery_time):
        """ Converts a time input to a datetime object if it's a string. """
        if isinstance(delivery_time, datetime):
            return delivery_time.time()  # Return the time part of the datetime object.
        elif isinstance(delivery_time, str):
            try:
                # Parse only the time.
                return datetime.strptime(delivery_time, '%H:%M').time()
            except ValueError:
                """print(f"Invalid time format: {delivery_time}. Expected format: HH:MM")"""
                return None
        else:
            return None

    # Update the status of the package status based on user_time input.
    #Space-TIme Complexity O(1)
    def update_status(self, user_time):
        """ Updates the status of the package based on the given user_time. """
        if self.delivery_time and user_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time and self.delivery_time and self.departure_time <= user_time < self.delivery_time:
            self.status = "At Hub"
        else:
            self.status = "In Transit"

    def __str__(self):
        return f"Package ID: {self.id}, Delivery Address: {self.delivery_address}, Status: {self.status}"


# Creates a function for the package data. Then package data is placed in the hash table
def load_package_data(package_data, package_hash_table):
    for package in package_data:
        id, delivery_address, delivery_city, delivery_zip_code, delivery_deadline, package_weight, *_ = package
        package_obj = Package(
            id=id,
            delivery_address=delivery_address,
            delivery_deadline=delivery_deadline,
            delivery_city=delivery_city,
            zip_code=delivery_zip_code,
            weight=package_weight,
            status="At hub"
        )
        package_hash_table.insert(id, package_obj)
        """print(f"Loaded package {package_obj}")  # Print each package loaded"""


# Calls the function because it has been defined
with open('packages.csv', 'r') as package1:
    reader_package = csv.reader(package1)
    load_package_data(reader_package, package_hash_table)

# After loading all packages, print out the contents of the hash table
for bucket_list in package_hash_table.table.values():
    for pair in bucket_list:
        package = pair[1]
        """print(f"Package in hash table: {package}")  # Print statement added"""


# Space-Time Complexity O(n), iterates over each row in reader_distance_list
distances = []
with open('distance.csv', 'r') as distance1:
    reader_distance = csv.reader(distance1)
    # Converting csv reader object into list
    reader_distance_list = list(reader_distance)
    for i, row in enumerate(reader_distance_list):  # replacing reader_distance with reader_distance_list
        if str(i) in package_row_numbers:
            distances.append(row)

# Space-Time Complexity O(1)
def distance_table(x_value, y_value, reader_distance_list):
    # Ensuring we don't try to access an out-of-bounds index.
    if x_value < len(reader_distance_list) and y_value < len(reader_distance_list[0]):
        return reader_distance_list[x_value][y_value] or reader_distance_list[y_value][x_value]
    else:
        return 0.0  # Or handle appropriately
        # Print statement moved inside else part


# While calling delivering_packages() function replace reader_distance with reader_distance_list
# Space-Time Complexity O(n) Iterates over each row to check for addresses.
def address_to_index(address):
    with open('addresses.csv', 'r') as addresses1:
        reader_address = csv.reader(addresses1)
        for row in reader_address:
            if address == row[2]:  # Consider using an exact match instead of 'in' for precision
                return int(row[0])
    return None  # Explicitly return None if no address is found


def parse_time(time_str, truck_id=None):
    if time_str is None:  # Handle None case
        return None
    try:
        # Parse only the time part from the string.
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()
        return time_obj
    except ValueError:
        if truck_id:
            """print(f"Time format is incorrect for truck {truck_id}: {time_str}")"""
        else:
            """print("Invalid time format. Expected format: HH:MM AM/PM")"""
        return None


...
class DeliveryTruck:
    def __init__(self, truck_id, available_at_time):
        self.truck_id = truck_id
        self.packages = []
        self.total_mileage = 0
        self.current_location = 0
        self.available_at_time = parse_time(available_at_time, truck_id)
        self.time = self.available_at_time
        self.returned = False

    # add this method instance to the class
    def load_packages(self, packages):
        self.packages.extend(packages)  # Use extend to add to the existing list of packages
        """print(f"Loaded packages onto {self.truck_id}: {self.packages}")  # Print statement added"""





# Prepare the delivery truck for manual loadind. Truck 3 leaves when truck 1 returns and
# contains package with corrected address.
truck1 = DeliveryTruck("Truck 1", "8:00 AM")
truck1.load_packages([1, 13, 14, 15, 16, 20, 21, 29, 30, 34, 37, 40])

truck2 = DeliveryTruck("Truck 2", "9:05 AM")
truck2.load_packages([3, 4, 5, 6, 12, 17, 18, 23, 25, 26, 28, 31, 32, 36, 38])

truck3 = DeliveryTruck("Truck 3", "11:30 AM")
truck3.load_packages([2, 7, 8, 9, 10, 11, 19, 22, 24, 27, 33, 35, 39])


trucks = [truck1, truck2, truck3]

# Define speed limit
SPEED_LIMIT = 18



# Cite: Python  datetime.timedelta  function. https://www.geeksforgeeks.org/python-datetime-timedelta-function/
# Function for using only the time parameter.
# Then used with truck.available_at_time to update time after each package delivery.
# Overall Space-Time Complexity O(1), space doesn't depend on size input
def add_hours_to_time(original_time, hours_to_add):
    # Combine the original time with today's date
    combined_datetime = datetime.combine(datetime.today(), original_time)
    # Add the hours
    new_datetime = combined_datetime + timedelta(hours=hours_to_add)
    # Return only the time part
    return new_datetime.time()

#----------------------------------------Algorithm-------------------------------------------------------
#Cite:K Nearest neighbours — Introduction to machine learning algorithms. Medium. https://towardsdatascience.com/k-nearest-neighbours-introduction-to-machine-learning-algorithms-18e7ce3d802a
# Nearest Neighbor Algo Begins by checking un-delivered packages by shortest distance.
# Overall Time Complexity O(n) iterates over 'n' un_delivered packages.
def find_closest_package(truck, undelivered_packages, reader_distance):
    closest_package = None
    shortest_distance = float('inf')
    for package in undelivered_packages: # Time Complexity O(n)
        current_location = truck.current_location
        destination = address_to_index(package.delivery_address) # Time Complexity O(1)
        distance = float(distance_table(current_location, destination, reader_distance)) # Time Complexity O(1)
        if distance < shortest_distance:
            shortest_distance = distance
            closest_package = package
        """print(f"Checking package {package.id}, current shortest distance: {shortest_distance}")"""
    return closest_package, shortest_distance

# Overall Space Time Complexity O(1), does not require space that grows with data
def update_truck_after_delivery(truck, package, shortest_distance):
    # Update truck's current location and total mileage
    truck.current_location = address_to_index(package.delivery_address)
    truck.total_mileage += shortest_distance # Space-Time Complexity O(1)

    # Update delivery time
    if truck.available_at_time is not None:
        truck.available_at_time = add_hours_to_time(truck.available_at_time, shortest_distance / SPEED_LIMIT) # Space-Time Complexity O(1)
    else:  # Handle the case when truck.time is None
        truck.available_at_time = datetime.now()
        truck.available_at_time = add_hours_to_time(datetime.now().time(), shortest_distance / SPEED_LIMIT) #Space-Time Compleixty O(1)
    package.delivery_time = truck.time
    """print(f"Delivered package {package.id} at {package.delivery_time}")"""
    """print(f"Current mileage for {truck.truck_id}: {truck.total_mileage}")"""


# delivering_packages function updates the status of a package based on the truck's time.
# This create a Nearest Neighbor Algorithm
# Overall Space-Time Complexity O(n^2).
def delivering_packages(truck, package_hash_table, reader_distance_list):
    undelivered_packages = [package_hash_table.lookup(str(packageID)) for packageID in truck.packages] # Space-Time Complexity O(n)
    if None in undelivered_packages:  # Space-Time O(n), scans through list once.
        """print(f"Missing package in hash table for {truck.truck_id}!")"""
    # Iterates as long as there are packages.
    #Space-Time Complexity O(n^2), decreased by 1 package each iteration.
    while undelivered_packages:
        closest_package, shortest_distance = find_closest_package(truck, undelivered_packages, reader_distance_list)
        if closest_package:
            # Set departure time and update status
            if truck.available_at_time:
                closest_package.departure_time = truck.available_at_time
                closest_package.update_status(truck.available_at_time)

            # Deliver the package and update truck details
            update_truck_after_delivery(truck, closest_package, shortest_distance)

            # Set the actual delivery time and update status again
            closest_package.delivery_time = truck.available_at_time
            closest_package.update_status(truck.time)

            # Remove package from truck and undelivered list
            truck.packages.remove(int(closest_package.id))
            undelivered_packages.remove(closest_package)


for truck in trucks:
    delivering_packages(truck, package_hash_table, reader_distance_list)



# Truck 1 delivers Package 13 that's 7.6 miles away from hub. truck1_distance_hub will be added to truck1's total distance.
# There is no concern for time due to Truck 3 leaving until 11:30am and Truck 1 finishing at 9:19am
truck1_distance_hub = 7.6
# Truck1 drive to hub added to total distance.
truck1.total_mileage += truck1_distance_hub
# Total combine distance of all trucks
total_combined_mileage = truck1.total_mileage + truck2.total_mileage + truck3.total_mileage


# Loops over values of hash table. Time depends on # of buckets.
# Space Time Complexity O(n)
def process_packages(package_hash_table, process_package_func):
    for bucket_list in package_hash_table.table.values():
        for pair in bucket_list:
            package = pair[1]
            process_package_func(package)


class UserInterface:

    # Function to get the user_input of a time and convert to datetime obj,
    @staticmethod
    def get_input_time():
        time_str = input("Enter time in format HH:MM: ")
        try:
            user_time = datetime.strptime(time_str, "%H:%M").time()  # Extract only the time part
            return user_time
        except ValueError:
            """print("Invalid time format. Expected format: HH:MM")"""
            return None
    def header_message():
        print('Create by: Robert Wright')
        print('▪︎' * 100)
        print('                         WGUPS - Packet Tracking ™                              ')
        print('▪' * 84)
        print('● Truck 1 total distance: ', "{0:.2f}".format(truck1.total_mileage, 2),
              'miles')
        print('● Truck 2 total distance: ', "{0:.2f}".format(truck2.total_mileage, 2),
              'miles')
        print('● Truck 3 total distance: ', "{0:.2f}".format(truck3.total_mileage, 2),
              'miles')
        print('-' * 50)
        print('Total distance of all trucks: ', "{0:.2f}".format(total_combined_mileage, 2),
              'miles')
        print('▪'*50)
# Home UI Layout
    header_message()
    while True:
        print("MENU OPTIONS:")
        print("1. Check status of all packages based on specific time")
        print("2. Check status of individual packages")
        print("3. Exit Program")
        choice = input("ENTER CHOICE:")

        # total delivery package for all 40 packets


        if choice == "1":
            header_message()
            user_time = get_input_time()
            print('Package ID:'.ljust(15) + 'Address:'.ljust(40) + 'Status:'.ljust(20) + 'Delivery time:')
            print('-'* 90)
            if user_time:
                for bucket_list in package_hash_table.table.values():
                    for pair in bucket_list:
                        package = pair[1]
                        package.update_status(user_time)

                        # Format and print package information
                        formatted_string = (
                                f" • {package.id}".ljust(15) +
                                f"{package.delivery_address}".ljust(40) +
                                f"{package.status}".ljust(20)
                        )

                        # Append delivery time if the package is not in transit or at the hub
                        if package.status.lower() not in ['in transit', 'at hub']:
                            formatted_string += f"{package.delivery_time}"

                        print(formatted_string)

        elif choice == '2':
            user_time = get_input_time()
            if user_time:
                package_id = input("Enter Package ID: ")
                print("Checking status of individual package")
                package = package_hash_table.lookup(package_id)
                if package:
                    package.update_status(user_time)
                    header_message()
                    # Check if the package is still in transit or at the hub
                    if package.status.lower() in ['In transit', 'At hub']:
                        print(f"● Package {package.id}\n ● Address: {package.delivery_address}\n ● Status: {package.status}\n")
                    else:
                        print(
                            f"● Package {package.id}\n ● Address: {package.delivery_address}\n ● Status: {package.status}\n ● Delivered at: {package.delivery_time}\n")
                else:
                    print("Package not found")
        elif choice == '3':
            print("Exiting Program")
            break
        else:
            print("Invalid choice. Choose: 1,2,3")

