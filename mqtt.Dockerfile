FROM eclipse-mosquitto:latest

# Copy in the pre-generated keys
COPY ./keys /mosquitto/config/keys

# Copy config from openmoxie
COPY ./site/data/openmoxie.conf /mosquitto/config/mosquitto.conf

# v2.1.2+ entrypoint no longer chowns /mosquitto/log; do it explicitly
RUN chown mosquitto:mosquitto /mosquitto/log

CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]