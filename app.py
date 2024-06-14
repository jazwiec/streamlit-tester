import streamlit as st
from pymssql import _mssql
import pymssql
import pyodbc
import requests

st.title('SQL Server Connection Tester')

st.write("Hosting TLS version: " + requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])
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