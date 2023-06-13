from .helper import Helper
from .interfaceDB import interfaceDB
import plotly.graph_objects as go
from plotly.subplots import make_subplots




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

    def plot_clusters_evolution(self, mode= None, clusters_targeted = None):
        """
        For each day from the beginning of the database until now, accumulate 
        the worked time of each cluster and than plot a graph of how each
        cluster has worked for each day.

        Capable of accumulated working time: mode = "accumulated"
        Capable of plotting for a specific set of clusters: clusters_targeted = ["cluster1", "cluster2", ...]
        """
        #--- Get the first day of the database
        first_day = self.interfaceDB_task.get_first_day()
        first_day_string = first_day[0]
        first_day_int = float(first_day[1])

        #--- Get the last day of the database
        last_day = self.interfaceDB_task.get_last_day()
        last_day_string = last_day[0]
        last_day_int = float(last_day[1])

        #--- Pointer that will be used to iterate over the days ---#
        current_day_int = first_day_int


        #--- Draft Dictionary ---#
        clusters_worked_time = {}

        #--- Get existing clusters ---#
        if clusters_targeted == None:
            clusters = self.interfaceDB_task.get_clusters()
        else:
            clusters = []
            for cluster_name in clusters_targeted:
                clusters.append([0, cluster_name])

        #--- create vectors for each cluster ---#
        for cluster in clusters:
            cluster_name = cluster[1]
            if cluster_name != "temp":
                clusters_worked_time[cluster_name] = []

        #--- create vector for days ---#
        days_vector_int = [current_day_int]

        while current_day_int <= last_day_int:
            #--- add the next day ---#
            next_day_int = current_day_int + 86400
            days_vector_int.append(next_day_int)

            #--- Counting worked time of clusters ---#
            for cluster in clusters:
                cluster_name = cluster[1]
                worked_time = self.interfaceDB_task.get_period_worked_time_of_cluster(cluster_name, current_day_int, next_day_int)
                
                #--- check for cleaning conditions ---#
                if worked_time == None:
                    worked_time = 0

                if cluster_name != "temp":
                    if mode== "accumulated" or mode == "polimi":
                        if len(clusters_worked_time[cluster_name]) == 0:
                            clusters_worked_time[cluster_name].append(worked_time)
                        else:
                            clusters_worked_time[cluster_name].append(clusters_worked_time[cluster_name][-1] + worked_time)
                    
                    else:
                        clusters_worked_time[cluster_name].append(worked_time)

            #--- Update the current day with the increased day ---#
            current_day_int = next_day_int
        
        #--- Convert to hours ---#
        for cluster_name in clusters_worked_time.keys():
            
            for i in range(len(clusters_worked_time[cluster_name])):
                clusters_worked_time[cluster_name][i] = round(clusters_worked_time[cluster_name][i]/3600, 2)
                


        #--- POLIMI Mode ---#
        if mode== "polimi":
            clusters_worked_time["polimi"] = []
            iterated_clusters = 0
            for cluster_name in clusters_worked_time.keys():
                #--- Sum the polimi worked time ---#
                if cluster_name == "socialent" or cluster_name == "leadership" or cluster_name == "operation" or cluster_name == "bie" or cluster_name == "plathinking":
                    for i in range(len(clusters_worked_time[cluster_name])):
                        if iterated_clusters == 0:
                            clusters_worked_time["polimi"].append(clusters_worked_time[cluster_name][i])
                        else:
                            clusters_worked_time["polimi"][i] += clusters_worked_time[cluster_name][i]

                    #--- Add iterated clusters ---#
                    iterated_clusters += 1

            #--- Delete the other clusters ---#
            polimi = ["socialent", "leadership", "operation", "bie", "plathinking"]
            for cluster_name in polimi:
                clusters_worked_time.pop(cluster_name)
  

        #--- Plotting ---#
        fig = go.Figure()

        #--- Convert days int to string ---#
        x_values = []
        for day_int in days_vector_int:
            day_string = self.helper.convert_timestamp_to_date(day_int)
            x_values.append(day_string)

        for cluster_name in clusters_worked_time.keys():
            y_values = clusters_worked_time[cluster_name] # list
            
            #--- Add traces ---#
            fig.add_trace(go.Scatter(x= x_values, y= y_values, mode='lines', name= cluster_name))

        fig.update_layout(title='Clusters Evolution (hours)', title_x=0.5)

        # Add a subtitle to the plot
        subtitle_text = f"[{first_day_string} to {last_day_string}]"
        fig.add_annotation(
            xref='paper', yref='paper',
            x=0.5, y=1.1,
            text=subtitle_text,
            showarrow=False,
            font=dict(size=16)
        )
        fig.show()


