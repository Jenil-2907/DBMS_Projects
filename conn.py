from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session handling
# Hardcoded Users (Username: Password and Role)
users = {
    "admin1": {"password": "adminpass1", "role": "admin"},
    "admin2": {"password": "adminpass2", "role": "admin"},
    "employee1": {"password": "emppass1", "role": "employee"},
    "employee2": {"password": "emppass2", "role": "employee"}
}

# Database Connection
try:
    cursor = None
    mydb = mysql.connector.connect(
        host="202311050-dbms.mysql.database.azure.com",
        user="jenil50",
        password="Azuredb99.", #ofc this will not work as i have removed sql server from cloud...
        database="project"
    )
    cursor = mydb.cursor()
except Error as e:
    print(f"Error connecting to MySQL: {e}")

# List of Allowed Tables
allowed_tables = ['Inventory', 'supplier', 'Offers', 'EMPLOYEE', 'Sales', 'Orders', 'Custormer', 'shipping', 'rack']

# ======== LOGIN & DASHBOARD ========
@app.route('/', methods=['GET', 'POST'])
def login():
    """Login Page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """User Dashboard (Options Based on Role)"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', role=session['role'], tables=allowed_tables)

@app.route('/logout')
def logout():
    """Logout and Clear Session"""
    session.clear()
    return redirect(url_for('login'))

