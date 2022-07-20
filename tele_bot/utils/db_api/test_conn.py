import psycopg2
import asyncpg
import datetime
import asyncio
import logging


def conn_db():
    pass


def get_list_oo(pattern_search, DB_CREDIENTALS):
    try:
        db_conn = psycopg2.connect(**DB_CREDIENTALS)#(database="PN_QUERIES", user="pn_admin", password="12345", host="localhost", port=5432)
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


def get_list_services(DB_CREDIENTALS): # debt: rewrite with asyncpg
    try:
        db_conn = psycopg2.connect(**DB_CREDIENTALS)
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
        
      
def get_list_tgusers(DB_CREDIENTALS): # debt: rewrite with asyncpg
    try:
        db_conn = psycopg2.connect(**DB_CREDIENTALS)
        cursor = db_conn.cursor()
        cursor.execute(f'''
                   SELECT telegram_id FROM owners
                   ORDER BY id ASC 
                   ''')
        u = cursor.fetchall()
        uu = []
        for i in u:
            if not i[0] is None:
                uu.append(i[0])
        return tuple(uu)
    except Exception:
        print("херня с базой")
    finally:
        db_conn.close()
 
 
async def add_query_to_DB(obj_for_DB, DB_CREDIENTALS):
    conn_db = await asyncpg.connect(**DB_CREDIENTALS)
    owner_id = await conn_db.fetchval ('''
        SELECT id FROM owners WHERE telegram_id = $1
        ''', str(obj_for_DB['user_id']))
    await conn_db.execute('''
        INSERT INTO pn_queries (id_oo_id, text, id_owner_id, service_id, date_create, active, photo_link) VALUES ($1, $2, $3, $4, $5, $6, $7)
        ''', int(obj_for_DB['oo_id']),
            obj_for_DB['text'],
            owner_id,
            int(obj_for_DB['service_id']),
            datetime.datetime.now(),
            True,
            obj_for_DB['path_to_localdir'])
    await conn_db.close()
    

# asyncio.get_event_loop().run_until_complete(add_query_to_DB({'oo_id': '4', 'service_id': '1', 'text': 'Tr', 'user_id': '73053093', 'photocounter': 1, 'path_to_localdir': '2022-03-11_21_32_07.600289_rn_2043'}))
# asyncio.run(add_query_to_DB({'oo_id': '4', 'service_id': '1', 'text': 'oi', 'user_id': '73053093', 'photocounter': 1, 'path_to_localdir': '2022-03-11_21_32_07.600289_rn_2043'}))