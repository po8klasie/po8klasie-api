/bin/sh

database="warsawlo"
install_trg() {
  if hash postgresql-contrib 2>/dev/null; then
    echo "postgresql installed"
  else
    sudo apt install postgresql-contrib
  fi
}

install_trg

# run as postgres user
sudo -ui postgres

# create a database with encoding UTF-8
createdb -E utf8 $database

# install pg_trgm extension
psql -d $database -c "CREATE EXTENSION pg_trgm"