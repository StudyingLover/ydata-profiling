from typing import List, Optional

from ydata_profiling.config import Settings
from ydata_profiling.model import BaseDescription
from ydata_profiling.report.presentation.core import Container, CorrelationTable, Image
from ydata_profiling.report.presentation.core.renderable import Renderable
from ydata_profiling.visualisation import plot


def get_correlation_items(
    config: Settings, summary: BaseDescription
) -> Optional[Renderable]:
    """创建相关性项的列表

    Args:
        config: 报告配置对象
        summary: 相关性字典

    Returns:
        要在界面中显示的相关性项列表。
    """
    items: List[Renderable] = []

    key_to_data = {
        "pearson": (-1, "皮尔逊相关系数 (Pearson's r)"),
        "spearman": (-1, "斯皮尔曼相关系数 (Spearman's ρ)"),
        "kendall": (-1, "肯德尔相关系数 (Kendall's τ)"),
        "phi_k": (0, "Phik (φk)"),
        "cramers": (0, "克雷梅尔V系数 (Cramér's V (φc))"),
        "auto": (-1, "自动 (Auto)"),
    }

    image_format = config.plot.image_format

    for key, item in summary.correlations.items():
        vmin, name = key_to_data[key]

        if isinstance(item, list):
            diagrams: List[Renderable] = []
            for idx, i in enumerate(item):
                diagram: Renderable = Image(
                    plot.correlation_matrix(config, i, vmin=vmin),
                    image_format=image_format,
                    alt=name,
                    anchor_id=f"{key}_diagram",
                    name=config.html.style._labels[idx],
                    classes="correlation-diagram",
                )
                diagrams.append(diagram)

            diagrams_grid = Container(
                diagrams,
                anchor_id=f"{key}_diagram_with_desc",
                name="热图" if config.correlation_table else name,
                sequence_type="batch_grid",
                batch_size=len(config.html.style._labels),
            )

            if config.correlation_table:
                tables: List[Renderable] = []
                for idx, i in enumerate(item):
                    table = CorrelationTable(
                        name=config.html.style._labels[idx],
                        correlation_matrix=i,
                        anchor_id=f"{key}_table",
                    )
                    tables.append(table)

                tables_tab = Container(
                    tables,
                    anchor_id=f"{key}_tables",
                    name="表格",
                    sequence_type="batch_grid",
                    batch_size=len(config.html.style._labels),
                )

                diagrams_tables_tab = Container(
                    [diagrams_grid, tables_tab],
                    anchor_id=f"{key}_diagram_table",
                    name=name,
                    sequence_type="tabs",
                )

                items.append(diagrams_tables_tab)
            else:
                items.append(diagrams_grid)
        else:
            diagram = Image(
                plot.correlation_matrix(config, item, vmin=vmin),
                image_format=image_format,
                alt=name,
                anchor_id=f"{key}_diagram",
                name="热图" if config.correlation_table else name,
                classes="correlation-diagram",
            )

            if config.correlation_table:
                table = CorrelationTable(
                    name="表格", correlation_matrix=item, anchor_id=f"{key}_table"
                )

                diagram_table_tabs = Container(
                    [diagram, table],
                    anchor_id=f"{key}_diagram_table",
                    name=name,
                    sequence_type="tabs",
                )

                items.append(diagram_table_tabs)
            else:
                items.append(diagram)

    corr = Container(
        items,
        sequence_type="tabs",
        name="相关性",
        anchor_id="correlations_tab",
    )

    if len(items) > 0:
        return corr

    return None
