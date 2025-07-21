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
output_path = os.path.join(output_dir, 'bokeh_plot.html')

output_file(output_path)

# Initial parameters
mu = 0
sigma = 1
x = np.linspace(-5, 5, 200)
y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu)/sigma)**2)

source = ColumnDataSource(data=dict(x=x, y=y))

p = figure(title="Adjustable Gaussian Distribution", width=700, height=400)
p.line('x', 'y', source=source, line_width=3)

slider = Slider(start=0.1, end=3, value=1, step=0.01, title="Standard Deviation (σ)")

callback = CustomJS(args=dict(source=source, slider=slider), code="""
    const data = source.data;
    const sigma = slider.value;
    const x = data['x'];
    const y = data['y'];
    for (let i = 0; i < x.length; i++) {
        y[i] = 1/(sigma * Math.sqrt(2 * Math.PI)) * Math.exp(-0.5 * Math.pow(x[i]/sigma, 2));
    }
    source.change.emit();
""")

slider.js_on_change('value', callback)

layout = column(p, slider)
save(layout)