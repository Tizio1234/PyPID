class Prop:
    def __init__(self, P_GAIN:float):
        self._P_GAIN = P_GAIN
        self._output = 0

    def update(self, cte:float):
        self._output = cte * self._P_GAIN

    @property
    def output(self):
        return self._output

class PropDer:
    def __init__(self, P_GAIN:float, D_GAIN:float):
        self._P_GAIN = P_GAIN
        self._D_GAIN = D_GAIN
        self._output = 0
        self._last_cte = 0
        self._current_cte = 0
        self._current_cter = 0

    def update(self, cte:float):
        self._last_cte = self._current_cte
        self._current_cte = cte
        self._current_cter = self._current_cte - self._last_cte
        self._output = cte * self._P_GAIN + self._current_cter * self._D_GAIN

    @property
    def output(self):
        return self._output

class PropIntDer:
    def __init__(self, P_GAIN:float, D_GAIN:float, I_GAIN:float, CTE_LIST_LENGTH:int):
        if not (isinstance(CTE_LIST_LENGTH, int) and 2 <= CTE_LIST_LENGTH <= 1000):
            raise TypeError("Invalid cte list(int and between 2 and 1000)")
        else:
            self._cte_list_size = CTE_LIST_LENGTH
            self._cte_list = [0.0] * CTE_LIST_LENGTH
        self._P_GAIN = float(P_GAIN)
        self._D_GAIN = float(D_GAIN)
        self._I_GAIN = float(I_GAIN)
        self._output = 0
        self._last_cte = 0
        self._current_cte = 0
        self._current_cter = 0
        self._current_sse = 0
        self._index = 0

    def update(self, cte:float):
        self._last_cte = self._current_cte
        self._current_cte = cte
        self._current_cter = self._current_cte - self._last_cte
        self._cte_list[self._index] = self._current_cte
        self._current_sse = sum(self._cte_list) / self._cte_list_size
        self._index += 1
        if self._index == self._cte_list_size: self._index = 0
        self._output = cte * self._P_GAIN + self._current_cter * self._D_GAIN + self._current_sse * self._I_GAIN

    def reset_integral(self):
        self._cte_list = [0.0]*self._cte_list_size
        self._index = 0

    @property
    def output(self):
        return self._output
