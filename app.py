import time
import logging
import redis
from flask import Flask, render_template_string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
db = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return db.incr('hits')
        except redis.exceptions.ConnectionError as e:
            if retries == 0:
                logger.error("Redis connection failed after multiple retries.")
                raise e
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def index():
    try:
        hits = get_hit_count()
        logger.info(f"Request served. Hit count: {hits}")
    except Exception as e:
        logger.error(f"Hit counter error: {e}")
        return "Database connection error", 500

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Visitor Counter</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background: #0f172a;
                color: #f8fafc;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                text-align: center;
                background: #1e293b;
                padding: 3rem;
                border-radius: 1rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                border: 1px solid #334155;
            }
            h1 {
                margin: 0 0 1rem 0;
                font-size: 2rem;
                color: #38bdf8;
            }
            .counter {
                font-size: 4.5rem;
                font-weight: 800;
                color: #f43f5e;
            }
            p {
                color: #94a3b8;
                font-size: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Visitor Counter</h1>
            <p>This page has been viewed</p>
            <div class="counter">{{ hits }}</div>
            <p>times</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, hits=hits)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
