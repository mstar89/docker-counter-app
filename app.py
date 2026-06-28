import time
import redis
from flask import Flask, render_template_string

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Docker Compose Counter</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
                color: white;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                text-align: center;
                background: rgba(255, 255, 255, 0.05);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(15px);
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            h1 {
                margin: 0 0 20px 0;
                font-size: 2.5rem;
                color: #0db7ed;
            }
            .counter {
                font-size: 5rem;
                font-weight: bold;
                color: #ff6b6b;
                text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
            }
            p {
                color: #a0aec0;
                font-size: 1.1rem;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🐳 Docker Compose Counter</h1>
            <p>This page has been viewed</p>
            <div class="counter">{{ count }}</div>
            <p>times</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
