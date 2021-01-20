from .il import ilta_lehti
from .sanoma import helsingin_sanomat, ilta_sanomat
from .yle import yle_uutiset
from .mtv import mtv_uutiset
import time
import threading


def fetch_all():
    threads = []
    result = {}

    def add_to_dict(keyname, fecher_func):
        result[keyname] = fecher_func()
    
    pairs = {
        "il": ilta_lehti,
        "yle": yle_uutiset,
        "is": ilta_sanomat,
        "hs": helsingin_sanomat,
        "mtv": mtv_uutiset
    }
    
    for key in pairs:
        t = threading.Thread(target=add_to_dict, args=[key, pairs[key]])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    return(result)
