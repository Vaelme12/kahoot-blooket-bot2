from flask import Flask, render_template, request, jsonify
import threading
import requests
import time

app = Flask(__name__)

def kahoot_bot(pin, base_name, bot_id):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://kahoot.it/reserve-session/{pin}", headers=headers, timeout=5)
        return r.status_code == 200
    except:
        return False

def blooket_bot(pin, base_name, bot_id):
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        data = {"gameCode": pin, "name": f"{base_name}{bot_id}"}
        r = requests.post("https://api.blooket.com/api/games/join", json=data, headers=headers, timeout=5)
        return r.status_code == 200
    except:
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_bots():
    data = request.get_json()
    game_type = data['game_type']
    pin = data['pin']
    base_name = data['base_name']
    count = min(int(data.get('count', 20)), 60)

    def run():
        for i in range(1, count + 1):
            if game_type == "kahoot":
                threading.Thread(target=kahoot_bot, args=(pin, base_name, i), daemon=True).start()
            else:
                threading.Thread(target=blooket_bot, args=(pin, base_name, i), daemon=True).start()
            time.sleep(0.3)

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"message": f"🚀 {count} Bots gestartet!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
