from typing import List

import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.model.sample import Sample, get_sample


@get_sample.register(Settings, pd.DataFrame)
def pandas_get_sample(config: Settings, df: pd.DataFrame) -> List[Sample]:
    """从DataFrame的头部和尾部获取样本

    Args:
        config: 配置对象
        df: pandas DataFrame

    Returns:
        Sample对象的列表
    """
    samples: List[Sample] = []
    if len(df) == 0:
        return samples

    n_head = config.samples.head
    if n_head > 0:
        samples.append(Sample(id="head", data=df.head(n=n_head), name="前几行"))

    n_tail = config.samples.tail
    if n_tail > 0:
        samples.append(Sample(id="tail", data=df.tail(n=n_tail), name="后几行"))

    n_random = config.samples.random
    if n_random > 0:
        samples.append(Sample(id="random", data=df.sample(n=n_random), name="随机样本"))

    return samples
