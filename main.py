import xml.etree.ElementTree as ET
from database import DatabaseConnection

metric_names = ["HeartRate", "StepCount", "DistanceWalkingRunning", "ActiveEnergyBurned", "BasalEnergyBurned", "AppleExerciseTime", "EnvironmentalAudioExposure",
                "HeadphoneAudioExposure", "WalkingDoubleSupportPercentage", "AppleStandTime", "WalkingStepLength", "OxygenSaturation", "RespiratoryRate"]


def parse_xml_data(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        return root
    except OSError:
        print("Error: Unable to open file!")
        exit(1)


def parse_date(input_date):
    date, time, *extra = input_date.split(' ')
    return f"{date} {time}"


def extract_field(root, fieldname):
    data = []
    for child in root:
        if(child.attrib.get('type') == f"HKQuantityTypeIdentifier{fieldname}"):
            each_row = (parse_date(child.attrib.get('creationDate')), parse_date(child.attrib.get(
                'startDate')), parse_date(child.attrib.get('endDate')), child.attrib.get('value'))
            data.append(each_row)
    return data


def batch_insert(db, data, metric_name):
    start, end = 0, 50000
    while(start < len(data)):
        db.insert_data(data[start:end], metric_name)
        start, end = end, end + 50000
        if(end > len(data)):
            diff = end - len(data)
            end = end - diff


if __name__ == "__main__":
    db = DatabaseConnection()

    # Create Database
    db.create_db("applehealthreport")

    # Crete Tables
    for each_metric in metric_names:
        db.create_table(each_metric)

    # Parse XML data
    root = parse_xml_data("data/export.xml")

    # Insert data to respective field
    for each_metric in metric_names:
        print(f"inserting {each_metric}")
        data = extract_field(root, each_metric)
        if(len(data) > 50000):
            batch_insert(db, data, each_metric)
        else:
            db.insert_data(data, each_metric)
