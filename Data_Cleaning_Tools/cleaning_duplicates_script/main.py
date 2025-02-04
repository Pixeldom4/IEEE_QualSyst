import os
import tkinter as tk
from tkinter import filedialog
from flag_duplicates import flag_duplicates  # Import flagging function
from remove_duplicates import remove_duplicates  # Import duplicate removal function
from get_levenshtein_distances import calculate_min_levenshtein_distances  # Import Levenshtein function


def select_file():
    """Opens a file dialog to select the CSV file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")],
        initialdir=os.path.join(os.path.expanduser("~"), "PycharmProjects", "IEEE_QualSyst", "Databases",
                                "relevance_algo_training_data")
    )
    return file_path if file_path else None


def choose_action(file_path):
    """Prompts the user to select an action and runs the corresponding function on the selected file."""

    actions = {
        "1": "Flag duplicates",
        "2": "Calculate Levenshtein distances",
        "3": "Remove duplicates",
        "4": "Exit"
    }

    while True:
        # Display menu
        print("\n Choose an action:")
        print("Note: Must do 2 before 3")
        for key, action in actions.items():
            print(f"{key}. {action}")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice not in actions:
            print("\n Invalid choice. Please enter a number from 1 to 4.")
            continue

        if choice == "4":
            print("\n Exiting program.")
            break

        print(f"\n Processing file: {file_path}")

        try:
            if choice == "1":
                print(f"\n Running duplicate flagging on {file_path}...")
                flagged_file = flag_duplicates(file_path)
                print(f"\n Flagging completed. Updated file saved at: {flagged_file}")

            elif choice == "2":
                print(f"\n Calculating Levenshtein distances for {file_path}...")
                distance_file = calculate_min_levenshtein_distances(file_path)
                print(f"\n Distance calculations completed. Updated file saved at: {distance_file}")

            elif choice == "3":
                # Ensure we use the correct path with "_with_distances"
                file_path_with_distances = file_path.replace(".csv", "_with_distances.csv")

                # Check if the "_with_distances.csv" file exists before proceeding
                if not os.path.exists(file_path_with_distances):
                    print(f"\n Error: Expected file '{file_path_with_distances}' not found. Run Levenshtein analysis first.")
                    continue

                print(f"\n Removing duplicates from {file_path_with_distances}...")
                cleaned_file = remove_duplicates(file_path_with_distances)
                print(f"\n Duplicates removed. Cleaned file saved at: {cleaned_file}")


        except Exception as e:
            print(f"\n An error occurred while processing {file_path}: {e}")


if __name__ == "__main__":
    print("\n Please select the CSV file to process.")
    file_path = select_file()

    if file_path:
        print(f"\n Selected file: {file_path}")
        choose_action(file_path)
    else:
        print("\n No file selected. Exiting program.")
