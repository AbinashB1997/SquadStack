import fileinput # fileinput package allow us to get file as an input

class parkingSlotData:
    def __init__(self):
        """
        Initial declarations
        """
        self.ParkingLotSpace = 0
        self.Total_Available_Slots = 0
        self.Current_slot = 0
        self.Total_Occupied_Slots = 0
        self.Slots = list()
        self.Slot_numbers_By_Age = dict()
        self.Slot_numbers_By_Vehicle_Number = dict()
        self.Vehicle_Number_By_Age = dict()
        self.Age_By_Vehicle_Number = dict()


    def get_closest_available_slot(self):
        """
        get_closest_available_slot method will return the closest available slot if found, otherwise it will
        return -1(It means no slots are available)
        """
        for i in range(len(self.Slots)):
            if(self.Slots[i] == 0):
                return i
        return -1


    def get_vehicle_number_by_slot(self, slot):
        """
        get_vehicle_number_by_slot method returns the vehicle number at a given slot
        """
        for car_number, slot_number in self.Slot_numbers_By_Vehicle_Number.items():
            if(slot == slot_number):
                return car_number
        return "KeyNotFound" # If slot not found


    def Create_parking_lot(self, slots):
        """
        Create_parking_lot method will create given number of space for the parkingLot
        """
        if(self.Total_Available_Slots == 0):
            self.Total_Available_Slots = slots
            self.Slots = [0] * slots
            self.Current_slot = 0 # 0 based indexing
            print('Created parking of {0} slots'.format(slots))
        else:
            print("No slots are available")

    def vehicle_not_in_entry(self, Vehicle_Number):
        """
        vehicle_not_in_entry method will check whether the given vehicle already existing
        """
        for car_number in self.Slot_numbers_By_Vehicle_Number.keys():
            if(car_number == Vehicle_Number):
                return False
        return True # If entry not found


    def Park_Vehicle(self, Vehicle_Number, Driver_Age):
        """
        Park_Vehicle method will create an entry of the Vehicle and driver's information in the system
        Constraints: A vehicle will be allowed to park iff at least one slot is available
        """
        if(self.Total_Occupied_Slots < self.Total_Available_Slots and self.vehicle_not_in_entry(Vehicle_Number)):
            nearest_available_slot_position = self.get_closest_available_slot()
            if(nearest_available_slot_position < self.Current_slot):
                self.Slots[nearest_available_slot_position] = 1
                self.Slot_numbers_By_Vehicle_Number[Vehicle_Number] = nearest_available_slot_position + 1

                # Appending the slot_number with given driver_age

                if Driver_Age in self.Slot_numbers_By_Age.keys():
                    self.Slot_numbers_By_Age[Driver_Age] += str(nearest_available_slot_position + 1) + ","
                else:
                    self.Slot_numbers_By_Age[Driver_Age] = str(nearest_available_slot_position + 1) + ","

                # Appending the vehicle_number with given driver_age

                if Vehicle_Number in self.Vehicle_Number_By_Age.keys():
                    self.Vehicle_Number_By_Age[Driver_Age] += Vehicle_Number + ","
                else:
                    self.Vehicle_Number_By_Age[Driver_Age] = Vehicle_Number + ","

                self.Age_By_Vehicle_Number[Vehicle_Number] = Driver_Age
                self.Total_Available_Slots -= 1
                self.Total_Occupied_Slots += 1
                print('Car with vehicle registration number "{0}" has been parked at slot number {1}'.format(Vehicle_Number, nearest_available_slot_position + 1))
            else:
                self.Slots[self.Current_slot] = 1
                self.Slot_numbers_By_Vehicle_Number[Vehicle_Number] = self.Current_slot + 1

                # Appending the slot_number with given driver_age

                if Driver_Age in self.Slot_numbers_By_Age.keys():
                    self.Slot_numbers_By_Age[Driver_Age] += str(self.Current_slot + 1) + ","
                else:
                    self.Slot_numbers_By_Age[Driver_Age] = str(self.Current_slot + 1) + ","

                # Appending the vehicle_number with given driver_age

                if Vehicle_Number in self.Vehicle_Number_By_Age.keys():
                    self.Vehicle_Number_By_Age[Driver_Age] += Vehicle_Number + ","
                else:
                    self.Vehicle_Number_By_Age[Driver_Age] = Vehicle_Number + ","

                self.Age_By_Vehicle_Number[Vehicle_Number] = Driver_Age
                print('Car with vehicle registration number "{0}" has been parked at slot number {1}'.format(Vehicle_Number, self.Current_slot + 1))
                self.Current_slot += 1
                self.Total_Available_Slots -= 1
                self.Total_Occupied_Slots += 1
        else:
            print("No slots are available or Car is already in parking slot")

    def get_slots_by_age(self, age):
        """
        get_slots_by_age method returns all the slots occupied by the driver of given age
        """
        if age in self.Slot_numbers_By_Age.keys():
            slots = self.Slot_numbers_By_Age[age]
            print(slots[:-1]) # Since there will be an extra comma at the end of the slots string
        else:
            print("null")


    def get_slot_by_car_number(self, Vehicle_Number):
        """
        get_slot_by_car_number method returns the slot number occupied with the car by it's number
        """
        if Vehicle_Number in self.Slot_numbers_By_Vehicle_Number.keys():
            slot = self.Slot_numbers_By_Vehicle_Number[Vehicle_Number]
            print(slot)
        else:
            print(-1)

    def get_vehicle_numbers_by_age(self, age):
        """
        get_vehicle_numbers_by_age method returns all the parked vehicle number by given driver age
        """
        if age in self.Vehicle_Number_By_Age.keys():
            vehicles = self.Vehicle_Number_By_Age[age]
            print(vehicles[:-1]) # Since there will be an extra comma at the end of the vehicle_numbers string
        else:
            print("null")


    def leave(self, slot):
        """
        leave method will make the given slot available for other customers
        This method will remove the data of the customer who is leaving
        """
        if(slot < len(self.Slots) and self.Slots[slot] == 1):
            car_number = self.get_vehicle_number_by_slot(slot + 1)
            if(car_number == "KeyNotFound"):
                print("Slot already available")
            else:
                self.Slots[slot] = 0
                self.Total_Available_Slots += 1
                self.Total_Occupied_Slots -= 1
                age_of_driver = self.Age_By_Vehicle_Number[car_number]
                vehicles = self.Vehicle_Number_By_Age[age_of_driver]
                slots = self.Slot_numbers_By_Age[age_of_driver]

                # Removing the age of the customer who had parked the car

                if(slots.count(',') > 1):
                    slots = slots[ : slots.index(str(slot + 1))] + slots[slots.index(str(slot + 1)) + 2 : ]
                    self.Slot_numbers_By_Age[age_of_driver] = slots
                else:
                    del self.Slot_numbers_By_Age[age_of_driver]

                # Removing the parked vehicle_number at given slot

                if(vehicles.count(',') > 1):
                    vehicles = vehicles[ : vehicles.index(car_number)] + vehicles[vehicles.index(car_number) + len(car_number) + 1 : ]
                    self.Vehicle_Number_By_Age[age_of_driver] = vehicles
                else:
                    del self.Vehicle_Number_By_Age[age_of_driver]

                # Removing the slot_number where the customer had parked the car

                del self.Slot_numbers_By_Vehicle_Number[car_number]
                print('Slot number {0} vacated, the car with vehicle registration number "{1}" left the space, the driver of the car was of age {2}'.format(slot + 1, car_number, age_of_driver))
        else:
            print("Slot already available")



if __name__ == '__main__':
    obj = parkingSlotData()
    for line in fileinput.input(files =('query.txt')):
        values = line.split()
        if(values[0] == 'Park'):
            obj.Park_Vehicle(values[1], int(values[3]))
        elif(values[0] == 'Slot_numbers_for_driver_of_age'):
            obj.get_slots_by_age(int(values[1]))
        elif(values[0] == 'Slot_number_for_car_with_number'):
            obj.get_slot_by_car_number(values[1])
        elif(values[0] == 'Vehicle_registration_number_for_driver_of_age'):
            obj.get_vehicle_numbers_by_age(int(values[1]))
        elif(values[0] == 'Create_parking_lot'):
            obj.Create_parking_lot(int(values[1]))
        elif(values[0] == 'Leave'):
            obj.leave(int(values[1]) - 1)