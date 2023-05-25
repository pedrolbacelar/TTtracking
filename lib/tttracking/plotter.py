from .helper import Helper
from .interfaceDB import interfaceDB
import plotly.graph_objects as go



class Plotter():
    def __init__(self, name):
        self.name = name
        self.helper = Helper()
        self.interfaceDB_task = interfaceDB("task")

    # =============== TAKS PLOTTER =============== #
    def plot_clusters_overview(self, mode= "pizza"):
        """
        Plot different comparasions of how much each cluster has been used
        in terms of minutes. Depending of the mode selected each plot
        different graphs.
        """
        clusters_worked_time = {}

        #--- Get existing clusters ---#
        clusters = self.interfaceDB_task.get_clusters()

        #--- Counting worked time of clusters ---#
        for cluster in clusters:
            cluster_name = cluster[1]
            worked_time = self.interfaceDB_task.get_all_worked_time_of_cluster(cluster_name)
            clusters_worked_time[cluster_name] = worked_time

        #--- clean data ---#
        cluster_worked_clean = {}
        for cluster_name in clusters_worked_time.keys():
            if clusters_worked_time[cluster_name] == 0 or clusters_worked_time[cluster_name] == None or cluster_name == "temp":
                pass
            else:
                cluster_worked_clean[cluster_name] = clusters_worked_time[cluster_name]

        #--- Convert to hours ---#
        for cluster_name in cluster_worked_clean.keys():
            cluster_worked_clean[cluster_name] = round(cluster_worked_clean[cluster_name]/3600, 2)

        #--- Plotting ---#
        if mode == "pizza":
            fig = go.Figure(data=[go.Pie(labels=list(cluster_worked_clean.keys()), values=list(cluster_worked_clean.values()))])
        
        if mode == "bar":
            fig = go.Figure(data=[go.Bar(x=list(cluster_worked_clean.keys()), y=list(cluster_worked_clean.values()))])

        fig.update_layout(title='Clusters Full Overview (hours)', title_x=0.5)
        fig.show()
    
    def plot_clusters_week(self):
        """
        Plot the clusters worked time of the current week.
        """
        #--- Get first and last day of the week ---#
        (first_week_day, last_week_day) = self.helper.get_week()

        #--- Draft Dictionary ---#
        clusters_worked_time = {}

        #--- Get existing clusters ---#
        clusters = self.interfaceDB_task.get_clusters()

        #--- Counting worked time of clusters ---#
        for cluster in clusters:
            cluster_name = cluster[1]
            worked_time = self.interfaceDB_task.get_period_worked_time_of_cluster(cluster_name, first_week_day, last_week_day)
            clusters_worked_time[cluster_name] = worked_time

        #--- clean data ---#
        cluster_worked_clean = {}
        for cluster_name in clusters_worked_time.keys():
            if clusters_worked_time[cluster_name] == 0 or clusters_worked_time[cluster_name] == None or cluster_name == "temp":
                pass
            else:
                cluster_worked_clean[cluster_name] = clusters_worked_time[cluster_name]

        #--- Convert to hours ---#
        for cluster_name in cluster_worked_clean.keys():
            cluster_worked_clean[cluster_name] = round(cluster_worked_clean[cluster_name]/3600, 2)

        #--- Plotting ---#
        fig = go.Figure(data=[go.Pie(labels=list(cluster_worked_clean.keys()), values=list(cluster_worked_clean.values()))])
        
        fig.update_layout(title='Clusters Week Overview (hours)', title_x=0.5)
        
        # Add a subtitle to the plot
        subtitle_text = f"[{first_week_day} to {last_week_day}]"
        fig.add_annotation(
            xref='paper', yref='paper',
            x=0.5, y=1.1,
            text=subtitle_text,
            showarrow=False,
            font=dict(size=16)
)
        fig.show() 

    def plot_clusters_day(self):
        """
        Plot the clusters worked time of the current day.
        """
        #--- Get first and last day of the week ---#
        (current_day, previous_day) = self.helper.get_current_and_previous_day()

        #--- Draft Dictionary ---#
        clusters_worked_time = {}

        #--- Get existing clusters ---#
        clusters = self.interfaceDB_task.get_clusters()

        #--- Counting worked time of clusters ---#
        for cluster in clusters:
            cluster_name = cluster[1]
            worked_time = self.interfaceDB_task.get_period_worked_time_of_cluster(cluster_name, previous_day, current_day)
            clusters_worked_time[cluster_name] = worked_time

        #--- clean data ---#
        cluster_worked_clean = {}
        for cluster_name in clusters_worked_time.keys():
            if clusters_worked_time[cluster_name] == 0 or clusters_worked_time[cluster_name] == None or cluster_name == "temp":
                pass
            else:
                cluster_worked_clean[cluster_name] = clusters_worked_time[cluster_name]

        #--- Convert to hours ---#
        for cluster_name in cluster_worked_clean.keys():
            cluster_worked_clean[cluster_name] = round(cluster_worked_clean[cluster_name]/3600, 2)

        #--- Plotting ---#
        fig = go.Figure(data=[go.Pie(labels=list(cluster_worked_clean.keys()), values=list(cluster_worked_clean.values()))])
        
        fig.update_layout(title='Clusters Day Overview (hours)', title_x=0.5)
        # Add a subtitle to the plot
        subtitle_text = f"[{previous_day} to {current_day}]"
        fig.add_annotation(
            xref='paper', yref='paper',
            x=0.5, y=1.1,
            text=subtitle_text,
            showarrow=False,
            font=dict(size=16)
        )
        fig.show()