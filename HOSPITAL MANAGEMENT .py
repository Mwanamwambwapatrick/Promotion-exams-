# ================== HOSPITAL MANAGEMENT SYSTEM ==================

# -------------------- DATA STORAGE --------------------
patients = {}


# -------------------- HELPER FUNCTIONS --------------------

def calculate_total_bill(patient_id):
    """Calculate the total bill for a patient."""
    treatments = patients[patient_id]["treatments"]
    return sum(treatments.values())


def display_separator():
    print("-" * 50)


# -------------------- 1. ADD PATIENT --------------------

def add_patient():
    print("\n===== ADD PATIENT =====")

    # Patient ID (must be unique)
    patient_id = input("Enter Patient ID: ").strip()
    if patient_id in patients:
        print(f"Error: Patient ID '{patient_id}' already exists.")
        return

    full_name = input("Enter Full Name: ").strip()

    # Age validation
    while True:
        try:
            age = int(input("Enter Age: "))
            if age <= 0:
                print("Age must be a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    gender = input("Enter Gender (Male/Female/Other): ").strip()
    diagnosis = input("Enter Diagnosis (e.g., Malaria, Flu): ").strip()

    # Collect at least 2 treatments
    treatments = {}
    print("Enter at least 2 treatments with costs:")
    treatment_count = 0
    while True:
        treatment_name = input(f"  Treatment {treatment_count + 1} name (or 'done' if >= 2 added): ").strip()
        if treatment_name.lower() == "done":
            if treatment_count < 2:
                print("  You must enter at least 2 treatments.")
                continue
            else:
                break
        # Cost validation
        while True:
            try:
                cost = float(input(f"  Cost for '{treatment_name}': "))
                if cost <= 0:
                    print("  Cost must be a positive number.")
                else:
                    break
            except ValueError:
                print("  Invalid input. Please enter a number.")
        treatments[treatment_name] = cost
        treatment_count += 1

    patients[patient_id] = {
        "name": full_name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis,
        "treatments": treatments
    }

    print(f"\nPatient '{full_name}' added successfully!")


# -------------------- 2. VIEW ALL PATIENTS --------------------

def view_all_patients():
    print("\n===== ALL PATIENTS =====")
    if not patients:
        print("No patients registered yet.")
        return

    display_separator()
    print(f"{'Patient ID':<12} {'Name':<20} {'Diagnosis':<20}")
    display_separator()
    for pid, info in patients.items():
        print(f"{pid:<12} {info['name']:<20} {info['diagnosis']:<20}")
    display_separator()


# -------------------- 3. VIEW PATIENT REPORT --------------------

def view_patient_report():
    print("\n===== VIEW PATIENT REPORT =====")
    patient_id = input("Enter Patient ID: ").strip()

    if patient_id not in patients:
        print(f"Error: Patient ID '{patient_id}' not found.")
        return

    p = patients[patient_id]
    display_separator()
    print(f"  Patient ID : {patient_id}")
    print(f"  Name       : {p['name']}")
    print(f"  Age        : {p['age']}")
    print(f"  Gender     : {p['gender']}")
    print(f"  Diagnosis  : {p['diagnosis']}")
    print("\n  Treatments & Costs:")
    for treatment, cost in p["treatments"].items():
        print(f"    - {treatment:<25} K{cost:.2f}")
    total = calculate_total_bill(patient_id)
    display_separator()
    print(f"  TOTAL BILL : K{total:.2f}")
    display_separator()


# -------------------- 4. UPDATE PATIENT --------------------

def update_patient():
    print("\n===== UPDATE PATIENT =====")
    patient_id = input("Enter Patient ID to update: ").strip()

    if patient_id not in patients:
        print(f"Error: Patient ID '{patient_id}' not found.")
        return

    p = patients[patient_id]
    print(f"\nUpdating patient: {p['name']}")
    print("  a. Update Diagnosis")
    print("  b. Add New Treatment")
    print("  c. Update Treatment Cost")
    print("  d. Remove Treatment")
    choice = input("Select option (a/b/c/d): ").strip().lower()

    if choice == "a":
        new_diagnosis = input("Enter new diagnosis: ").strip()
        p["diagnosis"] = new_diagnosis
        print("Diagnosis updated successfully.")

    elif choice == "b":
        treatment_name = input("Enter new treatment name: ").strip()
        while True:
            try:
                cost = float(input(f"Enter cost for '{treatment_name}': "))
                if cost <= 0:
                    print("Cost must be a positive number.")
                else:
                    break
            except ValueError:
                print("Invalid input. Enter a number.")
        p["treatments"][treatment_name] = cost
        print(f"Treatment '{treatment_name}' added successfully.")

    elif choice == "c":
        if not p["treatments"]:
            print("No treatments available to update.")
            return
        print("Current treatments:", list(p["treatments"].keys()))
        treatment_name = input("Enter treatment name to update cost: ").strip()
        if treatment_name not in p["treatments"]:
            print(f"Treatment '{treatment_name}' not found.")
            return
        while True:
            try:
                new_cost = float(input(f"Enter new cost for '{treatment_name}': "))
                if new_cost <= 0:
                    print("Cost must be a positive number.")
                else:
                    break
            except ValueError:
                print("Invalid input. Enter a number.")
        p["treatments"][treatment_name] = new_cost
        print(f"Cost for '{treatment_name}' updated successfully.")

    elif choice == "d":
        if not p["treatments"]:
            print("No treatments available to remove.")
            return
        print("Current treatments:", list(p["treatments"].keys()))
        treatment_name = input("Enter treatment name to remove: ").strip()
        if treatment_name not in p["treatments"]:
            print(f"Treatment '{treatment_name}' not found.")
            return
        del p["treatments"][treatment_name]
        print(f"Treatment '{treatment_name}' removed successfully.")

    else:
        print("Invalid option.")


# -------------------- 5. DELETE PATIENT --------------------

def delete_patient():
    print("\n===== DELETE PATIENT =====")
    patient_id = input("Enter Patient ID to delete: ").strip()

    if patient_id not in patients:
        print(f"Error: Patient ID '{patient_id}' not found.")
        return

    patient_name = patients[patient_id]["name"]
    confirm = input(f"Are you sure you want to delete '{patient_name}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        del patients[patient_id]
        print(f"Patient '{patient_name}' deleted successfully.")
    else:
        print("Deletion cancelled.")


# -------------------- 6. SEARCH PATIENT --------------------

def search_patient():
    print("\n===== SEARCH PATIENT =====")
    search_term = input("Enter Patient ID or Name to search: ").strip().lower()

    results = []
    for pid, info in patients.items():
        if search_term == pid.lower() or search_term in info["name"].lower():
            results.append((pid, info))

    if not results:
        print("No matching patients found.")
        return

    display_separator()
    print(f"{'Patient ID':<12} {'Name':<20} {'Diagnosis':<20}")
    display_separator()
    for pid, info in results:
        print(f"{pid:<12} {info['name']:<20} {info['diagnosis']:<20}")
    display_separator()


# -------------------- 7. HOSPITAL STATISTICS --------------------

def hospital_statistics():
    print("\n===== HOSPITAL STATISTICS =====")

    if not patients:
        print("No patients registered yet.")
        return

    total_patients = len(patients)

    # Calculate bills for all patients
    bills = {pid: calculate_total_bill(pid) for pid in patients}
    total_revenue = sum(bills.values())

    highest_bill_id = max(bills, key=bills.get)
    lowest_bill_id = min(bills, key=bills.get)

    display_separator()
    print(f"  Total Number of Patients : {total_patients}")
    print(f"  Total Revenue            : K{total_revenue:.2f}")
    print(f"  Patient with Highest Bill: {patients[highest_bill_id]['name']} "
          f"(ID: {highest_bill_id}) - K{bills[highest_bill_id]:.2f}")
    print(f"  Patient with Lowest Bill : {patients[lowest_bill_id]['name']} "
          f"(ID: {lowest_bill_id}) - K{bills[lowest_bill_id]:.2f}")
    display_separator()


# -------------------- MAIN MENU --------------------

def display_menu():
    print("\n========================================")
    print("       HOSPITAL MANAGEMENT SYSTEM       ")
    print("========================================")
    print("  1. Add Patient")
    print("  2. View All Patients")
    print("  3. View Patient Report")
    print("  4. Update Patient")
    print("  5. Delete Patient")
    print("  6. Search Patient")
    print("  7. Hospital Statistics")
    print("  8. Exit")
    print("========================================")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_all_patients()
        elif choice == "3":
            view_patient_report()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            delete_patient()
        elif choice == "6":
            search_patient()
        elif choice == "7":
            hospital_statistics()
        elif choice == "8":
            print("\nThank you for using the Hospital Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    main()


