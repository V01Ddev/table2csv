from bs4 import BeautifulSoup
import pandas as pd
import sys
import os


def html_to_csv(input_path: str):

    # Ensuring path exists
    if not os.path.exists(input_path):
        sys.exit("HTML input file not found")
        return None

    input_data = ""

    with open(input_path, 'r') as file:
        for line in file:
            input_data += line

    data = []
    list_header = []

    soup = BeautifulSoup(input_data, 'html.parser')

    header = soup.find_all("tbody")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except Exception as e:
            print(f"Error loading some header: {e}")
            continue

    # for getting the data
    HTML_data = soup.find_all("tbody")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except Exception as e:
                print(f"Error loading some data: {e}")
                continue
        data.append(sub_data)

    dataFrame = pd.DataFrame(data=data, columns=list_header)
    dataFrame.to_csv('out.csv', index=False)
    return "out.csv"


def clean_csv(csv_path: str):
    if not os.path.exists(csv_path):
        sys.exit("CSV input file not found")
        return None

    # Doing this manually because I'm fucking cool
    # Loading data
    new_data = []  # Every line is an item
    try:
        with open(csv_path, 'r') as f_data:
            for line in f_data:
                new_data.append(line)
    except Exception as e:
        print(f"Couldn't load CVS to clean: {e}")

    for index, item in enumerate(new_data):
        if index == 0:
            sd = item.split(',')
            for i in sd:
                og_item = i
                if '.' in i:
                    day, date = i.split('y')
                    fo = f"{day}y {date}"
                    new_data[0] = new_data[0].replace(og_item, fo)
        else:
            # Adding space between time
            new_string = item[0:5] + " " + item[5:-1] + "\n"
            new_data[index] = new_string

    # Writing out data
    with open(csv_path, 'w') as file:
        for i in new_data:
            file.write(i.replace(', ', ','))


def csv_Gcsv(csv_input: str):
    # Converts CSV to Google calender style CSV for import
    # Takes out.csv as input and outputs to GCalender.csv
    output_line = []  # lines to be written to csv
    csv_data = pd.read_csv(csv_input).to_dict(orient='dict')

    times_arr = list(csv_data.get("Hour").values())
    del csv_data["Hour"]

    for date in csv_data:

        lessons = list(csv_data.get(date).values())

        found_lessons = []
        for index, lesson in enumerate(lessons):
            if lesson != "" and lesson not in found_lessons:
                found_lessons.append(lesson)  # Makes sure that a lesson isn't repeated
                if times_arr:
                    start_time = times_arr[index][0:5]
                    end_time = times_arr[index][6:]
                else:
                    print(f"Times columns not found...")
                    exit()

                for c in range(index + 1, len(lessons)):
                    # If lesson is split into two parts, it will be one big block... Known edge case ig
                    if lessons[c] == lesson:
                        end_time = times_arr[c][6:]

                d = date.split(' ')[1]  # date without day bs
                output_line.append(f"{lesson},{d},{start_time},{end_time},False\n")

        # Again writing CSV manually because I'm a absolute fucking machine...
        with open('GCalender.csv', 'w') as output_file:
            output_file.write("Subject,Start Date,Start Time,End Time,All Day Event\n")
            for i in output_line:
                output_file.write(i)


def main():
    csv_path = html_to_csv('input.html')
    clean_csv(csv_path)
    print("Output path:", csv_path)

    print("Converting CSV to Google Calender CSV")
    csv_Gcsv(csv_path)


if __name__ == "__main__":
    main()
