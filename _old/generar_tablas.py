class Quasigroup():
    def __init__(self, set_of_elements,
                 operation_table, qg=None):
        if qg is None:
            self.elements = set_of_elements
            self.n_elements = len(set_of_elements)
            self.translate_dict = {
                set_of_elements[i]: i for i in
                range(0, self.n_elements)}
            self.funcion_s = operation_table

            self.funcion_d = [[0 for i in range(0,
                                                self.n_elements)]
                              for j in range(0,
                                             self.n_elements)]

            for i in range(0, self.n_elements):
                for j in range(0,
                               self.n_elements):
                    self.funcion_d[
                        self.translate_dict[
                            self.funcion_s[i][
                                j]]][j] = \
                        set_of_elements[i]

            self.funcion_d_g = [[0 for i in
                                 range(0,
                                       self.n_elements)]
                                for j in range(0,
                                               self.n_elements)]

            for i in range(0, self.n_elements):
                for j in range(0,
                               self.n_elements):
                    self.funcion_d_g[
                        self.translate_dict[
                            self.funcion_s[i][
                                j]]][i] = \
                        set_of_elements[j]
        else:
            self.elements = qg.elements
            self.n_elements = qg.n_elements
            self.translate_dict = qg.translate_dict
            self.funcion_s = qg.funcion_s
            self.funcion_d = qg.funcion_d
            self.funcion_d_g = qg.funcion_d_g


class QElement(Quasigroup):
    def __init__(self, qg, e):
        self.e = e
        self.qg = qg
        Quasigroup.__init__(self, None, None,
                            qg=qg)

    def __eq__(self, other):
        return self.e == other.e

    def __str__(self):
        return str(self.e)

    def __repr__(self):
        return str(self.e)

    def __add__(self, other):
        return QElement(self.qg, self.funcion_s[
            self.translate_dict[self.e]][
            other.translate_dict[other.e]])

    def __sub__(self, other):
        return QElement(self.qg, self.funcion_d[
            self.translate_dict[self.e]][
            other.translate_dict[other.e]])

    def __truediv__(self, other):
        return QElement(self.qg, self.funcion_d_g[
            self.translate_dict[self.e]][
            other.translate_dict[other.e]])


class Field(Quasigroup):
    def __init__(self, qg, product_table):
        Quasigroup.__init__(self, None, None,
                            qg=qg)
        self.product = product_table
        self.division = [
            [0 for i in range(0, self.n_elements)]
            for j in range(0, self.n_elements)]

        for i in range(0, self.n_elements):
            for j in range(1, self.n_elements):
                self.division[self.translate_dict[
                    self.product[i][j]]][j] = \
                    self.elements[i]


class FElement(Field):
    def __init__(self, qg, product_table, e):
        self.e = e
        self.qg = qg
        Field.__init__(self, qg, product_table)

    def __eq__(self, other):
        return self.e == other.e

    def __str__(self):
        return str(self.e)

    def __repr__(self):
        return str(self.e)

    def __add__(self, other):
        return FElement(self.qg, self.product,
                        self.funcion_s[
                            self.translate_dict[
                                self.e]][
                            other.translate_dict[
                                other.e]])

    def __sub__(self, other):
        return FElement(self.qg, self.product,
                        self.funcion_d[
                            self.translate_dict[
                                self.e]][
                            other.translate_dict[
                                other.e]])

    def __mul__(self, other):
        return FElement(self.qg, self.product,
                        self.product[
                            self.translate_dict[
                                self.e]][
                            other.translate_dict[
                                other.e]])

    def __truediv__(self, other):
        if self.translate_dict != "0":
            return FElement(self.qg, self.product,
                            self.division[
                                self.translate_dict[
                                    self.e]][
                                other.translate_dict[
                                    other.e]])
        else:
            raise Exception


def introducir_manualmente():
    tupla_qg = parser_tabla()

    qg = Quasigroup(tupla_qg[1], tupla_qg[0])

    # Ahora podemos operar con los elementos del cuasigrupo si quisieramos
    cero = QElement(qg, "0")
    uno = QElement(qg, "1")
    dos = QElement(qg, "2")
    tres = QElement(qg, "3")
    cuatro = QElement(qg, "4")


def parser_tabla():
    elementos = [elemento for elemento in input(
        "Elementos del cuasigrupo: ").split(" ")]
    n_elementos = len(elementos)

    matriz_operacional = [
        [elemento for elemento in
         input().split(" ")] for linea in
        range(0, n_elementos)]

    return (matriz_operacional, elementos)


def print_tabla(tabla):
    for i in range(0, len(tabla)):
        for j in range(0, len(tabla[i])):
            print(tabla[i][j],
                  end=" " if j != len(
                      tabla) - 1 else "\n")


