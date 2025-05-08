# Inventory Management System 🛠️📊  

This is a Flask-based application designed for managing inventory, orders, employees, and other related data in a system. It supports admin and employee roles with different functionalities, including login, dashboard, viewing and filtering tables, adding and deleting data.  

---

## ✨ Features  

### 🔐 User Authentication  
- Login system with role-based access (Admin, Employee).  

### 👨‍💼 Admin Dashboard  
- Admins can add and delete data.  
- View various tables with filtering capabilities.  

### 👩‍💻 Employee Dashboard  
- Employees can view various tables.  
- Limited access compared to admin.  

### 🧭 Table Filters  
- Filter tables by various criteria such as salary, quantity, date, discount, etc.  
- Easily retrieve specific data based on filters.  

### 💸 Daily Turnover  
- View daily turnover for orders.  
- Track revenue and sales performance.  

---  

## ⚙️ Prerequisites  

Ensure you have the following installed:  
- Python  
- MySQL Server  
- Flask  
- MySQL Connector for Python  

---  

## 🛠️ Setup  

1. **Clone this repository.**  

2. **Install required Python packages:**  
   ```bash  
   pip install flask mysql-connector-python  
   ```  

3. **Configure the database connection:**  
   - Update the `mysql.connector.connect()` method in the code with your database credentials.  

4. **Run the application:**  
   ```bash  
   python app.py  
   ```  
   The application will run on `http://localhost:5000`.  

---  

Enjoy managing your inventory efficiently! 🚀
