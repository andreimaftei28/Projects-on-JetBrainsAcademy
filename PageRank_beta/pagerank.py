import numpy as np
import numpy.linalg as la
from io import StringIO


class PageRank:

    def __init__(self):


        self.L = np.array([
            [0, 1 / 2, 1 / 3, 0, 0, 0],
            [1 / 3, 0, 0, 0, 1 / 2, 0],
            [1 / 3, 1 / 2, 0, 1, 0, 1 / 2],
            [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 2],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1 / 3, 0, 0, 0]
        ])
        self.L2 = np.array([
    [0,   1/2, 1/3, 0, 0,   0,     0 ],
    [1/3, 0,   0,   0, 1/2, 0,     0 ],
    [1/3, 1/2, 0,   1, 0,   1 / 3, 0 ],
    [1/3, 0,   1/3, 0, 1/2, 1 / 3, 0 ],
    [0,   0,   0,   0, 0,   0,     0 ],
    [0,   0,   1/3, 0, 0,   0,     0 ],
    [0,   0,   0,   0, 0,   1 / 3, 1 ]
])

    def web_matrix(self, L):
        """method return the probability matrix in a nice formated way"""
        s = StringIO()
        np.savetxt(s, L, fmt="%.3f")
        return s.getvalue()

    def web_eingen(self, L):
        """method returns eingen vetctor in a nice formated way"""
        e_vals, e_vecs = la.eig(L)
        vec = np.transpose(e_vecs)[0]
        vec = vec * (100 / sum(vec))
        s = StringIO()
        np.savetxt(s, vec.real, fmt="%.3f")
        return s.getvalue()

    def web_eingen_iteration(self, L):
        """Method returns the eingen vectors using iteration"""
        r = (100 * np.ones(len(L))) / len(L)
        r = L @ r
        s_0 = StringIO()
        np.savetxt(s_0, r, fmt="%.3f")
        s_11 = StringIO()
        r_11 = r
        for _ in range(10):
            r_11 = L @ r_11
        np.savetxt(s_11, r_11, fmt="%.3f")
        s_con = StringIO()
        r_prev = r_11
        r_next = L @ r_prev
        while True:
            r_prev = L @ r_next
            r_next = L @ r_prev
            if la.norm(r_prev - r_next) <= 0.01:
                break

        np.savetxt(s_con, r_next, fmt="%.3f")
        return (s_0.getvalue(), s_11.getvalue(),s_con.getvalue())

    def web_probability_matrix(self, L, d):
        """Method takes a matrix as an imput and
        returns it multiplied by a dumping factor and normalized """
        J = np.ones(len(L))
        M = d * L + ((1 - d) / len(L)) * J
        return M

    def print_I_II(self):
        """Method for printing the output in stage I and stage II"""
        matrix = self.web_matrix(self.L)
        print(matrix)
        #comment this out if you are using it in stage II
        eingen = self.web_eingen(self.L)
        print(eingen)
        #comment this out if you are using it in stage I
        eingen_iter = self.web_eingen_iteration(self.L)
        print(*eingen_iter, sep="\n")


    def print_III(self):
        """method for printing the output in stage III"""
        matrix = self.web_matrix(self.L2)
        print(matrix)
        M = self.web_probability_matrix(self.L2, 0.5)
        *other, r_next = self.web_eingen_iteration(self.L2)
        print(r_next)

        *other, r_next = self.web_eingen_iteration(M)
        
        print(r_next)

    def print_IV(self):
        """method for printing the output in stage IV"""
        n, d = input("Enter the number of rows in your matrix and the dumping factor separated by space:\n").split()
        print("Enter yout matrix: ")
        L = np.array([[float(x) for x in input().split()] for _ in range(int(n))])
        M = self.web_probability_matrix(L, float(d))

        *other, r_next = self.web_eingen_iteration(M)

        print(r_next)

    def print_V(self):
        """method for printing the output in stage V"""
        n = int(input("Enter the number of websites in your micro-internet:\n"))
        site_list = [x for x in input().split()]
        print("""Enter the n lines of your probability matrix
Each line must contain n elements separated by space""")
        L = np.array([[float(x) for x in input().split()] for _ in range(n)])
        querry = input("""Enter your searching string:\n""")
        M = self.web_probability_matrix(L, 0.5)
        *other, r_next = self.web_eingen_iteration(M)
        site_ranks = [float(x) for x in r_next.split("\n") if x != '']
        ranks = dict(zip(site_list, site_ranks))
        output = []
        if querry in ranks:
            output.append(querry)
            del(ranks[querry])
        ranks  = dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True))

        rev_ranks = {}
        for key, value in ranks.items():
            rev_ranks.setdefault(value, []).append(key)
        for key, value in rev_ranks.items():
            if len(value) > 1:
                output.extend(sorted(value, reverse=True))
            else:
                output.append(*value)
        if len(output) > 5:
            print()
            print(*output[:5], sep="\n")
        else:
            print()
            print(*output, sep="\n")


page_rank = PageRank()
message = int(input("Please enter the number of your stage:\n"))

if message == 1 or message == 2:
    page_rank.print_I_II()
elif message == 3:
     page_rank.print_III()
elif message == 4:
    page_rank.print_IV()
elif message == 5:
    page_rank.print_V()
else:
    print("Please enter an integer from 1 to 5 inclusive!")
    message
