

### How to get started

1. Clone the repo
```bash
git clone https://github.com/SkuliX01/banking-system.git
```
2. Copy the .env.sample into .env
```bash
cp .env.sample .env
```

3. Setup your database
- Create a database with a name of your choice, e.g. "banking"
- Go to .env and put in your connection details into `MONGO_CONNECTION_STRING` and your database name (e.g. "banking") into `MONGO_DATABASE_NAME`

4. Run userdashboard.py
```bash
python userdashboard.py
```