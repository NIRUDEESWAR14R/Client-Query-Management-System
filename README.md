# Client-Query-Management-System
The Client Query Management System (CQMS) is a real-time web application built using Streamlit, MySQL, and Python, designed to streamline client-support communication. It allows clients to submit support queries, while support teams can track, manage, and close them efficiently.
🧠 Skills You’ll Learn
Python programming
Streamlit web app development
MySQL database management
Data organizing and cleaning using Pandas
EDA (Exploratory Data Analysis) and visualization
Statistics & performance tracking
Maintainable and portable code design
🏢 Domain
SQL / Data Engineering / Python
💡 Problem Statement
The goal of this project is to create a Client Query Management System that:
Provides a platform for clients to submit support queries.
Enables support teams to track open and closed queries.
Improves communication, efficiency, and response times.
Provides visualization and performance analytics for the support team.
📈 Business Use Cases
Use Case	Description
Query Submission Interface	Clients can submit new queries with email, mobile, heading, and description.
Query Tracking Dashboard	Support team monitors, filters, and manages open/closed queries.
Service Efficiency	Track how quickly queries are resolved.
Customer Satisfaction	Faster query resolution improves client satisfaction.
Support Load Monitoring	Identify query trends and high-load areas.
⚙️ Approach & Architecture
🔐 1. Login System (Client & Support Team)
Role-based login with Client and Support user types.
Passwords hashed securely using hashlib.sha256().
User credentials stored in users table (MySQL).
users(username, hashed_password, role)
💬 2. Query Insertion (Client Side)
Clients fill a Streamlit form with:
Email ID
Mobile Number
Query Heading
Query Description
Automatically stores:
query_created_time → datetime.now()
status → "Open"
🧰 3. Query Management (Support Team)
View, filter, and close queries.
Closing a query updates:
status → "Closed"
query_closed_time → datetime.now()
📊 4. Visualization / EDA
Query statistics panel includes:
Total queries count
Open vs Closed queries
Average resolution time (in hours)
Bar chart: queries created per day
Pie chart: query status distribution
🧹 Data Cleaning
Buttons to clean user and query data from MySQL tables for testing.
Ensures a maintainable and reusable demo environment.
⚡ Maintainability & Portability
Database-agnostic: Works with MySQL or SQLite.
Modular functions: get_connection(), create_tables(), etc.
Cross-platform: Run on any OS with Streamlit installed.
Easy deployment via:
streamlit run streamlit_app.py
🧩 Technology Stack
Component	Technology
Language	Python
Frontend	Streamlit
Database	MySQL (via mysql-connector-python)
Data Handling	Pandas
Visualization	Streamlit Charts & Matplotlib
Libraries	pandas, mysql.connector, hashlib, datetime, matplotlib
🧮 Dataset
Simulated query log CSV file with columns:
Column	Description
query_id	Unique query identifier
mail_id	Client email ID
mobile_number	Client mobile number
query_heading	Short title of the query
query_description	Detailed description
status	"Open" or "Closed"
query_created_time	Timestamp when created
query_closed_time	Timestamp when closed
📁 Folder Structure
Client_query_management_system/
│
├── Data/
│   └── queries.csv
│
├── src/
│   ├── create_db_tables.py
│   ├── load_csv_to_mysql.py
│
├── env/
│   └── (Virtual environment)
│
├── streamlit_app.py
├── requirements.txt
└── README.md
💻 Setup Instructions
Clone or download the project
git clone https://github.com/<your-username>/Client_query_management_system.git
cd Client_query_management_system
Install dependencies
pip install -r requirements.txt
Configure MySQL
Create a database (e.g. client_query_db)
Update credentials in get_connection() inside streamlit_app.py
Create tables and load data
python src/create_db_tables.py
python src/load_csv_to_mysql.py
Run the Streamlit app
streamlit run streamlit_app.py
📊 Sample Outputs
Client Page
Submit new query form
Confirmation message on submission
Support Dashboard
Open/Closed queries list
“Close Query” button
Real-time metrics and charts
EDA Section
📅 Bar chart: Queries per day
🥧 Pie chart: Open vs Closed
📈 Metric cards for statistics
🧠 Project Evaluation Metrics
✅ Maintainable Code
✅ Portable Across Environments
✅ Public GitHub Repository
✅ Well-Documented README
✅ Streamlit UI with Forms and Tables
✅ Uses datetime and proper SQL Querying
✅ Visualization / EDA Section
👨‍💻 Developer
Nirudeeswar R
📍 Chennai
🎓 B.Tech CSE, VIT Chennai
📧 nirudeeswarr15@gmail.com
🏁 Final Result
✅ Fully functional Client Query Management System featuring:
Secure login system
Real-time query management
Support analytics dashboard
Data visualization and EDA
Maintainable and portable architecture
