from database.DB_connect import DBConnect
from model.product import product
from model.edges import edges


class DAO:

    @staticmethod
    def getColori():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  gp.Product_color as 'color'
FROM go_products gp """
            cursor.execute(query)
            for row in cursor:
                result.append(row['color'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getProducts(color):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp.* 
FROM go_products gp 
WHERE gp.Product_color = %s"""
            cursor.execute(query, (color,))
            for row in cursor:
                result.append(product(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year, color, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp1.Product_number as id1, gp2.Product_number as id2, COUNT(DISTINCT gds2.`Date`) as weight
FROM go_products gp1, go_products gp2, go_daily_sales gds1, go_daily_sales gds2
WHERE gp1.Product_number < gp2.Product_number and gp1.Product_number = gds1.Product_number and gp2.Product_number = gds2.Product_number and gds1.Retailer_code = gds2.Retailer_code and gds1.`Date` = gds2.`Date` and YEAR(gds1.`Date`) = %s and gp1.Product_color = %s and gp2.Product_color = %s 
GROUP BY gp1.Product_number, gp2.Product_number"""
            cursor.execute(query, (year, color, color))
            for row in cursor:
                result.append(edges(idMap[row['id1']], idMap[row['id2']], row['weight']))
            cursor.close()
            cnx.close()
        return result
