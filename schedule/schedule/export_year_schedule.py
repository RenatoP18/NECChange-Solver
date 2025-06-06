import matplotlib.pyplot as plt
import json
import os


def create_schedule(year, semester, schedule_data):
    # Initialize the table
    days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    times = [
        "9h-10h",
        "10h-11h",
        "11h-12h",
        "12h-13h",
        "13h-14h",
        "14h-15h",
        "15h-16h",
        "16h-17h",
        "17h-18h",
        "18h-19h",
        "19h-20h",
    ]
    table = [["" for _ in range(5)] for _ in range(11)]
    overlaps = {}
    
    print(schedule_data)

    # Populate the table with schedule data
    for entry in schedule_data:
        if entry["year"] == year and entry["semester"] == semester:
            for slot in entry["slots"]:
                day = days.index(slot[0])
                start_time = int(slot[1]) - 9
                end_time = int(slot[3]) - 9
                course = "".join(filter(str.isupper, entry["uc"]))
                type_class = entry["type_class"]
                shift = entry["shift"]
                slot_info = f"{course} {type_class}{shift}"

                # Check for overlapping slots
                for i in range(start_time, end_time):
                    print(i, day)
                    if table[i][day] != "":
                        if (i, day) in overlaps:
                            overlaps[(i, day)].append(slot_info)
                        else:
                            overlaps[(i, day)] = [table[i][day], slot_info]
                    table[i][day] = slot_info

    # Mark overlapping slots with combined information
    for overlap, info in overlaps.items():
        i, day = overlap
        existing_info = "/".join(info)
        table[i][day] = existing_info

    # Create the table as a plot with increased size and colors
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")
    cell_colors = [["white" for _ in range(5)] for _ in range(11)]
    for i in range(11):
        for j in range(5):
            if table[i][j] != "":
                if (i, j) in overlaps:
                    cell_colors[i][j] = "lightgray"
                else:
                    cell_colors[i][j] = "lightblue"
    table = ax.table(
        cellText=table,
        cellColours=cell_colors,
        cellLoc="center",
        loc="center",
        colLabels=days,
        rowLabels=times,
    )
    table.scale(1, 2)  # Increase the row height for better readability
    table.auto_set_font_size(False)  # Disable automatic font size adjustment

    for cell in table.get_celld().values():
        cell.set_fontsize(12)  # Set the font size of the cells

    if os.path.relpath(__file__) == "export_year_schedule.py":
        folder_path = "year_semester_schedule_png"
    else:
        folder_path = os.path.join(".", "..", "schedule", "schedule", "output", "year_semester_schedule_png")

    os.makedirs(folder_path, exist_ok=True)

    # Save the plot as a PNG image in the folder
    filename = os.path.join(folder_path, f"schedule_{year}_{semester}.png")

    plt.savefig(filename, bbox_inches="tight", pad_inches=0.4)
    plt.close()


# Load the schedule data from the JSON file
if os.path.relpath(__file__) == "export_year_schedule.py":
    data_path = os.path.join(".", "..", "..", "web", "src", "data", "schedule.json")
else:
    data_path = os.path.join(".", "..", "web", "src", "data", "schedule.json")

# print(data_path)

with open(data_path) as file:
    schedule_data = json.load(file)
    # print(schedule_data)

print("Generating schedules...")
# Generate schedules for each year and semester
for year in range(1, 4):
    for semester in range(1, 3):
        create_schedule(str(year), str(semester), schedule_data)