def tablas_de_operaciones(quasigrupo,
                          field=False):
    print("Tabla de S(x,y):")
    print_tabla(quasigrupo.funcion_s)
    print("----------------")
    print("Tabla de D(x,y):")
    print_tabla(quasigrupo.funcion_d)
    print("----------------")
    print("Tabla de D gorro(x,y):")
    print_tabla(quasigrupo.funcion_d_g)
    print("----------------")

    if field:
        print("Tabla de Producto(x,y):")
        print_tabla(quasigrupo.product)
        print("----------------")
        print("Tabla de Division(x,y):")
        print_tabla(quasigrupo.division)
        print("----------------")


def funcion_s(mensaje, clave,
              orden_inverso=False):
    resultado = []

    for i in range(len(mensaje)):
        resultado.append(mensaje[i] + clave[
            i]) if not orden_inverso else resultado.append(
            clave[i] + mensaje[i])

    return resultado


def funcion_d(mensaje, clave,
              orden_inverso=False):
    resultado = []

    for i in range(len(mensaje)):
        resultado.append(mensaje[i] - clave[
            i]) if not orden_inverso else resultado.append(
            clave[i] - mensaje[i])

    return resultado


def funcion_d_g(mensaje, clave,
                orden_inverso=False):
    resultado = []

    for i in range(len(mensaje)):
        resultado.append(mensaje[i] / clave[
            i]) if not orden_inverso else resultado.append(
            clave[i] / mensaje[i])
    return resultado


def cifrado_combinaciones_lineales(mensaje, clave,
                                   seed_aleatoria):
    texto_cifrado = []
    cifrados = [funcion_s(mensaje, clave),
                funcion_d(mensaje, clave,
                          orden_inverso=True),
                funcion_d(mensaje, clave)]

    for i in range(len(mensaje)):
        aux = seed_aleatoria[0] * cifrados[0][i] + \
              seed_aleatoria[1] * cifrados[1][i] + \
              seed_aleatoria[2] * cifrados[2][
                  i]
        texto_cifrado.append(aux)

    return texto_cifrado


def descifrado_combinaciones_lineales(
        texto_cifrado, clave, seed_aleatoria,
        uno):
    mensaje_original = []

    lambda_1_inverso = uno / seed_aleatoria[0]
    diferencia_lambda_2_3 = seed_aleatoria[1] - \
                            seed_aleatoria[2]
    diferencia_lambda_3_2 = seed_aleatoria[2] - \
                            seed_aleatoria[1]

    factor_1 = uno / (
            uno - lambda_1_inverso * diferencia_lambda_2_3)

    factor_2 = []
    for i in range(len(texto_cifrado)):
        factor_2.append(lambda_1_inverso * (
                texto_cifrado[i] + clave[
            i] * diferencia_lambda_3_2) -
                        clave[i])

    for i in range(len(factor_2)):
        mensaje_original.append(
            factor_1 * factor_2[i])

    return mensaje_original


# z_3_qg = Quasigroup([0, 1, 2], [[0, 1, 2], [1, 2, 0], [2, 0, 1]])
z_5_qg = Quasigroup([0, 1, 2, 3, 4],
                    [[0, 1, 2, 3, 4],
                     [1, 2, 3, 4, 0],
                     [2, 3, 4, 0, 1],
                     [3, 4, 0, 1, 2],
                     [4, 0, 1, 2, 3]])

# tablas_de_operaciones(z_3_qg)
# tablas_de_operaciones(z_5_qg)

# z_3_field = Field(z_3_qg,[[0, 0, 0], [0, 1, 2], [0, 2, 1]])
z_3_field = Field(z_5_qg, [[0, 0, 0, 0, 0],
                           [0, 1, 2, 3, 4],
                           [0, 2, 4, 1, 3],
                           [0, 3, 1, 4, 2],
                           [0, 4, 3, 2, 1]])

# ablas_de_operaciones(z_3_field, field=True)

cero = FElement(z_5_qg, z_3_field.product, 0)
uno = FElement(z_5_qg, z_3_field.product, 1)
dos = FElement(z_5_qg, z_3_field.product, 2)
tres = FElement(z_5_qg, z_3_field.product, 3)
cuatro = FElement(z_5_qg, z_3_field.product, 4)

mensaje = [uno, uno, tres, cuatro]
clave = [dos, tres, cero, cuatro]
seed_aleatoria = [cuatro, dos, uno]

c = cifrado_combinaciones_lineales(mensaje, clave,
                                   seed_aleatoria)
print(c)
d = descifrado_combinaciones_lineales(c, clave,
                                      seed_aleatoria,
                                      uno)
print(d)

# s_3 = Quasigroup([])
