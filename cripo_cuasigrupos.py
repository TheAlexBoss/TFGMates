import random
"""
This is a demo implementation of Quasigroups, Fields and main
functionality of Linear Combinations with the presented Cyphers.
"""


class QuasiGroup:
    def __init__(self, name, elements, operation_table):
        self.name = name
        self.elements = elements
        self._operation_table = operation_table

        self._s_function = Utils.calc_s_function(operation_table,
                                                 elements)
        self._d_function = Utils.calc_d_function(self._s_function,
                                                 elements)
        self._d_hat_function = Utils.calc_d_hat_function(
            self._s_function, elements)

    def _get_name(self):
        return f"Quasigroup {self.name}\n"

    def __str__(self):
        output = self._get_name()
        output += self.print_s_table()
        output += self.print_d_table()
        output += self.print_dh_table()
        return output

    def s(self, a, b):
        return self._s_function[(a, b)]

    def d(self, a, b):
        return self._d_function[(a, b)]

    def dh(self, a, b):
        return self._d_hat_function[(a, b)]

    # Cyphering methods that apply the function to lists
    # of elements of the QG
    @staticmethod
    def _apply(f, a, b):
        result = list()

        for i in range(len(a)):
            result.append(f(a[i], b[i]))
        return result

    def apply_s(self, a, b):
        return self._apply(self.s, a, b)

    def apply_d(self, a, b):
        return self._apply(self.d, a, b)

    def apply_dh(self, a, b):
        return self._apply(self.dh, a, b)

    # Printing methods that show the tables.
    def _print_table(self, table, table_name, div=False):
        output = f"{table_name}\n"

        for element_i in self.elements:
            for element_j in self.elements:
                if div and element_j == 0:
                    output += "X\t"
                    continue

                output += f"{table[(element_i, element_j)]}"
                if element_j != self.elements[-1]:
                    output += "\t"
            output += "\n"
        output += "\n"
        return output

    def print_s_table(self):
        return self._print_table(self._s_function, "S")

    def print_d_table(self):
        return self._print_table(self._d_function, "D")

    def print_dh_table(self):
        return self._print_table(self._d_hat_function, "^D")


class Field(QuasiGroup):
    def __init__(self, name, elements, sum_table, product_table):
        super(Field, self).__init__(name, elements, sum_table)
        self._product_table = product_table
        self._product_function = Utils.calc_s_function(product_table,
                                                       elements)
        self._division_function = Utils.calc_d_function(
            self._product_function, elements)

    def _get_name(self):
        return f"Field {self.name}\n"

    def __str__(self):
        output = super(Field, self).__str__()
        output += self._print_table(self._product_function, "x")
        output += self._print_table(self._division_function, "/",
                                    div=True)
        return output

    @staticmethod
    def _apply_scalar_vector_function(f, scalar, vector):
        """
        In fields, apply_p and apply_div are functions that receive an
        scalar and a vector and multiplies (resp. divides) the vector
        by the scalar.

        This is because element by element product or division is not
        used.
        """
        result = list()
        for element in vector:
            result.append(f(scalar, element))
        return result

    def product(self, a, b):
        return self._product_function[(a, b)]

    def division(self, a, b):
        return self._division_function[(a, b)]

    def apply_p(self, a, b):
        return self._apply_scalar_vector_function(self.product, a, b)

    def apply_div(self, a, b):
        return self._apply_scalar_vector_function(self.product, a, b)


