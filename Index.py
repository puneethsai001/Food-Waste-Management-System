import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime


def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()

    except Exception:
        return None

def parse_ts(ts: str):
    try:
        return datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None

# Setup MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aries@123"
)

cursor = conn.cursor()
cursor.execute("use FOOD")

st.set_page_config(page_title="Food Waste Management System", layout="wide")

OPERATIONS = [
    "Insert Records",
    "Update Records",
    "Delete Records",
]

PAGES = [
    "About Project",
    "View Tables",
    "CRUD Operations",
    "P & R Filters",
    "15 Queries",
]

TABLES = ["Providers", "Receivers", "Food Listings", "Claims"]

QUERIES = [
    "How many food providers and receivers are there in each city?",
    "Which type of food provider (restaurant, grocery store, etc.) contributes the most food?",
    "What is the contact information of food providers in a specific city?",
    "Which receivers have claimed the most food?",
    "What is the total quantity of food available from all providers?",

    "Which city has the highest number of food listings?",
    "What are the most commonly available food types?",
    "How many food claims have been made for each food item?",
    "Which provider has had the highest number of successful food claims?",
    "What percentage of food claims are completed vs. pending vs. canceled?",

    "What is the average quantity of food claimed per receiver?",
    "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?",
    "What is the total quantity of food donated by each provider?",
    "Which food items have the highest unclaimed rate?",
    "How many unique food items does each provider contribute?"
]

# A sidebar with a dropdown menu to toggle between pages of the applications
with st.sidebar:
    page = st.sidebar.selectbox("All Pages", PAGES)

# About Project Page
if page == "About Project":
    st.title("Food Waste Management System")
    st.caption("By Puneeth Sai")

    # Gives a basic idea about the application
    st.markdown("""
    ### Overview
    Food wastage is a significant issue, with many households and restaurants discarding
    surplus food while numerous people struggle with food insecurity. This project aims to
    develop a Local Food Wastage Management System, where

    - Restaurants and individuals can list surplus food 
    - NGOs or individuals in need can claim the food. 
    - SQL stores available food details and locations.
    - A Streamlit app enables interaction, filtering, CRUD operation and visualization.
 

    ---

    ### How It Works
    1. **Providers** (restaurants/individuals) post surplus food with quantity, location, and expiry date.  
    2. **Receivers** (NGOs/individuals) discover and **claim** listings that match their needs.  
    3. All records are stored in **SQL** (food listings, providers, receivers, claims).  
    4. The **Streamlit interface** allows:
       - Filtering of data
       - CRUD operations for admins
       - Real-time visualizations that update as data changes  

    ---

    ### Pages in this Application
    - **About Page** — Quick guide to understand the system and how to use it.  
    - **View Tables Page** — Browse all database tables (providers, receivers, listings, claims).  
    - **CRUD Operations Page** — Admins can **add**, **update**, or **delete** records.  
    - **P & R Filters Page** — Find **Providers** or **Receivers** by **ID** or **City**, and view contact details.  
    - **15 Queries Page** — A library of common queries with results and visualizations that refresh automatically.  

    ---
    
    **Note**: Navigate between the pages using sidebar.

    """)



# View Tables Page
elif page == "View Tables":
    st.title("View Tables")

    # A dropdown for user to select which table to view
    selectedTable = st.selectbox("Select Table", TABLES)

    # Display provider table
    if selectedTable == "Providers":
        cursor.execute("select * from providers")
        table = cursor.fetchall()
        table_df = pd.DataFrame(table, columns=["Provider ID", "Name", "Type", "Address", "City", "Contact"])
        st.dataframe(table_df)

    # Display receivers table
    elif selectedTable == "Receivers":
        cursor.execute("select * from receivers")
        table = cursor.fetchall()
        table_df = pd.DataFrame(table, columns=["Receiver ID", "Name", "Type", "City", "Contact"])
        st.dataframe(table_df)

    # Display food_listings table
    elif selectedTable == "Food Listings":
        cursor.execute("select * from food_listings")
        table = cursor.fetchall()
        table_df = pd.DataFrame(table, columns = ["Food ID", "Name", "Quantity", "Expiry Date", "Provider ID",
                                                  "Provider Type", "Location", "Food Type", "Meal Type"])
        st.dataframe(table_df)

    # Display claims table
    elif selectedTable == "Claims":
        cursor.execute("select * from claims")
        table = cursor.fetchall()
        table_df = pd.DataFrame(table, columns=["Claim ID", "Food ID", "Receiver ID", "Status", "Timestamp"])
        st.dataframe(table_df)



