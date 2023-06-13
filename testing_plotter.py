from lib.tttracking.plotter import Plotter

plotter = Plotter("test")
# plotter.plot_clusters_evolution()
# plotter.plot_clusters_evolution(mode="accumulated")
# plotter.plot_clusters_evolution(clusters_targeted=["dt", "jobs", "socialent"])
# plotter.plot_clusters_evolution(clusters_targeted=["dt", "jobs", "socialent"], mode="accumulated")

plotter.plot_clusters_evolution(mode="polimi")

