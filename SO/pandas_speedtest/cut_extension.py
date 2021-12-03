import pandas as pd
import time

ITER = 10


def rm_re(dat: pd.DataFrame) -> pd.Series:
    """Use regular expression."""
    return dat["fname"].str.replace(r'.txt$', '', regex=True)


def rm_map(dat: pd.DataFrame) -> pd.Series:
    """Use pandas map, find occurrences and remove with []"""
    where = dat["fname"].str.endswith(".txt")
    dat.loc[where, "fname"] = dat["fname"].map(lambda x: x[:-4])
    return dat["fname"]


def rm_map2(dat: pd.DataFrame) -> pd.Series:
    """Use pandas map with lambda conditional."""
    return dat["fname"].map(lambda x: x[:-4] if x[-4:] == ".txt" else x)


def rm_apply_str_suffix(dat: pd.DataFrame) -> pd.Series:
    """Use str method suffix with pandas apply"""
    return dat["fname"].apply(str.removesuffix, args=(".txt",))


def rm_suffix(dat: pd.DataFrame) -> pd.Series:
    """Use pandas removesuffix from version 1.6"""
    return dat["fname"].str.removesuffix(".txt")


functions = [rm_map2, rm_apply_str_suffix, rm_map, rm_suffix, rm_re]
print(*["nof. elements", *[func.__name__ for func in functions]], sep="\t")
for base in range(12, 23):
    size = 2**base
    print(size, end="\t")
    data = pd.DataFrame({"fname": ["fn"+str(i) for i in range(size)]})
    data.update(data.sample(frac=.5)["fname"]+".txt")
    for func in functions:
        diff = 0
        for _ in range(ITER):
            data_copy = data.copy()
            start = time.process_time()
            func(data_copy)
            diff += time.process_time() - start

        print(diff, end="\t")
    print("")
