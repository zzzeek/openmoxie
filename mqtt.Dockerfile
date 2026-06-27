FROM eclipse-mosquitto:latest

# Copy in the pre-generated keys
COPY ./keys /mosquitto/config/keys

# Copy config from openmoxie
COPY ./site/data/openmoxie.conf /mosquitto/config/mosquitto.conf

# v2.1.2+ entrypoint no longer chowns /mosquitto/log at runtime; chown
# via CMD since /mosquitto/log is a bind mount overlaid at container start
CMD ["sh", "-c", "chown -R mosquitto:mosquitto /mosquitto/log && exec mosquitto -c /mosquitto/config/mosquitto.conf"]