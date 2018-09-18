class ConexionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class QueryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ProcedimientoError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
