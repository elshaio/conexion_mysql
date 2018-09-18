def arrayobj_a_arraytupla(arreglo, *args):

    lista = []

    for entrada in arreglo:
        tupla = ()
        for argumento in list(args):
            tupla = tupla + (getattr(entrada, argumento),)

        lista.append(tupla)

    return lista
