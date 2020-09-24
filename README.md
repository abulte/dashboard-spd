# dashboard-spd

## Usage

### Add measurement

`POST /api/measurement (201)`

```json
{
  "project": "data.gouv.fr",
  "interval": {
    "start": "1977-04-22T00:00:00Z",
    "end": "1977-04-23T00:00:00Z"
  },
  "measurement": {
    "name": "visits",
    "value": 10000
  }
}
```

### Development

Launch backend:

```
python3 -mvenv pyenv
. pyenv/bin/activate
cd backend
python cli.py init-db
FLASK_DEBUG=1 FLASK_APP=app flask run
```

Launch frontend:

```
cd frontend
yarn
yarn serve
```

The frontend is available on http://localhost:8080 and uses the API available at http://localhost:5000.

### Production (dokku)

This project uses two buildpacks, `node` and `python`, to build and install both frontend and backend.

On the dokku server, prepare the postgres database and create the app:

```
dokku apps:create simple-spa
dokku postgres:create simple-spa
dokku postgres:link simple-spa simple-spa
```

On local copy:

```
git remote add dokku dokku@{host}:simple-spa
git push dokku master
```

The deployment process will run `init-db` thanks to the Procfile.

Get a SSL certificate and redirect to https:

```
dokku letsencrypt simple-spa
```

:rocket: https://simple-spa.{host}/api
