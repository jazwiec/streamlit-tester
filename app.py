import streamlit as st
from pymssql import _mssql
import pymssql
import pyodbc

st.title('SQL Server Connection Tester')


server = st.text_input('Server', "mssql4.webio.pl,2401")
database = st.text_input('Database', "")
username = st.text_input('Username', "")
password = st.text_input('Password', type='password')


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
        
        connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password + ";Encrypt=no;TrustServerCertificate=yes;TLSVersion=1.2"
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