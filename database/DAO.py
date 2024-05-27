from database.DB_connect import DBConnect
from model.airport import Airport
from model.connessione import Connessione


class DAO:

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n_min, id_map):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select tmp.ID, tmp.IATA_CODE, count(*) N
                    from (
                    select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*) n 
                    from airports a, flights f
                    where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID, a.IATA_CODE, f.AIRLINE_ID) tmp
                    group by tmp.ID, tmp.IATA_CODE
                    having N>=%s"""
        cursor.execute(query, (n_min,))
        for row in cursor:
            result.append(id_map[row["ID"]])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_edges_v1(id_map):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID """
        cursor.execute(query)
        for row in cursor:  #creo l'oggetto Connessione
            result.append(Connessione(id_map[row["ORIGIN_AIRPORT_ID"]],  #estraggo l'aeroporto di partenza e arrivo
                                      id_map[row["DESTINATION_AIRPORT_ID"]],
                                      row["n"]))  #estraggo il numero di rotte
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_edges_v2(id_map):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
        select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce(t1.rotte, 0)+ coalesce(t2.rotte, 0) n
from (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) rotte
	from flights f 
	group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
	order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
left join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) rotte
	from flights f 
	group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
	order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and t2.ORIGIN_AIRPORT_ID = t1.DESTINATION_AIRPORT_ID
where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null"""
        cursor.execute(query)
        for row in cursor:  # creo l'oggetto Connessione
            result.append(Connessione(id_map[row["ORIGIN_AIRPORT_ID"]],  # estraggo l'aeroporto di partenza e arrivo
                                      id_map[row["DESTINATION_AIRPORT_ID"]],
                                      row["n"]))  # estraggo il numero di rotte
        cursor.close()
        conn.close()
        return result
