from flask import Flask, render_template, jsonify
import platform

if platform.system() == "Windows":
    import pywifi
    from pywifi import const
else:
    import wifi

app = Flask(__name__)

def scan_wifi():
    if platform.system() == "Windows":
        wifi_scanner = pywifi.PyWiFi()
        iface = wifi_scanner.interfaces()[0]
        iface.scan()
        results = iface.scan_results()
        networks = [{"ssid": result.ssid, "signal": result.signal} for result in results]
    else:
        cells = wifi.Cell.all('wlan0')  # Adjust interface name as needed
        networks = [{"ssid": cell.ssid, "signal": cell.signal} for cell in cells]

    return networks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    networks = scan_wifi()
    return jsonify(networks)

if __name__ == '__main__':
    app.run(debug=True)
