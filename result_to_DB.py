import psycopg2


def insert_result_db(url, harmless, malicious, suspicious, undetected, timeout, result_status, treat_status, treat_count):
    # Open a cursor to perform database operations
    conn = psycopg2.connect(database="DB",
                            host="dns.badbotsolution.xyz",
                            user="postgres",
                            password="cAmbodi@168c",
                            port=5432)

    cursor = conn.cursor()
    # Executing a SQL query to insert data into  table
    # insert_query = f""" INSERT INTO result_db (url, harmless, malicious, suspicious, undetected, timeout, result_status, treat_status, treat_count) VALUES ('uu', 1, 1, 1, 1, 1, 'uu', 'uu', 1)"""
    query = f""" INSERT INTO result_db (url, harmless, malicious, suspicious, undetected, timeout, result_status, treat_status, treat_count) VALUES ('{url}', {harmless}, {malicious}, {suspicious}, {undetected}, {timeout}, '{result_status}', '{treat_status}', {treat_count})"""

    cursor.execute(query)
    conn.commit()
    conn.close()


def select_result_db(link):
    conn = psycopg2.connect(database="DB",
                            host="dns.badbotsolution.xyz",
                            user="postgres",
                            password="cAmbodi@168c",
                            port=5432)
    cursor = conn.cursor()
    # Executing a SQL query to insert data into  table
    # insert_query = f""" INSERT INTO result_db (url, harmless, malicious, suspicious, undetected, timeout, result_status, treat_status, treat_count) VALUES ('uu', 1, 1, 1, 1, 1, 'uu', 'uu', 1)"""
    query = f"""SELECT url, harmless, malicious, suspicious, undetected, timeout, result_status, treat_status, treat_count
	FROM public.result_db 
	 WHERE url LIKE '{link}%';"""

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
