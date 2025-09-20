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
            print(i)
            file.write(i)


def main():
    csv_path = html_to_csv('input.html')
    clean_csv(csv_path)
    print("Output path:", csv_path)


if __name__ == "__main__":
    main()
