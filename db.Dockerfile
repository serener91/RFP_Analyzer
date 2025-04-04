FROM mariadb:latest

# Set environment variables for MariaDB
ENV MYSQL_ROOT_PASSWORD=mypassword
ENV MYSQL_DATABASE=mydatabase

# Expose the MariaDB port
EXPOSE 3306

WORKDIR /app

# Create the database and table on container startup
COPY /database/init.sql /docker-entrypoint-initdb.d/
