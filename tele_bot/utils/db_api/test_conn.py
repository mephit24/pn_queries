import psycopg2

def parsing_query_db(result):
    pass


def get_list_oo(pattern_search):
    try:
        db_conn = psycopg2.connect(database="PN_QUERIES", user="pn_admin", password="12345", host="localhost", port=5432)
        cursor = db_conn.cursor()
        if pattern_search == "*":
            cursor.execute(f'''
                   SELECT * FROM public.oo
                    ORDER BY oo ASC 
                   ''')
        else:
            cursor.execute(f'''
                   SELECT * FROM public.oo
                    WHERE oo ILIKE '%{pattern_search}%'
                    ORDER BY oo ASC 
                   ''')
        return cursor.fetchall()
    except Exception:
        print("херня с базой")
    finally:
        db_conn.close()


def get_list_services():
    try:
        db_conn = psycopg2.connect(database="PN_QUERIES", user="pn_admin", password="12345", host="localhost", port=5432)
        cursor = db_conn.cursor()
        cursor.execute(f'''
                SELECT * FROM services
                ORDER BY service ASC 
                ''')
        return cursor.fetchall()
    except Exception:
        print("херня с базой")
    finally:
        db_conn.close()
        
      
def get_list_tgusers():
    try:
        db_conn = psycopg2.connect(database="PN_QUERIES", user="pn_admin", password="12345", host="localhost", port=5432)
        cursor = db_conn.cursor()
        cursor.execute(f'''
                   SELECT telegram_id FROM owners
                   ORDER BY id ASC 
                   ''')
        u = cursor.fetchall()
        uu = []
        for i in u:
            uu.append(i[0])
        return tuple(uu)
    except Exception:
        print("херня с базой")
    finally:
        db_conn.close()
        