# CRUDE Operations Page
elif page == "CRUD Operations":
    st.title("CRUD Operations")

    # Dropdown to select which table to work with
    selectedTable = st.selectbox("Select Table", TABLES)

    if selectedTable == "Providers":

        selectedOperation = st.selectbox("Select Operation", OPERATIONS)

        # Insert to providers
        if selectedOperation == "Insert Records":

            # Input all fields
            with st.form("insert_provider"):
                pid_str = st.text_input("Provider ID")
                pname = st.text_input("Name")
                ptype = st.text_input("Type")
                paddress = st.text_input("Address")
                pcity = st.text_input("City")
                pcontact = st.text_input("Contact")

                submit = st.form_submit_button("Insert Records")

            if submit:

                # Validate the PID
                if not pid_str.strip().isdigit():
                    st.error("Provider ID must be a whole number.")

                elif not all([pname.strip(), ptype.strip(), paddress.strip(), pcity.strip(), pcontact.strip()]):
                    st.error("All fields are required.")

                else:
                    pid = int(pid_str.strip())

                    pinsert_query = """
                        INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    # Handle the insert query using exceptions

                    try:
                        cursor.execute(pinsert_query, (pid, pname, ptype, paddress, pcity, pcontact))
                        conn.commit()
                        st.success("Successfully inserted the record")

                    except Exception as e:
                        st.error(f"Insert failed: {e}")

        # Update to providers
        elif selectedOperation == "Update Records":

            with st.form("update_provider"):

                # Dropdown to update which field
                selectedField = st.selectbox("Update Field", ["Name", "Type", "Address", "City", "Contact"])
                pid_str = st.text_input("Provider ID")
                pdata = st.text_input(f"Enter {selectedField}")
                submit = st.form_submit_button("Update Records")

                if submit:

                    if not pid_str.strip().isdigit():
                        st.error("Provider ID must be a whole number.")
                        st.stop()

                    if pdata.strip() == "":
                        st.error(f"{selectedField} cannot be empty.")
                        st.stop()

                    pid = int(pid_str.strip())

                    pupdate_query = f"update providers set {selectedField} = %s where Provider_ID = %s"

                    try:
                        cursor.execute(pupdate_query, (pdata, pid))
                        conn.commit()

                        if cursor.rowcount == 0:
                            st.warning(f"No record found for Provider_ID = {pid}.")

                        else:
                            st.success("Successfully updated the record.")

                    except Exception as e:
                        st.error(f"Update failed: {e}")


        # Delete from providers
        elif selectedOperation == "Delete Records":
            with st.form("delete_provider"):
                pid_str = st.text_input("Provider ID")
                submit = st.form_submit_button("Delete Records")

                if submit:
                    if not pid_str.strip().isdigit():
                        st.error("Provider ID must be a whole number.")

                    pid = int(pid_str.strip())
                    pdelete_query = f"""
                    delete from providers where Provider_ID = {pid}
                    """

                    try:
                        cursor.execute(pdelete_query)
                        conn.commit()
                        st.success("Successfully deleted the record.")

                    except Exception as e:
                        st.error(f"Delete failed: {e}")

    elif selectedTable == "Receivers":

        selectedOperation = st.selectbox("Select Operation", OPERATIONS)

        # Insert to receivers
        if selectedOperation == "Insert Records":
            with st.form("insert_receiver"):
                rid_str = st.text_input("Receiver ID")
                rname = st.text_input("Name")
                rtype = st.text_input("Type")
                rcity = st.text_input("City")
                rcontact = st.text_input("Contact")
                submit = st.form_submit_button("Insert Records")

            if submit:
                if not rid_str.strip().isdigit():
                    st.error("Receiver ID must be a whole number.")

                elif not all([rname.strip(), rtype.strip(), rcity.strip(), rcontact.strip()]):
                    st.error("All fields are required.")
                else:
                    rid = int(rid_str.strip())
                    rinsert_query = """
                        insert into receivers (Receiver_ID, Name, Type, City, Contact)
                        values (%s, %s, %s, %s, %s)
                    """
                    try:
                        cursor.execute(rinsert_query, (rid, rname, rtype, rcity, rcontact))
                        conn.commit()
                        st.success("Successfully inserted the record.")
                    except Exception as e:
                        st.error(f"Insert failed: {e}")

        # Update to receivers
        elif selectedOperation == "Update Records":

            with st.form("update_receiver"):

                # Dropdown to update which field
                selectedField = st.selectbox("Update Field", ["Name", "Type", "City", "Contact"])
                rid_str = st.text_input("Receiver ID")
                rdata = st.text_input(f"Enter {selectedField}")
                submit = st.form_submit_button("Update Records")

            if submit:
                if not rid_str.strip().isdigit():
                    st.error("Receiver ID must be a whole number.")
                    st.stop()
                if rdata.strip() == "":
                    st.error(f"{selectedField} cannot be empty.")
                    st.stop()

                rid = int(rid_str.strip())
                rupdate_query = f"update receivers set {selectedField} = %s where Receiver_ID = %s"
                try:
                    cursor.execute(rupdate_query, (rdata, rid))
                    conn.commit()
                    if cursor.rowcount == 0:
                        st.warning(f"No record found for Receiver_ID = {rid}.")
                    else:
                        st.success("Successfully updated the record.")
                except Exception as e:
                    st.error(f"Update failed: {e}")

        # Delete from receivers
        elif selectedOperation == "Delete Records":
            with st.form("delete_receiver"):
                rid_str = st.text_input("Receiver ID")
                submit = st.form_submit_button("Delete Records")

            if submit:
                if not rid_str.strip().isdigit():
                    st.error("Receiver ID must be a whole number.")
                else:
                    rid = int(rid_str.strip())
                    rdelete_query = "delete from receivers WHERE Receiver_ID = %s"
                    try:
                        cursor.execute(rdelete_query, (rid,))
                        conn.commit()
                        st.success("Successfully deleted the record.")
                    except Exception as e:
                        st.error(f"Delete failed: {e}")

    elif selectedTable == "Food Listings":

        selectedOperation = st.selectbox("Select Operation", OPERATIONS)

        # Insert into food_listings
        if selectedOperation == "Insert Records":
            with st.form("insert_food"):
                fid_str = st.text_input("Food ID")
                fname = st.text_input("Food Name")
                fqty_str = st.text_input("Quantity")
                fexp_str = st.text_input("Expiry Date (YYYY-MM-DD)")
                pid_str = st.text_input("Provider ID")
                ptype = st.text_input("Provider Type")
                flocation = st.text_input("Location")
                ftype = st.text_input("Food Type")
                mtype = st.text_input("Meal Type")
                submit = st.form_submit_button("Insert Records")

            if submit:
                # numeric checks
                if not fid_str.strip().isdigit():
                    st.error("Food ID must be a whole number.")
                elif not fqty_str.strip().isdigit():
                    st.error("Quantity must be a whole number.")
                elif not pid_str.strip().isdigit():
                    st.error("Provider ID must be a whole number.")
                # required text
                elif not all([fname.strip(), ptype.strip(), flocation.strip(), ftype.strip(), mtype.strip(),
                              fexp_str.strip()]):
                    st.error("All fields are required.")
                else:
                    fexp = parse_date(fexp_str)
                    if fexp is None:
                        st.error("Expiry Date must be in YYYY-MM-DD format.")
                    else:
                        fid = int(fid_str.strip())
                        fqty = int(fqty_str.strip())
                        pid = int(pid_str.strip())

                        finsert_query = """
                            insert into food_listings
                            (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        try:
                            cursor.execute(finsert_query, (fid, fname, fqty, fexp, pid, ptype, flocation, ftype, mtype))
                            conn.commit()
                            st.success("Successfully inserted the record")

                        except Exception as e:
                            st.error(f"Insert failed: {e}")

        # Update to food_listings
        elif selectedOperation == "Update Records":
            with st.form("update_food"):
                updatable_fields = [
                    "Food_Name", "Quantity", "Expiry_Date", "Provider_ID",
                    "Provider_Type", "Location", "Food_Type", "Meal_Type"
                ]
                selectedField = st.selectbox("Update Field", updatable_fields)
                fid_str = st.text_input("Food ID")
                fdata = st.text_input(f"Enter {selectedField}")
                submit = st.form_submit_button("Update Records")

            if submit:
                if not fid_str.strip().isdigit():
                    st.error("Food ID must be a whole number.")
                    st.stop()
                if fdata.strip() == "":
                    st.error(f"{selectedField} cannot be empty.")
                    st.stop()

                # type handling per field
                value = fdata.strip()

                if selectedField in ("Quantity", "Provider_ID"):
                    if not value.isdigit():
                        st.error(f"{selectedField} must be a whole number.")
                        st.stop()
                    value = int(value)


                elif selectedField == "Expiry_Date":
                    d = parse_date(value)
                    if d is None:
                        st.error("Expiry Date must be in YYYY-MM-DD format.")
                        st.stop()
                    value = d

                fid = int(fid_str.strip())
                fupdate_query = f"update food_listings set {selectedField} = %s where Food_ID = %s"
                try:
                    cursor.execute(fupdate_query, (value, fid))
                    conn.commit()
                    if cursor.rowcount == 0:
                        st.warning(f"No record found for Food_ID = {fid}.")
                    else:
                        st.success("Successfully updated the record.")
                except Exception as e:
                    st.error(f"Update failed: {e}")

        # Delete from food_listings
        elif selectedOperation == "Delete Records":
            with st.form("delete_food"):
                fid_str = st.text_input("Food ID")
                submit = st.form_submit_button("Delete Records")

            if submit:
                if not fid_str.strip().isdigit():
                    st.error("Food ID must be a whole number.")
                else:
                    fid = int(fid_str.strip())
                    fdelete_query = "delete from food_listings where Food_ID = %s"
                    try:
                        cursor.execute(fdelete_query, (fid,))
                        conn.commit()
                        st.success("Successfully deleted the record.")
                    except Exception as e:
                        st.error(f"Delete failed: {e}")

    elif selectedTable == "Claims":

        selectedOperation = st.selectbox("Select Operation", OPERATIONS)

        # Insert into claims
        if selectedOperation == "Insert Records":
            with st.form("insert_claim"):
                cid_str = st.text_input("Claim ID")
                fid_str = st.text_input("Food ID")
                rid_str = st.text_input("Receiver ID")
                cstatus = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
                ctime_str = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
                submit = st.form_submit_button("Insert Records")

            if submit:
                if not cid_str.strip().isdigit():
                    st.error("Claim ID must be a whole number.")

                elif not fid_str.strip().isdigit():
                    st.error("Food ID must be a whole number.")

                elif not rid_str.strip().isdigit():
                    st.error("Receiver ID must be a whole number.")

                elif ctime_str.strip() == "":
                    st.error("Timestamp is required (YYYY-MM-DD HH:MM:SS).")

                else:
                    ctime = parse_ts(ctime_str)
                    if ctime is None:
                        st.error("Timestamp must be in format YYYY-MM-DD HH:MM:SS.")

                    else:
                        cid = int(cid_str.strip())
                        fid = int(fid_str.strip())
                        rid = int(rid_str.strip())

                        cinsert_query = """
                            insert into claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        try:
                            cursor.execute(cinsert_query, (cid, fid, rid, cstatus, ctime))
                            conn.commit()
                            st.success("Successfully inserted the record.")

                        except Exception as e:
                            st.error(f"Insert failed: {e}")

        # Update to claims
        elif selectedOperation == "Update Records":

            with st.form("update_claim"):
                updatable_fields = ["Food_ID", "Receiver_ID", "Status", "Timestamp"]
                selectedField = st.selectbox("Update Field", updatable_fields)
                cid_str = st.text_input("Claim ID")
                cdata_str = st.text_input(f"Enter {selectedField} (for Timestamp use YYYY-MM-DD HH:MM:SS)")
                submit = st.form_submit_button("Update Records")

            if submit:
                if not cid_str.strip().isdigit():
                    st.error("Claim ID must be a whole number.")
                    st.stop()
                if cdata_str.strip() == "":
                    st.error(f"{selectedField} cannot be empty.")
                    st.stop()

                value = cdata_str.strip()

                if selectedField in ("Food_ID", "Receiver_ID"):

                    if not value.isdigit():
                        st.error(f"{selectedField} must be a whole number.")
                        st.stop()
                    value = int(value)

                elif selectedField == "Status":
                    if value not in ["Pending", "Completed", "Cancelled"]:
                        st.error("Status must be one of: Pending, Completed, Cancelled.")
                        st.stop()

                elif selectedField == "Timestamp":
                    ts = parse_ts(value)
                    if ts is None:
                        st.error("Timestamp must be in format YYYY-MM-DD HH:MM:SS.")
                        st.stop()
                    value = ts

                cid = int(cid_str.strip())
                cupdate_query = f"update claims SET {selectedField} = %s where Claim_ID = %s"
                try:
                    cursor.execute(cupdate_query, (value, cid))
                    conn.commit()
                    if cursor.rowcount == 0:
                        st.warning(f"No record found for Claim_ID = {cid}.")
                    else:
                        st.success("Successfully updated the record.")
                except Exception as e:
                    st.error(f"Update failed: {e}")

        # Delete from claims
        elif selectedOperation == "Delete Records":
            with st.form("delete_claim"):
                cid_str = st.text_input("Claim ID")
                submit = st.form_submit_button("Delete Records")

            if submit:
                if not cid_str.strip().isdigit():
                    st.error("Claim ID must be a whole number.")
                else:
                    cid = int(cid_str.strip())
                    cdelete_query = "DELETE FROM claims WHERE Claim_ID = %s"
                    try:
                        cursor.execute(cdelete_query, (cid,))
                        conn.commit()
                        st.success("Successfully deleted the record.")
                    except Exception as e:
                        st.error(f"Delete failed: {e}")



# P & R Filters Page
elif page == "P & R Filters":
    st.title("Provider and Receiver Filters")

    selectedEntity = st.selectbox("Search for", ["Providers", "Receivers"])

    # Fetch Provider details
    if selectedEntity == "Providers":
        selectFilter = st.selectbox("Search based on", ["City", "Provider ID"])

        # If searching based on City
        if selectFilter == "City":
            provider_city = st.text_input("Enter City")

            if provider_city is not None and st.button("Search"):
                st.subheader(f"Search results for '{provider_city}'")
                provider_city_query = f"select Provider_ID, Name, Address, Contact from providers where city = '{provider_city}'"
                cursor.execute(provider_city_query)
                provider_city_result = cursor.fetchall()
                provider_city_df = pd.DataFrame(provider_city_result, columns=["Provider ID", "Name",
                                                                               "Address", "Contact"])
                st.dataframe(provider_city_df)

        # If searching based on ID
        elif selectFilter == "Provider ID":
            provider_id = st.text_input("Enter Provider ID")

            if provider_id is not None and st.button("Search"):
                st.subheader(f"Search results for '{provider_id}'")
                provider_id_query = f"select Name, Address, Contact from providers where Provider_ID = {provider_id}"
                cursor.execute(provider_id_query)
                provider_id_result = cursor.fetchall()
                provider_id_df = pd.DataFrame(provider_id_result, columns=["Name", "Address", "Contact"])
                st.dataframe(provider_id_df)

    # Fetch receiver details
    elif selectedEntity == "Receivers":
        selectFilter = st.selectbox("Search based on", ["City", "Receiver ID"])

        # If searching based on City
        if selectFilter == "City":
            receiver_city = st.text_input("Enter City")

            if receiver_city is not None and st.button("Search"):
                st.subheader(f"Search results for '{receiver_city}'")
                receiver_city_query = f"select Receiver_ID, Name, Contact from receivers where City = '{receiver_city}'"
                cursor.execute(receiver_city_query)
                receiver_city_result = cursor.fetchall()
                receiver_city_df = pd.DataFrame(receiver_city_result, columns=["Receiver ID", "Name", "Contact"])
                st.dataframe(receiver_city_df)

        # If searching based on ID
        elif selectFilter == "Receiver ID":
            receiver_id = st.text_input("Enter Receiver ID")

            if receiver_id is not None and st.button("Search"):
                st.subheader(f"Search results for '{receiver_id}'")
                receiver_id_query = f"select Name, Contact from receivers where Receiver_ID = {receiver_id}"
                cursor.execute(receiver_id_query)
                receiver_id_result = cursor.fetchall()
                receiver_id_df = pd.DataFrame(receiver_id_result, columns=["Name", "Contact"])
                st.dataframe(receiver_id_df)



# 15 Queries Page
elif page == "15 Queries":
    st.title("15 Queries")

    # Dropdown of all important queries
    selectedQuery = st.selectbox("Select Queries", QUERIES)

    # One by One display the records for all queries
    if selectedQuery == QUERIES[0]:

        query1_1 = "Select City, count(*) as Provider_Count from providers group by City order by Provider_Count desc;"
        query1_2 = "Select City, count(*) as Receiver_Count from receivers group by City order by Receiver_Count desc;"

        cursor.execute(query1_1)
        query1_1_result = cursor.fetchall()

        cursor.execute(query1_2)
        query1_2_result = cursor.fetchall()

        query1_1_df = pd.DataFrame(query1_1_result, columns=["City", "Provider Count"])
        query1_2_df = pd.DataFrame(query1_2_result, columns=["City", "Receiver Count"])

        st.subheader("Food Providers")
        st.dataframe(query1_1_df)

        st.subheader("Food Receivers")
        st.dataframe(query1_2_df)

    elif selectedQuery == QUERIES[1]:

        query2 = "select Provider_Type, sum(Quantity) as Total_Quantity from food_listings group by Provider_Type order by Total_Quantity desc"

        cursor.execute(query2)
        query2_result = cursor.fetchall()

        query2_df = pd.DataFrame(query2_result, columns=["Provider Type", "Total Quantity"])
        st.dataframe(query2_df)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(query2_df["Provider Type"], query2_df["Total Quantity"])
        ax.set_xlabel("Provider Type")
        ax.set_ylabel("Total Quantity")
        ax.set_title("Total Quantity by Provider Type")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    elif selectedQuery == QUERIES[2]:
        st.subheader("Providers from New Carol")
        City = 'New Carol'
        query3 = f"select Name, Contact from providers where City='{City}';"

        cursor.execute(query3)
        query3_result = cursor.fetchall()

        query3_df = pd.DataFrame(query3_result, columns=["Name", "Contact"])
        st.dataframe(query3_df)

    elif selectedQuery == QUERIES[3]:

        query4 = """ select r.Receiver_ID, r.Name, count(c.Claim_ID) as No_of_Claims
        from receivers as r
        join claims as c
        on r.Receiver_ID = c.Receiver_ID
        where c.Status = 'Completed'
        group by r.Name, r.Receiver_ID
        order by No_of_Claims desc; """

        cursor.execute(query4)
        query4_result = cursor.fetchall()

        query4_df = pd.DataFrame(query4_result, columns=["Receiver ID", "Name", "No of Claims"])
        st.dataframe(query4_df)

        top5_receivers = query4_df.sort_values(by="No of Claims", ascending=False).head(5)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(top5_receivers["Name"], top5_receivers["No of Claims"], color="green")
        ax.set_xlabel("Receiver Name")
        ax.set_ylabel("Number of Claims")
        ax.set_title("Top 5 Receivers by Number of Claims")
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    elif selectedQuery == QUERIES[4]:

        query5_1 = """
        select p.Provider_ID, p.Name, sum(f.Quantity) as Total_Quantity
        from providers as p
        join food_listings as f
        on p.Provider_ID = f.Provider_ID
        group by p.Provider_ID, p.Name
        order by Total_Quantity desc
        """

        query5_2 = """
        select sum(Quantity) as Total_Quantity_Available from food_listings;
        """

        cursor.execute(query5_1)
        query5_1_result = cursor.fetchall()

        cursor.execute(query5_2)
        query5_2_result = cursor.fetchall()

        query5_1_df = pd.DataFrame(query5_1_result, columns=["Provider ID", "Name", "Total Quantity"])
        query5_2_df = pd.DataFrame(query5_2_result, columns=["Total Quantity Available"])

        st.dataframe(query5_2_df)

        top5_providers = query5_1_df.sort_values(by="Total Quantity", ascending=False).head(5)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(top5_providers["Name"], top5_providers["Total Quantity"], color="red")
        ax.set_xlabel("Provider Name")
        ax.set_ylabel("Total Quantity")
        ax.set_title("Top 5 Providers by Total Quantity")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)

    elif selectedQuery == QUERIES[5]:

        query6 = """
        select Location, count(*) as Total_Listing
        from food_listings group by Location
        order by Total_Listing desc
        limit 1
        """

        cursor.execute(query6)
        query6_result = cursor.fetchall()

        query6_df = pd.DataFrame(query6_result, columns=["Location", "Total Listing"])

        st.dataframe(query6_df)

    elif selectedQuery == QUERIES[6]:

        query7 = """
        select Food_Type, count(*) as Total_Listing
        from food_listings group by Food_Type
        order by Total_Listing desc
        """

        cursor.execute(query7)
        query7_result = cursor.fetchall()
        query7_df = pd.DataFrame(query7_result, columns=["Food Type", "Total Listing"])

        st.dataframe(query7_df)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            query7_df["Total Listing"],
            labels=query7_df["Food Type"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Food Type Distribution")
        plt.tight_layout()
        st.pyplot(fig)

    elif selectedQuery == QUERIES[7]:
        query8 = """
        select f.Food_ID, f.Food_Name, count(c.Claim_ID) as Claim_Count
        from claims as c join food_listings as f
        on f.Food_ID = c.Food_ID
        group by Food_ID
        order by Claim_Count desc;
        """

        cursor.execute(query8)
        query8_result = cursor.fetchall()

        query8_df = pd.DataFrame(query8_result, columns=["Food ID", "Food Name", "Claim Count"])

        st.dataframe(query8_df)

    elif selectedQuery == QUERIES[8]:
        query9 = """
        select p.Provider_ID, p.Name, count(c.Claim_ID) as Successful_Claims
        from claims as c
        join food_listings as f on c.Food_ID = f.Food_ID
        join providers as p on f.Provider_ID = p.Provider_ID
        where c.Status = 'Completed'
        group by p.Provider_ID, p.Name
        order by Successful_Claims desc
        limit 1
        """

        cursor.execute(query9)
        query9_result = cursor.fetchall()

        query9_df = pd.DataFrame(query9_result, columns=["Provider ID", "Provider Name", "Successful Claims"])

        st.dataframe(query9_df)

    elif selectedQuery == QUERIES[9]:
        st.subheader("Completed vs Pending vs Cancelled")

        query10 = """
        select Status, (count(*) / (select count(*) from claims)) * 100 as Percentage
        from claims
        group by Status
        order by Percentage desc
        """

        cursor.execute(query10)
        query10_result = cursor.fetchall()

        query10_df = pd.DataFrame(query10_result, columns=["Status", "Percentage"])
        st.dataframe(query10_df)

        labels = query10_df["Status"]
        sizes = query10_df["Percentage"]

        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.4)
        )

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)

        ax.set_title("Claim Status Distribution")
        plt.tight_layout()

        st.pyplot(fig)

    elif selectedQuery == QUERIES[10]:
        query11 = """
        select r.Receiver_ID, r.Name, avg(f.Quantity) as Avg_Quantity
        from receivers as r
        join claims as c on r.Receiver_ID = c.Receiver_ID
        join food_listings as f on f.Food_ID = c.Food_ID
        group by r.Receiver_ID, r.Name
        order by Avg_Quantity desc
        """

        cursor.execute(query11)
        query11_result = cursor.fetchall()

        query11_df = pd.DataFrame(query11_result, columns=["Receiver ID", "Receiver Name", "Average Quantity"])

        st.dataframe(query11_df)

    elif selectedQuery == QUERIES[11]:
        query12 = """
        select f.Meal_Type, count(c.Claim_ID) as Claim_Count
        from claims as c
        join food_listings as f on c.Food_ID = f.Food_ID
        group by f.Meal_Type
        order by Claim_Count desc
        limit 1
        """

        cursor.execute(query12)
        query12_result = cursor.fetchall()
        query12_df = pd.DataFrame(query12_result, columns=["Meal Type", "Claim Count"])
        st.dataframe(query12_df)

    elif selectedQuery == QUERIES[12]:
        query13 = """
        select p.Provider_ID, p.Name, sum(f.Quantity) as Total_Quantity
        from food_listings as f
        join providers as p on p.Provider_ID = f.Provider_ID
        group by p.Provider_ID, p.Name
        order by Total_Quantity desc
        """

        cursor.execute(query13)
        query13_result = cursor.fetchall()

        query13_df = pd.DataFrame(query13_result, columns=["Provider ID", "Provider Name", "Total Quantity"])

        st.dataframe(query13_df)

    elif selectedQuery == QUERIES[13]:
        query14 = """
        select f.Food_Name, count(c.Claim_ID) as Unclaim_Count
        from food_listings as f
        join claims as c on f.Food_ID = c.Food_ID
        where Status = 'Cancelled'
        group by f.Food_Name
        order by Unclaim_Count desc
        """

        cursor.execute(query14)
        query14_result = cursor.fetchall()

        query14_df = pd.DataFrame(query14_result, columns=["Food Name", "Cancelled Claims"])
        st.dataframe(query14_df)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(query14_df["Food Name"], query14_df["Cancelled Claims"], color="tomato")
        ax.set_xlabel("Cancelled Claims")
        ax.set_ylabel("Food Name")
        ax.set_title("Cancelled Claims by Food Item")
        plt.tight_layout()

        st.pyplot(fig)

    elif selectedQuery == QUERIES[14]:
        query15 = """
        select p.Provider_ID, p.Name, count(distinct f.Food_Name) as Unique_Food_Items
        from providers p
        join food_listings f on p.Provider_ID = f.Provider_ID
        group by p.Provider_ID, p.Name
        order by Unique_Food_Items desc
        """

        cursor.execute(query15)
        query15_result = cursor.fetchall()
        query15_df = pd.DataFrame(query15_result, columns=["Provider ID", "Provider Name", "Unique Food Items"])

        st.dataframe(query15_df)