# ======== VIEW TABLE ========
@app.route('/view_table', methods=['GET'])
def view_table():
    """View Selected Table with Optional Filtering"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    table_name = request.args.get('table')
    if table_name not in allowed_tables:
        flash("Invalid table selection", "error")
        return render_template('index.html', role=session['role'], tables=allowed_tables)
    
    try:
        # Handle specific table filters
        if table_name == 'EMPLOYEE' and request.args.get('salary_min') and request.args.get('salary_max'):
            salary_min = request.args.get('salary_min')
            salary_max = request.args.get('salary_max')
            
            # Assuming the salary column is named 'salary'
            query = f"SELECT * FROM {table_name} WHERE salary BETWEEN %s AND %s"
            cursor.execute(query, (salary_min, salary_max))
            
            data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            
            filter_applied = f"Showing employees with salary between {salary_min} and {salary_max}"
            return render_template('inventory.html', table_name=table_name, data=data, 
                                  column_names=column_names, filter_applied=filter_applied)
        
        elif table_name == 'Orders' and request.args.get('order_date'):
            order_date = request.args.get('order_date')
            order_ID = request.args.get('product_id')

            try:
                datetime.strptime(order_date, '%Y-%m-%d')  # Validate Date Format
            except ValueError:
                flash("Invalid date format.", "error")
                return redirect(url_for('view_table', table=table_name))

            # Get daily turnover
            turnover_query = """
                SELECT DATE(order_date) as date, COALESCE(SUM(sale_price), 0) as daily_turnover 
                FROM Orders 
                WHERE DATE(order_date) = %s 
                GROUP BY DATE(order_date)
            """
            cursor.execute(turnover_query, (order_date,))
            turnover_result = cursor.fetchone()
            turnover_value = turnover_result[1] if turnover_result else 0

            # Get all orders for that date
            cursor.execute("SELECT * FROM Orders WHERE DATE(order_date) = %s", (order_date,))
            data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description] if cursor.description else []

            # Handle product_id filter separately
            product_data = []
            if order_ID:
                Id_query = "SELECT * FROM Orders WHERE product_id = %s"
                cursor.execute(Id_query, (order_ID,))
                product_data = cursor.fetchall()

            if not data:
                data = []  # Ensure 'data' is iterable

            filter_applied = f"Showing orders for date: {order_date} | Daily Turnover: ${turnover_value}"

            return render_template(
                'inventory.html',
                table_name=table_name,
                data=data,
                column_names=column_names,
                filter_applied=filter_applied
            )
        
        elif table_name == 'Offers':
            # Build query dynamically based on provided filters
            query = f"SELECT * FROM {table_name} WHERE 1=1"
            params = []
            filter_description = []
            
            # Check for discount range filter
            discount_min = request.args.get('discount_min')
            discount_max = request.args.get('discount_max')
            if discount_min and discount_max:
                try:
                    discount_min = float(discount_min) / 100
                    discount_max = float(discount_max) / 100
                    query += " AND Offer BETWEEN %s AND %s"
                    params.extend([discount_min, discount_max])
                    filter_description.append(f"discount between {discount_min * 100}% and {discount_max * 100}%")
                except ValueError:
                    flash("Invalid discount values provided.", "error")
                    return redirect(url_for('view_table', table=table_name))
            
            # Check for product ID filter
            product_id = request.args.get('product_id')
            if product_id:
                query += " AND product_id = %s"
                params.append(product_id)
                filter_description.append(f"product ID = {product_id}")
            
            # If no filters applied, show all data
            if not params:
                cursor.execute(f"SELECT * FROM {table_name}")
            else:
                cursor.execute(query, params)
            
            data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            
            # Create filter notification message if filters were applied
            filter_applied = None
            if filter_description:
                filter_applied = f"Showing offers with {' and '.join(filter_description)}"
            
            return render_template('inventory.html', table_name=table_name, data=data, 
                                  column_names=column_names, filter_applied=filter_applied)
        
        elif table_name == 'Inventory':
            # Build query dynamically based on provided filters
            query = f"SELECT * FROM {table_name} WHERE 1=1"
            params = []
            filter_description = []
    
            # Check for quantity filter
            quantity_filter_type = request.args.get('quantity_filter_type')
            quantity_value = request.args.get('quantity_value')
    
            if quantity_value and quantity_filter_type:
                try:
                    quantity_value = int(quantity_value)
                    if quantity_filter_type == 'more':
                        query += " AND Quantity >= %s"
                        params.append(quantity_value)
                        filter_description.append(f"quantity greater than or equal to {quantity_value}")
                    elif quantity_filter_type == 'less':
                        query += " AND Quantity <= %s"
                        params.append(quantity_value)
                        filter_description.append(f"quantity less than or equal to {quantity_value}")
                except ValueError:
                    flash("Invalid quantity value provided.", "error")
                    return redirect(url_for('view_table', table=table_name))
    
            # Check for product ID filter
            product_id = request.args.get('product_id')
            if product_id:
                query += " AND product_id = %s"
                params.append(product_id)
                filter_description.append(f"product ID = {product_id}")
    
            # If no filters applied, show all data
            if not params:
                cursor.execute(f"SELECT * FROM {table_name}")
            else:
                cursor.execute(query, params)
    
            data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
    
            # Create filter notification message if filters were applied
            filter_applied = None
            if filter_description:
                filter_applied = f"Showing inventory with {' and '.join(filter_description)}"
    
            return render_template('inventory.html', table_name=table_name, data=data, 
                                  column_names=column_names, filter_applied=filter_applied)
        
        elif table_name == 'shipping':
            # Check if the user wants to join with Orders table
            join_with_orders = request.args.get('join_with_orders') == 'yes'

            if join_with_orders:
                query = """
                    SELECT s.shipping_id, s.Order_id, s.Address, s.dis_date, s.Order_date, o.customer_name 
                    FROM shipping s
                    JOIN Orders o ON s.Order_id = o.Order_id
                """
                filter_applied = "Showing shipping details with customer names"
            else:
                query = "SELECT * FROM shipping"
                filter_applied = "Showing shipping details without customer names"

            cursor.execute(query)
            data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]

            return render_template('inventory.html', table_name=table_name, data=data, 
                                   column_names=column_names, filter_applied=filter_applied)

        # Default view with no filters
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        return render_template('inventory.html', table_name=table_name, data=data, column_names=column_names)
    
    except Error as e:
        error_message = f"Database error: {str(e)}"
        flash(error_message, "error")
        return render_template('index.html', role=session['role'], tables=allowed_tables)

# ======== ADD DATA (Admin Only) ========
@app.route('/add_data', methods=['GET'])
def add_data():
    """Form to Add Data to Table (Admin Only)"""
    if 'username' not in session or session['role'] != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('dashboard'))
    
    table_name = request.args.get('table')
    if table_name not in allowed_tables:
        flash("Invalid table selection", "error")
        return redirect(url_for('dashboard'))
    
    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        column_names = [col[0] for col in cursor.fetchall()]
        return render_template('add_data.html', tables=allowed_tables, selected_table=table_name, column_names=column_names)
    except Error as e:
        error_message = f"Database error: {str(e)}"
        flash(error_message, "error")
        return render_template('index.html', role=session['role'], tables=allowed_tables)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    """Insert Data into Table (Admin Only)"""
    if 'username' not in session or session['role'] != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('dashboard'))
    
    table_name = request.form['table']
    if table_name not in allowed_tables:
        flash("Invalid table selection", "error")
        return redirect(url_for('dashboard'))
    
    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        column_names = [col[0] for col in cursor.fetchall()]
        values = [request.form[col] for col in column_names]
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
        
        cursor.execute(query, values)
        mydb.commit()
        flash(f"Data successfully added to {table_name}", "success")
        return redirect(url_for('add_data', table=table_name))
    
    except Error as e:
        error_message = f"Database error: {str(e)}"
        flash(error_message, "error")
        return render_template('add_data.html', tables=allowed_tables, selected_table=table_name, 
                              column_names=column_names, error=error_message)

# ======== DELETE DATA (Admin Only) ========
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """Delete Data from Table (Admin Only)"""
    if 'username' not in session or session['role'] != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('dashboard'))
    
    table_name = request.args.get('table') if request.method == 'GET' else request.form.get('table')
    if table_name not in allowed_tables:
        flash("Invalid table selection", "error")
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        record_id = request.form.get('record_id')

        try:
            cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
            primary_key = cursor.fetchone()
            
            if not primary_key:
                flash(f"Table {table_name} has no primary key, deletion not supported.", "warning")
                return redirect(url_for('view_table', table=table_name))
            
            primary_key_column = primary_key[4]
            query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
            cursor.execute(query, (record_id,))
            mydb.commit()
            
            if cursor.rowcount > 0:
                flash(f"Record successfully deleted from {table_name}", "success")
            else:
                flash("No matching record found.", "warning")
                
            return redirect(url_for('view_table', table=table_name))

        except Error as e:
            flash(f"Database error: {str(e)}", "error")
            return redirect(url_for('view_table', table=table_name))
    
    # Fetch records to display for deletion
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        column_names = [col[0] for col in cursor.fetchall()]
        return render_template('delete.html', table_name=table_name, records=records, column_names=column_names)
    except Error as e:
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for('dashboard'))
    
if __name__ == '__main__':
    app.run(debug=True)
