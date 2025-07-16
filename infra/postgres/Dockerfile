FROM postgres:17.5-alpine3.22

# changing permissions of the init script directory recursively for the postgres user to own future files
USER root
RUN chown postgres:postgres -R /docker-entrypoint-initdb.d/
USER postgres

# getting the init scripts
COPY init-scripts/* /docker-entrypoint-initdb.d/

# running the builtin entrypoint script when container starts
ENTRYPOINT ["docker-entrypoint.sh"]
# running the database after entrypoint finishes
CMD ["postgres"]