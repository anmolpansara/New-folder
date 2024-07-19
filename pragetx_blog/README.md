git clone
```
cd astrosphere-backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
CREATE DATABASE tracking;;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tracking; TO myuser;


GRANT ALL PRIVILEGES ON SCHEMA public TO myuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;
ALTER DATABASE tracking OWNER TO myuser; 