import os
import json

class Reservation:
    def __init__(self, table_number, time, people, status="Pending"):
        self.table_number = table_number
        self.time = time
        self.people = people
        self.status = status

class ReservationModelAndData:
    def __init__(self):
        self.staticData = []
        self.db_path = os.path.join(os.getcwd(), "DBFilesJson", "dutchman_reservation.json")
        self.loadData()

    def loadData(self):
        #Load reservation data from JSON file into a list of Reservation objects.
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.staticData = [Reservation(**res) for res in data]
        else:
            with open(self.db_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def saveData(self):
        #Save the list of Reservation objects to the JSON file.
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump([res.__dict__ for res in self.staticData], file, ensure_ascii=False, indent=4)

    def add_reservation(self, table_number, time, people):
       #Add a new reservation and save it.
        new_reservation = Reservation(table_number, time, people)
        self.staticData.append(new_reservation)
        self.saveData()

    def update_reservation_status(self, index, new_status):
        #Update the status of a reservation at the given index.
        if 0 <= index < len(self.staticData):
            self.staticData[index].status = new_status
            self.saveData()

    def get_reservations(self):
        #Return the list of all reservations.
        return self.staticData
    
    def remove_reservation(self, index):
        if 0 <= index < len(self.staticData):
            del self.staticData[index]
            self.saveData()