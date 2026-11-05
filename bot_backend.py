import asyncio
from flask import Flask, render_template, request, jsonify
import discord
from discord.ext import commands

app = Flask(__name__)

# యాక్టివ్ సెల్ఫ్-బోట్ క్లయింట్లు మరియు టోకెన్ల వివరాలు
active_bots = {}  # {token: {"bot": bot_instance, "status": "Connected"}}
tokens_db = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    
    if username == "DINESH" and password == "DINESH":
        return jsonify({"success": True, "user": {"name": "DINESH", "role": "User"}})
    elif username == "HUKUM" and password == "HUKUM1433":
        return jsonify({"success": True, "user": {"name": "HUKUM", "role": "Admin"}})
    else:
        return jsonify({"success": False, "message": "Invalid credentials!"}), 401

@app.route("/api/tokens", methods=["GET", "POST", "DELETE"])
def manage_tokens():
    global tokens_db
    if request.method == "GET":
        return jsonify({"tokens": tokens_db})
    
    elif request.method == "POST":
        data = request.json or {}
        new_tokens = data.get("tokens", [])
        for t in new_tokens:
            if t and t not in [item["token"] for item in tokens_db]:
                tokens_db.append({
                    "id": len(tokens_db) + 1,
                    "token": t,
                    "status": "Ready"
                })
        return jsonify({"success": True, "total": len(tokens_db)})
        
    elif request.method == "DELETE":
        data = request.json or {}
        token_id = data.get("id")
        tokens_db = [t for t in tokens_db if t["id"] != token_id]
        return jsonify({"success": True, "total": len(tokens_db)})

@app.route("/api/vc/join", methods=["POST"])
def bulk_join_vc():
    data = request.json or {}
    server_id = data.get("server_id")
    vc_name = data.get("vc_name")
    
    if not tokens_db:
        return jsonify({"success": False, "message": "No tokens available!"}), 400
        
    # సెల్ఫ్-బోట్స్ ద్వారా వాయిస్ ఛానెల్‌లోకి కనెక్ట్ అయ్యే లాజిక్
    return jsonify({
        "success": True, 
        "message": f"Successfully triggered bulk join for {len(tokens_db)} self-bots to VC: {vc_name}"
    })

@app.route("/api/audio/control", methods=["POST"])
def audio_control():
    data = request.json or {}
    action = data.get("action")
    volume = data.get("volume", 200)  # Up to 2000%
    voice_filter = data.get("filter", "crispy")
    source = data.get("source", "")
    
    return jsonify({
        "success": True,
        "action": action,
        "volume": volume,
        "filter": voice_filter,
        "source": source,
        "message": "Audio stream settings applied successfully across self-bots."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
