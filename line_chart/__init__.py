# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import io
import matplotlib
import matplotlib.pyplot as plt
from typing import Optional, Any, Dict
import base64
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


class LineChart(
    BaseComponent,
    component_name="Line chart",
    component_description="""Plots a line chart given a dictionary with numerical keys and values. The output can be linked to a report component.
Inputs:
  `Data` (Dict[Union(int,float), Union(int,float)]): A dictionary with keys (int or float) mapped to numerical values (int or float).
Output (Dict): A dictionary with the key `data` (str) mapped to the original input data (Dict[Any, Union[int, float]]), """ \
        """and the key `images` (str) mapped to a list (List[str]) with one element which is the produced image (the line chart) encoded in base64 on the format """ \
        """`f`data:image/png;base64,{base64.b64encode(binary_buffer_of_PNG.read()).decode()}`` (str).""",
    input_types={"data": DataType.JSON},
    output_type=DataType.LINE_CHART,
    component_group=ComponentGroup.DATA_VISUALIZATION,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    @staticmethod
    def plot_line_chart(input_dict):
        keys = list(map(lambda key: int(key), input_dict.keys()))
        values = list(input_dict.values())

        matplotlib.use("agg")

        # Plot the bar chart
        plt.plot(keys, values)
        plt.xlabel("Keys")
        plt.ylabel("Values")
        plt.title("Line Chart")

        # Save the plot to a BytesIO buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        # Convert the BytesIO buffer to a base64-encoded PNG string URL
        png_string_url = f"data:image/png;base64,{base64.b64encode(buffer.read()).decode()}"

        # Close the plot to free resources
        plt.close()

        return png_string_url

    def run(
        self,
        data: Dict,
    ):
        images = [self.__class__.plot_line_chart(data)]
        return {"data": data, "images": images}
