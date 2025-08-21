# Food Waste Management System

Food Waste Management System is an SQL-based project that enables to manage food wastage problem efficiently by providing those in need like NGOs and Orphanages with non-expired left over food from supermarkets, restaurants, etc. It also has Streamlit application with UI for anyone to interact with

The project primarily has four datasets to work with:
* Providers: The list of entities providing the food (Ex: Restaurant, Supermarket, etc.)
* Receivers: The list of entities receiving the food (Ex: NGOs)
* Food Listing: The table of all the foods listed by the provider
* Claims: The table that contains records of food claimed by receiver including status

There are four main phases of this project they are

#### Data Preparation

This involves loading the datasets into the memory, understanding them by establishing relationships between tables, searching for duplicates and null values. If found, enable an efficient way to handle them to finally produce clean dataset to work with during further phases.

From the given data, there are no null values or duplicates found, hence the original dataset is fully clean and ready for the next stage.

#### Database Creation

In this phase, MySQL is installed and deployed at port no 3306 of my local system. Once it is up and running, a framework called mysql.connector is installed to access the database using python for efficient automation. Connection is established by entering the port no and password. After the connection is setup, a cursor is defined which is then used to create the database, tables and insert values into those tables. Insertion is then perfomed with exception handling to catch any improper data.

Now the database and the tables in they are fully ready for in-depth analysis

#### Data Analysis

Data analysis aims to uncover any insights in data using select queries and graphical representations. Fifteen important questions were answered in this phase they are

1. How many food providers and receivers are there in each city?
2. Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
3. What is the contact information of food providers in a specific city?
4. Which receivers have claimed the most food?
5. What is the total quantity of food available from all providers?
6. Which city has the highest number of food listings?
7. What are the most commonly available food types?
8. How many food claims have been made for each food item?
9. Which provider has had the highest number of successful food claims?
10. What percentage of food claims are completed vs. pending vs. canceled?
11. What is the average quantity of food claimed per receiver?
12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
13. What is the total quantity of food donated by each provider?
14. Which food items have the highest unclaimed rate?
15. How many unique food items does each provider contribute?

Graphs were also plotted for some queries for a better understanding

#### Streamlit Application

The final Phase of the project is the streamlit application, which is a user-friendly application whose aim is to manage the data and check for insights with a non-code-based interface. It has five main pages they are
* About Project - The first page of the application that is static and displays the information about the project and guides user on how to use the application.
* View Tables - The page where user can see the data of all the tables in the database it uses select queries to fetch data from the database.
* CRUD Operations - This page is mainly for the application admin who can insert, update and delete records from all the tables with a simple UI and tested of various test cases with irregular and corrupted data.
* P & R Filters - The page where users can search for the contact of receivers and providers based on city and ID.
* 15 Queries - The queries mentioned before with graphs are added in this page where user can select using a dropdown on the type of data they look for. It get continuously updated as it performs select option every time user toggles between the dropdown of queries. Hence, working simultaneously with CRUD operation page.
