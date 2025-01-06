import os
import sys
import subprocess

def print_menu():
    print("\n=== Gas Flow Framework CLI ===")
    print("1. Collect data (run entsogData.py)")
    print("2. Prepare data")
    print("3. View inter-country data map (run mapPairs.py)")
    print("4. View country totals map (run mapCountryTotals.py)")
    print("5. View LNG 2019 point data map (run mapLNG_19.py)")
    print("6. View LNG 2023 point data map (run mapLNG_23.py)")
    print("0. Exit")

def run_script(script_name):
    script_path = os.path.join("src", script_name)
    if not os.path.exists(script_path):
        print(f"Error: {script_name} not found in 'src/' directory.")
        return
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Script {script_name} exited with an error.\n{e}")

def main():
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            run_script("entsogData.py")
        elif choice == "2":
            run_script("buildDataPerCountry.py")
            run_script("buildDataPerPointType.py")
        elif choice == "3":
            run_script("mapPairs_FINAL.py")
        elif choice == "4":
            run_script("mapCountryTotals_FINAL.py")
        elif choice == "5":
            run_script("mapLNG_19.py")
        elif choice == "6":
            run_script("mapLNG_23.py")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
