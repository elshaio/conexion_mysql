import pymysql
from conexion_mysql.Errors import ConexionError


class ManejadorConexion:

    def __init__(self, host=None, user=None, password=None, database=None):
        try:
            self.conexion = pymysql.connect(host=host,
                                            user=user,
                                            password=password,
                                            db=database,
                                            cursorclass=pymysql.cursors.DictCursor)
            self.conectado = True
        except Exception as e:
            self.conectado = False
            raise ConexionError(
                'No se ha podido conectar a la base de datos {}, causado por {}'.format(database, str(e)))

    def cerrar(self):
        self.conexion.close()
        self.conectado = False

    def reconectar(self):
        if self.conectado:
            self.conexion.close()

        self.conexion.connect()

    def cursor(self):
        return self.conexion.cursor()
