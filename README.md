
## Installation

First, clone project from repo:

```bash
# paste
git clone https://github.com/erkartik2001/GPT-Doc-Chatbot.git
```

Install all dependency:

```bash
# paste
pip install -r "requirements.txt"
```

Create ``` .env``` file.

Add ``` PINECONE_API_KEY=ENTER_YOUR_PINECONE_KEY ``` in .env file.

Add ``` POSTGRESQL_CONNECTION_URI=ENTER_YOUR_POSTGREURI``` in .env file.

## For Development

Run the development server:

```bash
# paste
python main_beta.py
```

Enter url [http://127.0.0.1:8000](http://127.0.0.1:8000) in frontend ```.env``` file.



## For Production

Install dependency:

```bash
# paste
pip install -g eventlet gunicorn
```

Run the production server:

```bash
# paste
gunicorn -k eventlet -w 1 main_beta:app
```


