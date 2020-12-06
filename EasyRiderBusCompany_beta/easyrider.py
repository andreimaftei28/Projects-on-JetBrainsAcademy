# Write your awesome code here
import json
import re

class EasyRider:

    def __init__(self ,data):
        self.data = json.loads(data)
        self.errors = {}

    def find_errors(self):
        data_names = ["bus_id", "stop_id", "stop_name", "next_stop", "stop_type", "a_time"]
        self.errors = dict.fromkeys(data_names, 0)
        for dct in self.data:
            if type(dct["bus_id"]) != int:
                self.errors["bus_id"] += 1
            if type(dct["stop_id"]) != int:
                self.errors["stop_id"] += 1
            if type(dct["stop_name"]) != str or dct["stop_name"] == "":
                self.errors["stop_name"] += 1
            if type(dct["next_stop"]) != int:
                self.errors["next_stop"] += 1
            if type(dct["stop_type"]) != str or len(dct["stop_type"]) > 1:
                self.errors["stop_type"] += 1
            if type(dct["a_time"]) != str or dct["a_time"] == "":
                self.errors["a_time"] += 1
        return self.errors

    def find_format_errors(self):

        required = ["stop_name", "stop_type", "a_time"]
        self.errors = dict.fromkeys(required, 0)
        name_template = r"[A-Z]\w+\s?\w+?\s(Road|Avenue|Boulevard|Street)$"
        type_template = r'^$|[SOF]{1}$'
        hour_template = r"([01]\d|2[0-3]):([0-5]\d)$"
        for dct in self.data:
            if not re.match(name_template, dct["stop_name"]):
                self.errors["stop_name"] += 1
            if not re.match(type_template, dct["stop_type"]):
                self.errors["stop_type"] += 1
            if not re.match(hour_template, dct["a_time"]):
                self.errors["a_time"] += 1
        return self.errors

    def number_of_stops(self):

        errors = self.find_errors()
        if sum(list(errors.values())) == 0:
            errors = self.find_format_errors()
        else:
            self.print_output()
        if sum(list(errors.values())) == 0:
            bus_stops = {}
        else:
            self.print_format_errors()
        for dct in self.data:
            if dct["bus_id"] not in bus_stops:
                bus_stops[dct["bus_id"]] = 1

            else:
                bus_stops[dct["bus_id"]] += 1

        return bus_stops

    def special_stops(self):
        check_start_stop = {}
        for dct in self.data:
            check_start_stop.setdefault(dct["bus_id"], []).append(dct["stop_type"])

        for key in check_start_stop:
            if  not "S" in check_start_stop[key] or not "F" in check_start_stop[key]:
                return f"There is no start or end stop for the line: {key}."
            else:
                stop_ids = [dct["stop_id"] for dct in self.data]
                next_stops = [dct["next_stop"] for dct in self.data]
                start_stops = {dct["stop_name"] for dct in self.data if dct["stop_id"] not in next_stops}
                transfer_stops = {dct["stop_name"] for dct in self.data if stop_ids.count(dct["stop_id"]) > 1}
                finish_stops = {dct["stop_name"] for dct in self.data if dct["next_stop"] not in stop_ids}


        return start_stops, transfer_stops, finish_stops



    def check_time(self):
        time_checker = {}
        data = self.data
        for i in range(len(data) - 1):

            if data[i]["bus_id"] == data[i + 1]["bus_id"]:
                while True:
                    if not data[i]["a_time"] < data[i + 1]["a_time"]:
                        time_checker.setdefault(data[i + 1]["bus_id"], []).append(data[i+1]["stop_name"])
                        break
                    break
            else:
                continue


        if time_checker:
            for key, value in time_checker.items():
                print(f"bus_id line: {key}: wrong time on station {value[0]}")
        else:
            print(f"Arival time test:\nOK")

    def validate_on_demand_stops(self):

        start_stops, transfer_stops, finish_stops = self.special_stops()
        special_stops = start_stops | transfer_stops | finish_stops

        errors = [dct["stop_name"] for dct in self.data if dct["stop_type"] == "O" and dct["stop_name"] in special_stops]
        print("On demand stops test:")
        if len(errors) == 0:
            print("OK")
        else:
            errors.sort()
            print(f"Wrong stop type: {errors}")

        return


    def print_special_stops(self):

        my_data = self.special_stops()
        if isinstance(my_data, str):
            print(my_data)
        else:
            start_stops, transfer_stops, finish_stops = my_data
            print(f"Start stops: {len(start_stops)} {sorted(start_stops)}")
            print(f"Transfer stops {len(transfer_stops)} {sorted(transfer_stops)}")
            print(f"Finish stops: {len(finish_stops)} {sorted(finish_stops)}")

        return


    def print_output(self):
        my_data = self.find_errors()
        print(f"Type and required field validation: {sum(list(self.errors.values()))}")
        for key, value in my_data.items():
            print(f"{key}: {value}")

        return

    def print_format_errors(self):

        my_data = self.find_format_errors()
        print(f"Format validation: {sum(list(self.errors.values()))} errors")
        for key, value in my_data.items():
            print(f"{key}: {value}")

        return

    def print_bus_stops(self):

        my_data = self.number_of_stops()
        print("Line names and number of stops: ")
        for key, value in my_data.items():
            print(f"bus_id: {key}, stops: {value}")

        return

if __name__ == "__main__":
    easy = EasyRider(input())
    #easy.print_output()
    #easy.print_format_errors()
    #easy.print_bus_stops()
    #easy.print_special_stops()
    #easy.check_time()
    easy.validate_on_demand_stops()
