import os
from bokeh.io import output_file, save
from bokeh.plotting import figure
from bokeh.models import Slider, ColumnDataSource
from bokeh.layouts import column
from bokeh.models import CustomJS
import numpy as np

# Ensure the assets directory exists
output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'bokeh_line_plot.html')

output_file(output_path)

# Initial parameters
m = 1.0  # Steigung
b = 0.0  # Achsenabschnitt
x = np.linspace(-10, 10, 400)
y = m * x + b

source = ColumnDataSource(data=dict(x=x, y=y))

p = figure(title="Veränderbare Gerade y = m*x + c", width=700, height=400)
p.line('x', 'y', source=source, line_width=3)

slope_slider = Slider(start=-5, end=5, value=m, step=0.1, title="Steigung (m)")
intercept_slider = Slider(start=-10, end=10, value=b, step=0.1, title="Achsenabschnitt (b)")

callback = CustomJS(args=dict(source=source, slope=slope_slider, intercept=intercept_slider), code="""
    const data = source.data;
    const x = data['x'];
    const y = data['y'];
    const m = slope.value;
    const b = intercept.value;
    for (let i = 0; i < x.length; i++) {
        y[i] = m * x[i] + b;
    }
    source.change.emit();
""")

slope_slider.js_on_change('value', callback)
intercept_slider.js_on_change('value', callback)

layout = column(p, slope_slider, intercept_slider)
save(layout)