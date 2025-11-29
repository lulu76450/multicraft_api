import subprocess
import json
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Serveurs MultiCraft</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h2>Liste des serveurs MultiCraft</h2>
    {% if servers %}
        <table>
            <thead>
                <tr>
                    {% for key in servers[0].keys() %}
                        <th>{{ key }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for server in servers %}
                    <tr>
                        {% for value in server.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Aucun serveur trouvé.</p>
        <h3>Debug JSON :</h3>
        <pre>{{ raw_json }}</pre>
    {% endif %}
</body>
</html>
"""

def fetch_servers():
    cmd = [
        "curl",
        "-s",
        "-H", "Host: menu2.multicraft.network",
        "-H", "User-Agent: MultiCraft/2.0.14 Android [Linux/5.15.180-android13-3-32001549 aarch64]",
        "-H", "Accept: */*",
        "-H", "Accept-Encoding: gzip",
        "-H", "Accept-Language: fr",
        "-H", "Content-Type: application/json",
        "-d", '{"proto_version_min":37,"proto_version_max":39,"platform":"Android"}',
        "https://menu2.multicraft.network/v1/find-nearby-servers"
    ]

    result = subprocess.run(cmd, capture_output=True)
    output = result.stdout

    # Décompresser gzip si nécessaire
    import gzip
    try:
        output = gzip.decompress(output)
    except:
        pass

    # Décoder en UTF-8
    try:
        output = output.decode("utf-8")
    except:
        output = str(output)

    try:
        data = json.loads(output)
        # Vérifier si on a un tableau direct ou un objet avec "servers"
        if isinstance(data, list):
            return data, json.dumps(data, indent=4, ensure_ascii=False)
        elif isinstance(data, dict):
            # Chercher une clé qui contient une liste
            for key, value in data.items():
                if isinstance(value, list):
                    return value, json.dumps(data, indent=4, ensure_ascii=False)
            return [], json.dumps(data, indent=4, ensure_ascii=False)
        else:
            return [], json.dumps(data, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        return [], output

@app.route("/")
def index():
    servers, raw_json = fetch_servers()
    return render_template_string(HTML_TEMPLATE, servers=servers, raw_json=raw_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
