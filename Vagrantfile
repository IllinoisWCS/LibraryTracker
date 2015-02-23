Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "wcs-library-tracker.dev"
  config.vm.network "forwarded_port", guest: 5432, host: 15432

  config.vm.provision "shell", inline: <<-SHELL
    set -e
    export DEBIAN_FRONTEND=noninteractive
    print_db_usage () {
        echo "Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: 15432)"
        echo "  Host: localhost"
        echo "  Port: 15432"
        echo "  Database: $APP_DB_NAME"
        echo "  Username: $APP_DB_USER"
        echo "  Password: $APP_DB_PASS"
        echo ""
        echo "Admin access to postgres user via VM:"
        echo "  vagrant ssh"
        echo "  sudo su - postgres"
        echo ""
        echo "psql access to app database user via VM:"
        echo "  vagrant ssh"
        echo "  sudo su - postgres"
        echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost $APP_DB_NAME"
        echo ""
        echo "Env variable for application development:"
        echo "  DATABASE_URL=postgresql://$APP_DB_USER:$APP_DB_PASS@localhost:15432/$APP_DB_NAME"
        echo ""
        echo "Local command to access the database via psql:"
        echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost -p 15432 $APP_DB_NAME"
    }
    PROVISIONED_ON=/etc/vm_provision_on_timestamp
    if [ -f "$PROVISIONED_ON" ]
    then
        echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
        echo "To run system updates manually login via 'vagrant ssh' and run 'apt-et update && apt-get upgrade'"
        echo ""
        print_db_usage
        exit
    fi

    PG_VERSION=9.3
    PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
    PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
    PG_DIR="/etc/postgresql/$PG_VERSION/main"

    # Set the database name, database user, and user's password
    APP_DB_USER=wcs
    APP_DB_PASS=wcssuperawesomepassword
    APP_DB_NAME=librarytracker

    # Update the package list and upgrade all packages
    apt-get update
    apt-get -y upgrade
    apt-get -y install postgresql-$PG_VERSION postgresql-contrib-$PG_VERSION

    # Edit postgresql.conf to change listen address to '*':
    sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

    # Append to pg_hba.conf to add password auth:
    echo "host    all             all             all                     md5" >> "$PG_HBA"

    # Explicitly set the default client_encoding
    echo "client_encoding = utf8" >> "$PG_CONF"

    # Restart so that all new config is loaded:
    service postgresql restart

    cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

# Tag the provision time:
date > "$PROVISIONED_ON"

echo "Successfully created PostgreSQL dev virtual machine."
echo ""
print_db_usage
  SHELL
end