class Utils:
    """
    Hola que tal :D
    """
    @staticmethod
    def calc_s_function(operation_table, elements):
        """
        We refactor the operation table into a map function.
        """
        elements_number = len(elements)
        function = dict()

        for i in range(elements_number):
            for j in range(elements_number):
                function[(elements[i], elements[j])] = \
                operation_table[i][j]
        return function

    @staticmethod
    def calc_d_function(s_function, elements):
        """
        We calc D(x,y) with:    D(x,y) = z <=> S(z,y) = x
        """
        function = dict()
        for element_i in elements:
            for element_j in elements:
                function[(s_function[(element_i, element_j)],
                          element_j)] = element_i
        return function

    @staticmethod
    def calc_d_hat_function(s_function, elements):
        """
        We calc ^D(x,y) with:    ^D(x,y) = z <=> S(y,z) = x
        """
        function = dict()
        for element_i in elements:
            for element_j in elements:
                function[(s_function[(element_j, element_i)],
                          element_j)] = element_i
        return function

    @staticmethod
    def load_data(text_file, integer_mode=False):
        """
        Loads the cuasigroup from a text_file with the correct format.
        Integer_mode is for the case that the Quasigroup is made of
        integers.
        """

        def process(x):
            return int(x.strip()) if integer_mode else x.strip()

        def read_table():
            table = list()
            for i in range(elements_number):
                table_line = list(map(lambda x: process(x),
                                      f.readline().split(",")))
                table.append(table_line)
            return table

        with open(text_file) as f:
            line = f.readline().split()
            is_field = (line[0] == "F")
            name = line[1]
            elements_number = int(line[2])
            elements = list(
                map(lambda x: process(x), f.readline().split(",")))
            operation_table = read_table()
            if is_field:
                product_table = read_table()
                return Field(name, elements, operation_table,
                             product_table)

        return QuasiGroup(name, elements, operation_table)

    @staticmethod
    def parse_construction(qg, construction, integer_mode=False):
        """
        This method receives a String as input, and it outputs a list
        with each element of the Quasigroup in that string.
        """
        elements_set = set(qg.elements)
        output = list()
        temp = ""

        for char in construction:
            temp += char
            if integer_mode:
                temp = int(temp)
            if temp in elements_set:
                if integer_mode:
                    output.append(int(temp))
                else:
                    output.append(temp)
                temp = ""
        return output


class LinearCombination:
    """
    This class is used to show the functionality of the Linear
    Combination Cypher described.
    """

    def __init__(self, field):
        self._field = field

    def create_random_seed(self):
        random_seed = [random.choices(self._field.elements) for _ in
                       range(3)]
        return random_seed

    def encrypt(self, message, key, random_seed):
        # There are these 3 different ways of cypher.
        s_cypher = self._field.apply_p(random_seed[0],
                                       self._field.apply_s(message,
                                                           key))
        flipped_d_cypher = self._field.apply_p(random_seed[1],
                                               self._field.apply_d(
                                                   key, message))
        d_cypher = self._field.apply_p(random_seed[2],
                                       self._field.apply_d(message,
                                                           key))

        return self._field.apply_s(
            self._field.apply_s(s_cypher, flipped_d_cypher), d_cypher)

    def decrypt(self, cypher_text, key, random_seed):
        constant_1 = self._field.division(1, random_seed[0])
        constant_2 = self._field.d(random_seed[1], random_seed[2])
        constant_3 = self._field.d(0, constant_2)

        left_member = self._field.product(constant_1, constant_2)
        left_member = self._field.d(1, left_member)
        left_member = self._field.division(1, left_member)

        right_member = self._field.apply_p(constant_3, key)
        right_member = self._field.apply_s(cypher_text, right_member)
        right_member = self._field.apply_p(constant_1, right_member)
        right_member = self._field.apply_d(right_member, key)

        return self._field.apply_p(left_member, right_member)


def basic_example_test():
    qg = Utils.load_data("./quasi_group_descriptions.txt")
    print(qg)
    # The result of adding 2 + 2 in the QG
    print(qg.s("2", "2"))
    # Cyphering 0012 + 1111
    print(qg.apply_s(["0", "0", "1", "2"], ["1", "1", "1", "1"]))
    # The same as:
    print(qg.apply_s(Utils.parse_construction(qg, "0012"),
                     Utils.parse_construction(qg, "1111")))


def qg_example():
    qg = Utils.load_data("./quasi_group_descriptions.txt")
    print(qg)
    m = Utils.parse_construction(qg, "hihi")
    k = Utils.parse_construction(qg, "fg(id)j")

    cypher_text = qg.apply_s(m, k)
    print(f"Cypher text: {cypher_text}")
    m_p = qg.apply_d(cypher_text, k)
    print(f"Recovered Plain Text: {m_p}")


def linear_combinations_test():
    field = Utils.load_data("./quasi_group_descriptions.txt",
                            integer_mode=True)
    print(field)
    lc = LinearCombination(field)
    random_seed = Utils.parse_construction(field, "421",
                                           integer_mode=True)
    message = Utils.parse_construction(field, "1134",
                                       integer_mode=True)
    key = Utils.parse_construction(field, "2304", integer_mode=True)

    c = lc.encrypt(message, key, random_seed)
    print(
        f"With the message {message}, the key {key} and the random "
        f"seed {random_seed} we have the Cypher text: {c}")
    m_prime = lc.decrypt(c, key, random_seed)
    print(f"Decrypted {m_prime} should be equal to message {message}")


basic_example_test()
linear_combinations_test()
qg_example()
