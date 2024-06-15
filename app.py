import streamlit as st
from pymssql import _mssql
import pymssql
import pyodbc
import requests
import ssl
import database.db_manager as db_manager


st.title('SQL Server Connection Tester v3')
st.write("Hosting TLS version (before): " + requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])

ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

ctx.options |= ssl.OP_NO_SSLv2
ctx.options |= ssl.OP_NO_SSLv3
ctx.options |= ssl.OP_NO_TLSv1
ctx.options |= ssl.OP_NO_TLSv1_1

ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

st.write("Hosting TLS version (after): " + requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])

st.divider()



server = st.text_input('Server', "mssql4.webio.pl,2401")
database = st.text_input('Database', "")
username = st.text_input('Username', "")
password = st.text_input('Password', type='password')

#DRIVER={SQL Server Native Client 11.0}
driver = st.text_input('Driver', "DRIVER={ODBC Driver 17 for SQL Server}")
encrypt = st.text_input('Encrypt', "no")
trustServerCertificate = st.text_input('TrustServerCertificate', "yes")
TLSVersion = st.text_input('TLSVersion', "1.2")
options = st.text_input('Options', "")

st.divider()

if st.button('Connect to database by _mssql'):
    try:
        st.write('Connecting to database...')
        
        conn = _mssql.connect(server=server, user=username, password=password, database=database)
        st.write('Connected to database!')

        row = conn.execute_row('SELECT TOP(1) * FROM poca.ChatSession')
        st.write(row)

        conn.close()
    except Exception as e:
        st.write('Error:', e)



if st.button('Connect to database by pymssql'):
    try:
        st.write('Connecting to database...')
        
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor(as_dict=True)

        st.write('Connected to database!')
        
        cursor.execute('SELECT TOP(1) * FROM poca.ChatSession')
        for row in cursor:
            st.write(row)

        cursor.close()
        conn.close()
    except Exception as e:
        st.write('Error:', e)



if st.button("Connect to database by pyodbc"):
    try:
        st.write('Connecting to database...')
        
        # connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password + ";Encrypt=no;TrustServerCertificate=yes;TLSVersion=1.2"
        connection_string = driver + ";SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password + ";Encrypt=no;TrustServerCertificate=yes;TLSVersion=1.2"
 
        if options:
            connection_string = connection_string + ";" + options
       
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        st.write('Connected to database!')
        
        cursor.execute('SELECT TOP(1) * FROM poca.ChatSession')
        for row in cursor:
            st.write(row)

        cursor.close()
        conn.close()
    except Exception as e:
        st.write('Error:', e)


        

if st.button("Create local database"):
    try:
        st.write('Create local database...')
        data = db_manager.create_database()
        
    except Exception as e:
        st.write('Error:', e)


if st.button("Get data from local database"):
    try:
        st.write('Connecting to local database...')
        data = db_manager.get_app_config()
        st.write('Data')
        st.write(data)
        
    except Exception as e:
        st.write('Error:', e)


id = st.text_input('Id', "")
value = st.text_input('Value', "")

if st.button("Add data to local database"):
    try:
        data = db_manager.add_app_config(id, value)
        
    except Exception as e:
        st.write('Error:', e)


db_path = st.text_input('Database path', "")
if db_path:
    try:
        with open(db_path, "rb") as file:
            btn = st.download_button(
                    label="Download db file",
                    data=file,
                    file_name="db_bkp.db"
                )
    except Exception as e:
        st.write('Error:', e)
else:
    st.write('Enter database path')
