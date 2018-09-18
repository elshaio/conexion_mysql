from conexion_mysql.ManejadorConexion import ManejadorConexion
from conexion_mysql.Errors import QueryError, ProcedimientoError
from conexion_mysql.utilidades import list_a_tupla
from datetime import date


class Conexion:

    def __init__(self, host='127.0.0.1', user=None, password=None, database=None, port=3306):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._port = port

        manejador = self._conectar()
        manejador.cerrar()

    def _conectar(self):
        return ManejadorConexion(host=self._host, user=self._user, password=self._password, database=self._database,
                                 port=self._port)

    def insertar_varios(self, query, arreglo_tuplas, metodo=None):
        manejador = self._conectar()

        metodo_str = ''
        if metodo is not None:
            metodo_str = '({})'.format(metodo)

        try:
            with manejador.cursor() as cursor:
                cursor.executemany(query, arreglo_tuplas)
                cursor.execute('COMMIT')
        except Exception as e:
            raise QueryError(
                '{}Hubo un error al insertar varios registros, error: "{}"'.format(metodo_str, str(e)))
        finally:
            manejador.cerrar()

    def lanzar_orden(self, query, metodo=None):
        manejador = self._conectar()

        metodo_str = ''
        if metodo is not None:
            metodo_str = '({})'.format(metodo)

        try:
            with manejador.cursor() as cursor:
                cursor.execute(query)
                cursor.execute('COMMIT')
        except Exception as e:
            raise QueryError(
                '{}Hubo un error al ejecutar la orden, error: "{}"'.format(metodo_str, str(e)))
        finally:
            manejador.cerrar()

    def lanzar_query(self, query, *args, **kwargs):
        metodo = kwargs.get('metodo', None)
        cantidad = kwargs.get('cantidad', 'M')

        manejador = self._conectar()

        metodo_str = ''
        if metodo is not None:
            metodo_str = '({})'.format(metodo)

        respuesta = None

        try:
            with manejador.cursor() as cursor:
                cursor.execute(query, list_a_tupla(args))
                if type(cantidad) == int:
                    if cantidad == 1:
                        respuesta = cursor.fetchone()
                    elif cantidad < 1:
                        raise QueryError(
                            '{}Hubo un error al ejecutar la query con la cantidad {} establecida, favor verificar'.format(
                                metodo_str, cantidad))
                    else:
                        respuesta = cursor.fetchmany(cantidad)
                elif type(cantidad) == str:
                    if cantidad == '1':
                        respuesta = cursor.fetchone()
                    elif cantidad == 'M':
                        respuesta = cursor.fetchall()
                    else:
                        raise QueryError(
                            '{}Hubo un error al ejecutar la query, se desconoce la cantidad {} establecida, favor verificar'.format(
                                metodo_str, cantidad))
                else:
                    raise QueryError(
                        '{}Hubo un error al ejecutar la query, el tipo de la cantidad establecida es desconocido.')

        except Exception as e:
            raise QueryError(
                '{}Hubo un error al ejecutar la query, error: "{}"'.format(metodo_str, str(e)))
        finally:
            manejador.cerrar()

        return respuesta

    def call(self, procedimiento, **kwargs):
        fecha = kwargs.get('fecha', date.today())
        fecha_formato = kwargs.get('fecha_formato', "%Y-%m-%d")
        respuesta_esperada = kwargs.get('respuesta_esperada', '')
        metodo = kwargs.get('metodo', None)

        connection = self._conectar()

        metodo_str = ''
        if metodo is not None:
            metodo_str = '({})'.format(metodo)

        call_str = 'CALL {}'.format(procedimiento)

        call_str = call_str.format(fecha=fecha.strftime(fecha_formato),
                                   parerror='@parerror')

        try:
            with connection.cursor() as cursor:
                sql = "SET @parerror = ''"
                cursor.execute(sql)
                cursor.execute(call_str)
                sql = 'SELECT @parerror as parerror'
                cursor.execute(sql)
                respuesta = cursor.fetchone()
                respuesta = respuesta['parerror']
        except Exception as e:
            raise QueryError(
                '{}Hubo un error al ejecutar el procedimiento {}, error: {}"'.format(metodo_str, procedimiento, str(e)))
        finally:
            connection.cerrar()

        if respuesta != respuesta_esperada:
            raise ProcedimientoError(
                '{}Error proporcionado por el procedimiento {}, "{}"'.format(metodo_str, procedimiento, respuesta))
