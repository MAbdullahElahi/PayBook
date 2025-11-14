# Project title         :  Pay Book – Billing and Invoice Generator
# Project for           :  IT Fundamentals and Applications
# Project completed by  :  Muhammad Abdullah Elahi, TC-061
# Project submitted to  :  Dr. Amir Zeb, Lab Instructor and Class Teacher



def edit_details(values):
    from pick import pick

    # ────────────────────────────────────────────
    # 1. Define Main Edit Menu Options (Flowchart)
    # ────────────────────────────────────────────
    edit_options = [
        "Edit Project Info",
        "Edit Services",
        "Back to Main Menu"
    ]

    # ────────────────────────────────────────────
    # 2. Loop Until User Chooses "Back"
    # ────────────────────────────────────────────
    while True:

        # Prompt user with the main edit menu (Flowchart: "Prompt user to select what to edit")
        choice, _ = pick(edit_options, "Select what to edit:")

        # ===========================================================
        # PART A: EDIT GENERAL PROJECT INFORMATION
        # ===========================================================
        if choice == "Edit Project Info":

            # ────────────────────────────────────────────────
            # A1. List Editable Project Fields (Flowchart)
            # ────────────────────────────────────────────────
            general_info_keys = ["Project Name", "Client Name", "Date", "Objective", "Time"]

            # User selects which field to modify
            key, _ = pick(general_info_keys, "Select field to edit:")

            # ────────────────────────────────────────────────
            # A2. Prompt for New Value & Store Update
            # ────────────────────────────────────────────────
            new_value = input(f"Enter new value for {key}: ")
            values[key] = new_value

            # Confirmation (Flowchart)
            print(f"✅ {key} updated.\n")

        # ===========================================================
        # PART B: EDIT / ADD / REMOVE SERVICES
        # ===========================================================
        elif choice == "Edit Services":

            # ────────────────────────────────────────────────
            # B1. If No Services Exist → Initialize Empty List
            # (Flowchart: "If no services exist → initialize empty list")
            # ────────────────────────────────────────────────
            if "Services" not in values or len(values["Services"]) == 0:
                print("No services found. Let's add one.\n")
                values["Services"] = []


            # ────────────────────────────────────────────────
            # B2. Service Actions Menu
            #    - Add Service
            #    - Edit Existing
            #    - Remove Service
            #    - Back
            # ────────────────────────────────────────────────
            service_actions = ["Add Service", "Edit Existing", "Remove Service", "Back"]
            act, _ = pick(service_actions, "Choose action for services:")

            # -----------------------------
            # B3. ADD SERVICE
            # -----------------------------
            if act == "Add Service":

                # Prompt user for service details (Flowchart: "Prompt for new service")
                name = input("Enter Service Name: ")
                amount = float(input("Enter Amount (PKR): ").replace(",", ""))
                discount = float(input("Enter Discount (%): ").replace(",", ""))

                # Calculate subtotal (Flowchart: Calculation box)
                subTotal = amount - (amount * discount / 100)

                # Append new service dictionary (Flowchart: "Append service")
                values["Services"].append({
                    "Service/ Product": name,
                    "Amount (PKR)": amount,
                    "Discount (%)": discount,
                    "Total (PKR)": subTotal
                })

                # Confirmation
                print("✅ Service added.\n")

            # -----------------------------
            # B4. EDIT EXISTING SERVICE
            # -----------------------------
            elif act == "Edit Existing":

                # (Flowchart: "If no services → print message")
                if len(values["Services"]) == 0:
                    print("No services to edit.\n")
                    continue

                # Show service names for selection
                service_names = [s["Service/ Product"] for s in values["Services"]]
                selected_service, index = pick(service_names, "Select service to edit:")

                # Retrieve selected record
                s = values["Services"][index]

                # Prompt for updated values (Flowchart)
                s["Service/ Product"] = input(f"Service Name ({s['Service/ Product']}): ") or s["Service/ Product"]
                s["Amount (PKR)"] = float(input(f"Amount ({s['Amount (PKR)']}): ").replace(",", "") or s["Amount (PKR)"])
                s["Discount (%)"] = float(input(f"Discount ({s['Discount (%)']}): ").replace(",", "") or s["Discount (%)"])

                # Recalculate total
                s["Total (PKR)"] = s["Amount (PKR)"] - (s["Amount (PKR)"] * s["Discount (%)"] / 100)

                # Confirmation
                print("✅ Service updated.\n")

            # -----------------------------
            # B5. REMOVE SERVICE
            # -----------------------------
            elif act == "Remove Service":

                # (Flowchart: "If no services exists → print message")
                if len(values["Services"]) == 0:
                    print("No services to remove.\n")
                    continue

                # Show list of service names
                service_names = [s["Service/ Product"] for s in values["Services"]]
                selected_service, index = pick(service_names, "Select service to remove:")

                # Remove and confirm
                removed = values["Services"].pop(index)
                print(f"🗑️  Removed {removed['Service/ Product']}.\n")

            # If user chooses "Back" → return to main menu loop
            else:
                pass

        # ===========================================================
        # PART C: EXIT TO MAIN MENU
        # ===========================================================
        else:
            break


    # ────────────────────────────────────────────
    # 3. Recalculate Totals After Editing (Flowchart: Final calculation)
    # ────────────────────────────────────────────
    total = sum(s["Total (PKR)"] for s in values["Services"])
    values["Total Amount (PKR)"] = total
    values["Advance"] = total / 2