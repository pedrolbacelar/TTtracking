import plotly.graph_objects as go
from lib.tttracking.plotter import Plotter
plotter = Plotter("Plotter")

#Plotter("Plotter").plot_clusters_overview()
#Plotter("Plotter").plot_clusters_week()

plotter.plot_clusters_day()