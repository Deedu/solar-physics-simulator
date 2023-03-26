FROM gcr.io/buildpacks/gcp/run:v1
USER root
ENV GRPC_POLL_STRATEGY=poll
ENV GOOGLE_MAPS_API_KEY $GOOGLE_MAPS_API_KEY
RUN apt-get update
USER cnb
CMD ["./testingScript.sh"]

#volumes:
#  - ~/.config/:/root/.config
#  - ~/.config/gcloud