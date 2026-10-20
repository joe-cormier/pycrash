
import numpy as np
import pandas as pd

"""
container for simulation results while a model is running
each column is a numpy array, so the per time step writes used throughout pycrash, such as
veh.model.vx[i] = value, write straight into the array
- pandas 3 (copy-on-write) silently ignores that kind of write on a DataFrame column
- on pandas 2 the same write on a DataFrame costs ~0.3 ms, on a numpy array it is ~100x faster
call to_frame() once the simulation is complete to get the usual DataFrame
"""


class ModelArrays:
    def __init__(self, columns, n_rows=None, fill=np.nan, object_columns=()):
        """ columns: list of column names (all filled with `fill`), or a DataFrame to copy
        object_columns hold any python value (e.g. True / False / NaN) instead of floats """
        object.__setattr__(self, '_data', {})
        if isinstance(columns, pd.DataFrame):
            object.__setattr__(self, '_index', columns.index)
            for col in columns.columns:
                dtype = object if col in object_columns else float
                self._data[col] = columns[col].to_numpy(dtype=dtype, copy=True)
        else:
            object.__setattr__(self, '_index', pd.RangeIndex(n_rows))
            for col in columns:
                self._data[col] = np.full(n_rows, fill, dtype=object if col in object_columns else float)

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name, value):
        self[name] = value

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        """ whole column assignment - a scalar fills the column """
        column = np.asarray(value)
        if column.dtype != object:
            column = column.astype(float)
        self._data[name] = np.full(len(self), column) if column.ndim == 0 else column

    def __contains__(self, name):
        return name in self._data

    def __len__(self):
        return len(self._index)

    @property
    def columns(self):
        return list(self._data)

    def to_frame(self):
        return pd.DataFrame(self._data, index=self._index)


def as_frame(table):
    """ DataFrame for a ModelArrays table, anything else is returned unchanged """
    return table.to_frame() if isinstance(table, ModelArrays) else table
