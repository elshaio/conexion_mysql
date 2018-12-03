def arrayobj_a_arraytupla(arreglo, *args):
    lista = []

    for entrada in arreglo:
        tupla = ()
        for argumento in list(args):
            tupla = tupla + (getattr(entrada, argumento),)

        lista.append(tupla)

    return lista


def arraydict_a_arraytupla(arreglo, *args):
    lista = []

    for entrada in arreglo:
        tupla = ()
        for argumento in list(args):
            tupla = tupla + (entrada[argumento],)

        lista.append(tupla)

    return lista


def list_a_tupla(lista):
    tupla = ()
    for elemento in lista:
        tupla = tupla + (elemento,)

    return tupla


def dict_a_tupla(diccionario, *args):
    tupla = ()
    for argumento in list(args):
        tupla = tupla + (diccionario[argumento], )

    return tupla
