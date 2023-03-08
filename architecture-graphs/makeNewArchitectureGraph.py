from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions, GKE
from diagrams.gcp.database import BigTable
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS
from diagrams.firebase.develop import Hosting, Firestore
from diagrams.generic.place import Datacenter
from diagrams.custom import Custom

graph_attr = {
    # "layout": "dot",
    # "concentrate": "true",
    # "compound": "true",
    # "splines": "spline",
}

REACT_ICON_PATH = "readmeAssets/react-1-logo-png-transparent.png"
GOOGLE_MAPS_ICON_PATH = "assets/google-maps-icon.png"
OPEN_METEO_ICON_PATH = "assets/open-meteo-icon.png"

with Diagram("Solar Physics Simulator", show=False, graph_attr=graph_attr):
    with Cluster("GCP Cloud Backend"):
        # firestoreIcon = Firestore("Database")

        with Cluster("Data Store"):
            bigqueryIcon = BigQuery("Simulations Database")
        with Cluster("Request Handling"):
            request_handling = AppEngine("NestJS Backend")

        bigqueryIcon << request_handling
        bigqueryIcon >> request_handling

        with Cluster("Simulation Messaging Service"):
            flow = PubSub("PubSub")

        with Cluster("Simulation Processing"):
            simulation_processing = [GKE("simulation"), GKE("simulation"), GKE("simulation")]
            flow >> simulation_processing[1]
            simulation_processing[1] >> bigqueryIcon

        request_handling >> flow

    with Cluster("Client Side"):
        with Cluster("Simulation App\r(app.greatestdemoever.com)"):
            react_app = [Hosting("React App")]
            react_app[0] >> request_handling
            request_handling >> react_app[0]

    with Cluster("Weather Data"):
        weather_cluster = [Custom("OpenMeteo API", OPEN_METEO_ICON_PATH)]
        # weather_cluster >> simulation_processing[0]
        weather_cluster >> simulation_processing[1]

    with Cluster("Google Maps API"):
        google_maps_cluster = [Custom("Google Maps API", GOOGLE_MAPS_ICON_PATH)]
        # google_maps_cluster >> simulation_processing[0]
        google_maps_cluster >> simulation_processing[1]

# with Cluster("Notifications For Users"):
#     twillio = Custom("Twillio", TWILIO_ICON_PATH)
#     sendgrid = Custom("SendGrid", SENDGRID_ICON_PATH)

# monitoringAndText >> twillio
#
# monitoringAndText >> flow
