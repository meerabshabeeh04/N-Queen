import tkinter as tk

N = int(input("Enter a number to solve Queen Problem "))

class NQueensGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("N-Queens Problem")

        self.varDomain = {}
        initDomain = []
        for j in range(1, N + 1):
            initDomain.append(j)

        for i in range(1, N + 1):
            key = f'C{i}'
            self.varDomain[key] = [initDomain]

        self.result = self.MainFunc(self.varDomain)

        self.positions = []
        for keys in self.result.keys():
            self.positions.append(self.result[keys][-1])

        self.Queen = {}
        for i in range(1, N + 1):
            key = f'C{i}'
            self.Queen[key] = self.positions[i - 1]

        self.create_gui()

    def Checkset(self):
        for key, value in self.varDomain.items():
            if isinstance(value[-1], list):
                return key
            else:
                continue
        return "All Set"

    def emptyDomain(self):
        for key, value in self.varDomain.items():
            if isinstance(value[-1], list):
                if len(value[-1]) == 0:
                    return True
        return False

    def Propagate(self, setVar, Value):
        tmpvar1 = int(Value) + 1
        tmpvar2 = int(Value) - 1
        for key, val in self.varDomain.items():
            if isinstance(val[-1], list):
                duplicate = list(val[-1])
                if Value in duplicate:
                    duplicate.remove(Value)
                if tmpvar1 in duplicate:
                    duplicate.remove(tmpvar1)
                if tmpvar2 in duplicate:
                    duplicate.remove(tmpvar2)
                tmpvar1 += 1
                tmpvar2 -= 1
                val.append(duplicate)
        return self.varDomain

    def backtrack(self, setVar, Value):
        var = setVar
        for key in list(self.varDomain.keys())[list(self.varDomain.keys()).index(setVar):]:
            self.varDomain[key].pop()
        if self.varDomain[setVar][-1] == self.varDomain[setVar][0]:
            dupdict = {}
            Domain = []
            dupdom = []
            for j in range(1, N + 1):
                Domain.append(j)
            for val in Domain:
                if val == Value:
                    continue
                else:
                    dupdom.append(val)
            dupdict["C1"] = [dupdom]
            for i in range(2, N + 1):
                key = f'C{i}'
                dupdict[key] = [Domain]
            self.varDomain = dupdict
        else:
            self.varDomain[setVar][-1].remove(Value)
        conflict = self.emptyDomain()
        if conflict is True:
            keys_list = list(self.varDomain.keys())
            ind = keys_list.index(setVar)
            Var = keys_list[int(ind) - 1]
            Val = self.varDomain[Var][-1]
            self.varDomain = self.backtrack(Var, Val)
        return self.varDomain

    def MainFunc(self, varDomain):
        setVar = self.Checkset()
        if setVar == "All Set":
            return varDomain
        else:
            Value = varDomain[setVar][-1][0]
            varDomain[setVar].append(Value)
            varDomain = self.Propagate(setVar, Value)
            conflict = self.emptyDomain()
            if conflict:
                varDomain = self.backtrack(setVar, Value)
                varDomain = self.MainFunc(varDomain)
            else:
                varDomain = self.MainFunc(varDomain)
        return varDomain

    def create_gui(self):
        board_size = 400
        cell_size = board_size // N

        canvas = tk.Canvas(self.master, width=board_size, height=board_size)
        canvas.pack()

        for row in range(N):
            for col in range(N):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                color = "white" if (row + col) % 2 == 0 else "black"
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        for col, row in enumerate(self.Queen.values()):
            col, row = col, row - 1  # Adjust the indexing from 1-based to 0-based
            x, y = col * cell_size + cell_size // 2, row * cell_size + cell_size // 2
            canvas.create_text(x, y, text="♕", font=("Helvetica", cell_size // 2), fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
