"""Numeric matrice calculator script is performing different operations with matrices"""

from operator import add
import math

class NumericMatrixProcessor:

    def __init__(self):
        self.message = None

    def first_second_matrix(self):
        """method for reading 2 matrices from input usig list comprehension"""
        n, m = input("Enter size of first matrix: ").split()
        matrix1 = []
        print("Enter first matrix:")
        for _ in range(int(n)):
            matrix1.append([int(x) if x.isdigit() else float(x) for x in input().split()])

        y, z = input("Enter size of second matrix: ").split()
        matrix2 = []
        print("Enter second matrix:")
        for _ in range(int(y)):
            matrix2.append([int(x) if x.isdigit() else float(x) for x in input().split()])
        return matrix1, matrix2

    def add_matrix(self):
        """method for addition of elements in 2 matrices"""
        added_matrix = []
        matrix1, matrix2 = self.first_second_matrix()
        n = len(matrix1)
        m = len(matrix1[0])
        y = len(matrix2)
        z = len(matrix2[0])
        if n == y and m == z:
            for i in range(len(matrix1)):
                added_matrix.append(list(map(add, matrix1[i], matrix2[i])))
            print("The result is:")
        else:
            print("The operation cannot be performed.")

        for list_ in added_matrix:
            line = []
            for element in list_:
                line.append(str(element))
            line = " ".join(line)
            print(line)

    def scaling(self):
        """method used for matrix multiplication with a constant"""
        n, m = input("Enter size of matrix: ").split()
        matrix = []
        scaled = []
        print("Enter matrix:")
        for _ in range(int(n)):
            matrix.append([int(x) if x.isdigit() else float(x) for x in input().split()])
        scaler = float(input("Enter constant: "))
        print("The result is:")
        for list_ in matrix:
            line = list(map(lambda x: x * scaler, list_))
            print(*line, sep=" ")

    def multiplication(self):
        """method used for element by element multiplication of 2 matrices"""
        matrix1, matrix2 = self.first_second_matrix()
        #n = len(matrix1)
        m = len(matrix1[0])
        y = len(matrix2)
        #z = len(matrix2[0])
        if m == y:
            multiplied = [[sum(x * y for x, y in zip(row_matrix1, col_matrix2))
                           for col_matrix2 in zip(*matrix2)] for row_matrix1 in matrix1]
            print("The result is:")
            for line in multiplied:
                print(*line, sep=" ")
        else:
            print("The operation cannot be performed.")



    def transpose(self):
        """method used for finding the transpose of a matrice.
        Even doe in linear algebra there is only transpose by main diagonal,
        for the sake of practice with this method we can find also
        transpose by secondary diagonal, by vertical line or by horisontal line"""


        choice = input("\n1. Main diagonal\n2. Side diagonal\n\
3. Vertical line\n4. Horizontal line\nYour choice: ")
        n, m = input("Enter matrix size: ").split()
        matrix = []
        print("Enter matrix:")
        for _ in range(int(n)):
            matrix.append([(x) for x in input().split()])
        if choice == "1":
            print("The result is: ")
            main_dt = [[matrix[j][i] for j in range(int(n))] for i in range(int(m))]
            for line in main_dt:
                print(*line, sep=" ")
        elif choice == "2":
            print("The result is: ")
            main_dt = [[matrix[j][i] for j in range(int(n))] for i in range(int(m))]
            side_dt = [main_dt[-i][::-1] for i in range(1, len(main_dt) + 1)]
            for line in side_dt:
                print(*line, sep=" ")
        elif choice == "3":
            print("The result is:")
            vertical_t = [matrix[i][::-1] for i in range(int(n))]
            for line in vertical_t:
                print(*line, sep=" ")
        elif choice == "4":
            print("The result is:")
            horizontal_t = [matrix[-i] for i in range(1, int(n) + 1)]
            for line in horizontal_t:
                print(*line, sep=" ")


    def determinant(self):
        """method used to find the determinant of a matrice n X n"""
        n, m = input("Enter matrix size: ").split()
        matrix = []
        print("Enter matrix:")
        for _ in range(int(n)):
            matrix.append([int(x) if x.isdigit() else float(x) for x in input().split()])
        def minor(matrice, i, j):
            """function is calculating the minor of a matrice"""
            return [row[:j] + row[j+1:] for row in (matrice[:i] + matrice[i+1:])]

        def get_determinant(matrice):
            """function is calculating the determinant of matrice using recursion"""
            if len(matrice) == 2:
                return matrice[0][0] * matrice[1][1] - matrice[0][1] * matrice[1][0]
            elif len(matrice) == 1:
                return matrice[0][0]

            determinant = 0
            for c in range(len(matrice)):
                determinant += ((-1) ** c) * matrice[0][c] * get_determinant(minor(matrice, 0, c))
            return determinant

        determinated = get_determinant(matrix)
        print(f"The result is:\n{determinated}")


    def inversed(self):
        """method for getting the inverse matrice"""
        n, m = input("Enter matrix size: ").split()
        matrix = []
        print("Enter matrix:")
        for _ in range(int(n)):
            matrix.append([int(x) if x.isdigit() else float(x) for x in input().split()])
        def minor(matrice, i, j):
            """function for getting the minor of a matrice"""
            return [row[:j] + row[j+1:] for row in (matrice[:i] + matrice[i+1:])]

        def get_determinant(matrice):
            """function for getting the determinant of a matrice"""
            if len(matrice) == 2:
                return matrice[0][0] * matrice[1][1] - matrice[0][1] * matrice[1][0]
            elif len(matrice) == 1:
                return matrice[0][0]

            determinant = 0
            for c in range(len(matrice)):
                determinant += ((-1) ** c) * matrice[0][c] * get_determinant(minor(matrice, 0, c))
            return determinant

        def get_transposed(matrice):
            """function for getting the transposed of a matrice"""
            return list(map(list, zip(*matrice)))

        def get_inversed(matrice):
            """function for finding the inversed matrice"""
            determinant = get_determinant(matrice)
            if determinant == 0:
                return ""
            elif len(matrice) == 1:
                return round((1 / matrice[0][0]), 3)
            elif len(matrice) == 2:
                return [[round((matrice[1][1] / determinant), 2), round((-1 * matrice[0][1] / determinant), 2)],
                        [round((-1 * matrice[1][0] / determinant), 2), round((matrice[0][0] / determinant), 2)]]

            cofactors = []

            for row in range(len(matrice)):
                cofactor_row = []

                for col in range(len(matrice)):
                    new_minor = minor(matrice, row, col)
                    cofactor_row.append(((-1) ** (row + col)) * get_determinant(new_minor))
                cofactors.append(cofactor_row)
            cofactors = get_transposed(cofactors)
            for row in range(len(cofactors)):
                for col in range(len(cofactors)):
                    cofactors[row][col] = round((cofactors[row][col] / determinant), 2)
            return cofactors

        inversed = get_inversed(matrix)
        determinant = get_determinant(matrix)
        if determinant == 0:
            print("The matrix doesn't have an inverse.")
        else:
            print("The result is:")
            #printing elements of the inversed matrix aligned
            print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in inversed]))

    def main_menu(self):
        while True:
            self.message = input("""1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrices
5. Calculate a determinant
6. Inverse matrix
0. Exit\nYour choice: """)
            if self.message == "1":
                self.add_matrix()
                print()
            elif self.message == "2":
                self.scaling()
                print()
            elif self.message == "3":
                self.multiplication()
                print()
            elif self.message == "4":
                self.transpose()
                print()
            elif self.message == "5":
                self.determinant()
                print()
            elif self.message == "6":
                self.inversed()
                print()
            else:
                if self.message == "0":
                    break





nmp = NumericMatrixProcessor()
nmp.main_menu()
