from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

# MD5 hash of: flag{multi_shift_caesar_is_fun}
FLAG_HASH = "9bf0e0d947df2f6edf004d32f5cefdba"

# Ciphertext using per-word Caesar shifts
CIPHERTEXT = "iodj{rzqyn_zopma_ljnbja_td_sha}"

# ----------------------- PAGE 1 -----------------------
PAGE_INTRO = r"""
<!doctype html>
<html>
<head>
<title>The Lost Caesar Scrolls – Part I</title>
<style>
body { background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:80px; }
.card { background:#1c1c1c; display:inline-block; padding:30px 40px; border-radius:10px; box-shadow:0 0 15px #000; }
button { background:#ff9800; padding:10px 20px; border-radius:6px; border:none; cursor:pointer; margin-top:20px; }
</style>
</head>
<body>
<div class="card">
    <h2>The Lost Caesar Scrolls</h2>
    <p>You discovered a mysterious encrypted fragment in an ancient vault.</p>

    <code>io...</code>

    <p><i>"Caesar never marched with one army alone..."</i></p>

    <form action="/clue">
        <button type="submit">Continue →</button>
    </form>
</div>
</body>
</html>
"""

# ----------------------- PAGE 2 -----------------------
PAGE_CLUE = r"""
<!doctype html>
<html>
<head>
<title>Clue Room</title>
<style>
body { background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:60px; }
.card { background:#1c1c1c; padding:30px 40px; display:inline-block; border-radius:10px; box-shadow:0 0 15px #000; }
button { background:#03a9f4; padding:10px 20px; border:none; border-radius:6px; cursor:pointer; margin-top:20px; }
.hint { color:#bbb; }
</style>
</head>
<body>

<!-- REAL HINT: Each word = 1 unit, each unit = 1 Caesar shift -->

<div class="card">
    <h2>Clue Room</h2>

    <p class="hint">Clue #1: Try ROT13?</p>
    <p class="hint">Clue #2: Some alphabets dance faster than others.</p>
    <p class="hint"><b>Clue #3: Shifts vary per unit. Units are separated.</b></p>

    <form action="/challenge">
        <button type="submit">Go to Encrypted Message →</button>
    </form>
</div>
</body>
</html>
"""

# ----------------------- PAGE 3 -----------------------
PAGE_CHALLENGE = r"""
<!doctype html>
<html>
<head>
<title>Caesar Battalions Challenge</title>
<style>
body { background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:70px; }
.card { background:#1c1c1c; padding:30px 40px; border-radius:10px; display:inline-block; box-shadow:0 0 15px #000; }
code { background:#222; padding:10px; border-radius:6px; display:block; margin-top:10px; }
button { background:#4caf50; padding:10px 20px; border:none; border-radius:6px; cursor:pointer; margin-top:20px; }
input { width:90%; padding:10px; margin-top:15px; border-radius:6px; border:1px solid #444; background:#111; color:#eee; }
.msg.ok { color:#4caf50; font-weight:bolder; margin-top:10px; }
.msg.err { color:#e91e63; font-weight:bolder; margin-top:10px; }
</style>
</head>
<body>
<div class="card">
    <h2>Encrypted Message</h2>

    <code>{{ ciphertext }}</code>

    <p><i>"A single army never marched this message. Each battalion used its own Caesar."</i></p>

    <form method="POST">
        <input type="text" name="flag" placeholder="flag{...}">
        <button type="submit">Submit Flag</button>
    </form>

    {% if message %}
        <div class="msg {{ css_class }}">{{ message }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def intro():
    return render_template_string(PAGE_INTRO)

@app.route("/clue")
def clue():
    return render_template_string(PAGE_CLUE)

@app.route("/challenge", methods=["GET","POST"])
def challenge():
    message = ""
    css_class = ""
    if request.method == "POST":
        guess = request.form.get("flag", "").strip()
        guess_hash = hashlib.md5(guess.encode()).hexdigest()

        if guess_hash == FLAG_HASH:
            message = "🎉 Correct! All Caesars obey your command."
            css_class = "ok"
        else:
            message = "❌ Incorrect. Each word uses a different shift!"
            css_class = "err"

    return render_template_string(
        PAGE_CHALLENGE,
        ciphertext=CIPHERTEXT,
        message=message,
        css_class=css_class
    )

if __name__ == "__main__":
    app.run(port=8000, debug=False)
