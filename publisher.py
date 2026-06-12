import time
import random
import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

BROKER_HOST = "localhost"
BROKER_PORT = 1883
USERNAME = "user_tani"
PASSWORD = "kata_kunci_tani"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[PUBLISHER] Terhubung ke broker sukses. Kode Alasan: {reason_code}")
    else:
        print(f"[PUBLISHER] Kegagalan koneksi ke broker. Kode Alasan: {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"[PUBLISHER] Pesan berhasil dipublikasikan. ID Pesan (mid): {mid}")

def main():
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="Agri Publisher Node")
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"Menghubungkan ke broker Mosquitto di {BROKER_HOST}:{BROKER_PORT}...")
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    try:
        print("\n=== Skenario 1 & 3: Mengirim Data Sensor ke Beberapa Topik ===")
        temp = round(random.uniform(26.5, 32.0), 2)
        hum = round(random.uniform(65.0, 80.0), 2)
        soil_a = round(random.uniform(30.0, 45.0), 2)

        client.publish("tani/field1/zoneA/sensor/temperature", json.dumps({"value": temp, "unit": "C"}), qos=0)
        client.publish("tani/field1/zoneA/sensor/humidity", json.dumps({"value": hum, "unit": "%"}), qos=0)
        client.publish("tani/field1/zoneB/sensor/soil_moisture", json.dumps({"value": soil_a, "unit": "%"}), qos=0)
        time.sleep(2)

        print("\n=== Skenario 2: Eksperimen Pengiriman dengan QoS Berbeda ===")
        topic_qos_test = "tani/field1/zoneA/sensor/temperature"
        
        print(f"Mengirim pesan QoS 0 (Fire and Forget) ke {topic_qos_test}...")
        client.publish(topic_qos_test, json.dumps({"telemetry": 28.5, "qos_level": 0}), qos=0)
        time.sleep(1)

        print(f"Mengirim pesan QoS 1 (Menunggu PUBACK dari Broker)...")
        msg_info = client.publish(topic_qos_test, json.dumps({"telemetry": 28.6, "qos_level": 1}), qos=1)
        msg_info.wait_for_publish()
        time.sleep(1)

        print(f"Mengirim pesan QoS 2 (Jabat Tangan 4 Arah Dijamin Tepat Sekali)...")
        msg_info2 = client.publish(topic_qos_test, json.dumps({"telemetry": 28.7, "qos_level": 2}), qos=2)
        msg_info2.wait_for_publish()
        time.sleep(2)

        print("\n=== Memulai Pengiriman Berkelanjutan untuk Pengujian Wildcard Klien ===")
        print("Sistem berjalan secara real-time. Tekan Ctrl+C untuk keluar.")
        
        while True:
            temp = round(random.uniform(24.0, 34.0), 2)
            hum = round(random.uniform(55.0, 85.0), 2)
            soil_a = round(random.uniform(20.0, 50.0), 2)
            soil_b = round(random.uniform(20.0, 50.0), 2)

            client.publish("tani/field1/zoneA/sensor/temperature", json.dumps({"value": temp}), qos=1)
            client.publish("tani/field1/zoneA/sensor/humidity", json.dumps({"value": hum}), qos=1)
            client.publish("tani/field1/zoneA/sensor/soil_moisture", json.dumps({"value": soil_a}), qos=1)
            client.publish("tani/field1/zoneB/sensor/soil_moisture", json.dumps({"value": soil_b}), qos=1)

            status = "ON" if soil_b < 28.0 else "OFF"
            client.publish("tani/field1/zoneB/actuator/pump", json.dumps({"status": status}), qos=2)

            print(f"[SIMULASI] Mengirim Telemetri Lahan. Kelembapan Tanah B: {soil_b}% -> Pompa B: {status}")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[PUBLISHER] Penghentian program atas instruksi pengguna.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()