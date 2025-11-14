# Project title         :  Pay Book – Billing and Invoice Generator
# Project for           :  IT Fundamentals and Applications
# Project completed by  :  Muhammad Abdullah Elahi, TC-061
# Project submitted to  :  Dr. Amir Zeb, Lab Instructor and Class Teacher


# ────────────────────────────────────────────────
# 1. Import Required Modules
#    (Start → Setup Phase in flowchart)
# ────────────────────────────────────────────────
from pick import pick
from detail_editor import edit_details
from exportpdf import export_to_pdf
from exportexcel import export_to_excel
from pretty_print import pretty_print_details


# ────────────────────────────────────────────────
# 2. Define Input Structure
#    (List representing required project fields)
# ────────────────────────────────────────────────
data = [
    "Project Name",
    "Client Name",
    "Date",
    "Objective",
    "Time",
    ["Services", "Amount", "Discount"]
]


# ────────────────────────────────────────────────
# 3. Initialise Data Storage
#    (Dictionary where all input will be stored)
# ────────────────────────────────────────────────
values = {
    "Total Amount (PKR)": 0,
    "Advance": 0
}


# ────────────────────────────────────────────────
# 4. Helper Function
#    Safely get a floating-point number from user
# ────────────────────────────────────────────────
def get_float(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", ""))
        except ValueError:
            print("❌ Please enter a valid number.")


# ────────────────────────────────────────────────
# 5. Collect User Input
#    Loops through structure and fills "values"
# ────────────────────────────────────────────────
for val in data:

    # ────────────────────────────────────────────
    # Case 1: When encountering the Services list
    #         (Special handling → sub-loop)
    # ────────────────────────────────────────────
    if type(val) == list:

        # Internal service list + counter
        services = []
        counter = 1

        # Options for pick menu
        options = ["Add Service/ Product", "Exit"]

        print("\n-----------------------")
        print("Services / Products")
        print("-----------------------\n")

        # Sub-loop → Collect multiple services
        while True:
            option, _ = pick(options, "Do you have more services or not?")

            if option == "Exit":
                break  # Exit the service entry loop

            # Display counter index for current service
            print(f"\nService - {counter}")
            counter += 1

            # Inputs for service details
            name = input("Enter Service Name: ")
            amount = get_float("Enter Service Amount (PKR): ")
            discount = get_float("Enter Discount (%): ")

            # Calculate discounted price
            subTotal = amount - (amount * discount / 100)

            # Store service in list
            services.append({
                "Service/ Product": name,
                "Amount (PKR)": amount,
                "Discount (%)": discount,
                "Total (PKR)": subTotal
            })

            # Update totals in main dictionary
            values["Total Amount (PKR)"] += subTotal
            values["Advance"] = values["Total Amount (PKR)"] / 2

        # After exiting service entry, attach list
        values["Services"] = services

    # ────────────────────────────────────────────
    # Case 2: Normal field (simple input)
    # ────────────────────────────────────────────
    else:
        values[val] = input(f"Enter {val}: ")


# ────────────────────────────────────────────────
# 6. Display Entered Details
#    (Pretty printed summary of all values)
# ────────────────────────────────────────────────
pretty_print_details(values)
print("\n\n\n\n")  # Visual spacing


# ────────────────────────────────────────────────
# 7. Export / Edit Options
#    (Main Post-Entry Menu Loop)
# ────────────────────────────────────────────────
opt = [
    "Export to PDF",
    "Export to Excel",
    "Export to Both",
    "Edit Data",
    "Exit"
]

# Continuous loop until user selects Exit
while True:
    option, _ = pick(opt, "Select")

    # Export to PDF
    if option == opt[0]:
        export_to_pdf(values, input("Enter file name: "))

    # Export to Excel
    elif option == opt[1]:
        export_to_excel(values, input("Enter file name: "))

    # Export to both formats
    elif option == opt[2]:
        export_to_excel(values, input("Enter file name for Excel: "))
        export_to_pdf(values, input("Enter file name for PDF: "))

    # Edit existing details
    elif option == opt[3]:
        edit_details(values)
        pretty_print_details(values)
        print("✅ Details updated successfully!\n")

    # Exit program
    else:
        break
