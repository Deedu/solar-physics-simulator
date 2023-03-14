from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions, GKE
from diagrams.gcp.database import BigTable
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS
from diagrams.firebase.develop import Hosting, Firestore
from diagrams.generic.place import Datacenter
from diagrams.gcp.security import KMS
from diagrams.custom import Custom

graph_attr = {
    # "layout": "dot",
    "concentrate": "false",
    "compound": "false",
    "pad": "2.0",
    "splines": "ortho",
    "nodesep": "1.5",
    "ranksep": "1",
    "fontname": "Futura",
    "fontsize": "20",
    "fontcolor": "#2D3436",
    # "splines": "spline"
    # "bgcolor": "orange"
}

REACT_ICON_PATH = "assets/react-icon.png"
GOOGLE_MAPS_ICON_PATH = "assets/google-maps-icon.png"
OPEN_METEO_ICON_PATH = "assets/open-meteo-icon.png"

with Diagram("Solar Physics Simulator", show=False, graph_attr=graph_attr
        , direction="LR"
             ):
    simulation_processing = None

    with Cluster("Client Side"):
        with Cluster("Simulation App\r(app.greatestdemoever.com)"):
            react_app = Custom("React App", REACT_ICON_PATH)

    with Cluster("GCP Cloud Backend"):
        # firestoreIcon = Firestore("Database")
        with Cluster("Request Handling"):
            request_handling = [AppEngine("NestJS Backend")]
        with Cluster("Data Store"):
            bigqueryIcon = BigQuery("Sim Database")

        bigqueryIcon >> Edge() \
                << request_handling

        with Cluster("Simulation Messaging Service"):
            flow = PubSub("PubSub")

        with Cluster("Sim Processing"):
            simulation_processing = [GKE("simulation"), GKE("simulation"), GKE("simulation")]
            flow >> Edge() >> simulation_processing[1]
            simulation_processing[1] >> Edge() \
            << bigqueryIcon

        request_handling >> flow
        react_app >> Edge(color="orange", label="external") \
                << request_handling
        # request_handling >> react_app

        with Cluster("Secrets Management"):
            secrets = KMS("Cloud KMS")
            secrets >> Edge(color="grey", style="dashed") >> request_handling
            secrets >> Edge(color="grey", style="dashed") >> simulation_processing[1]

    with Cluster("External APIs"):
        weather_cluster = Custom("OpenMeteo API", OPEN_METEO_ICON_PATH)
        # weather_cluster >> simulation_processing[0]
        simulation_processing[1] >> Edge(color="orange", label="") \
                << weather_cluster
        google_maps_cluster = Custom("Google Maps API", GOOGLE_MAPS_ICON_PATH)
        # google_maps_cluster >> simulation_processing[0]
        simulation_processing[1] >> Edge(color="orange", label="") \
                << google_maps_cluster
