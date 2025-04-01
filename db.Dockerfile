FROM mariadb:latest

# Set environment variables for MariaDB
ENV MYSQL_ROOT_PASSWORD=your_root_password
ENV MYSQL_DATABASE=mydatabase_name

# Expose the MariaDB port
EXPOSE 3306

# Create the database and table on container startup
COPY init.sql /docker-entrypoint-initdb.d/
