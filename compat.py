"""Compatibilidade do Experta com Python 3.10+.

O Experta 1.9.4 ainda importa ``collections.Mapping`` (e similares), nomes que
foram movidos para ``collections.abc`` no Python 3.10. Este módulo recria esses
apelidos antes de o Experta ser importado.
"""
import collections
import collections.abc

for _nome in ("Mapping", "MutableMapping", "Sequence", "Iterable", "Callable", "Hashable"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))
