import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

BROKER_HOST = "localhost"
BROKER_PORT = 1883
USERNAME = "user_tani"
PASSWORD = "kata_kunci_tani"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[SUBSCRIBER] Terhubung ke broker sukses. Mengaktifkan subskripsi...")
        # Skenario 1: Langganan Topik Spesifik Tunggal (Tanpa Wildcard)
        client.subscribe("tani/field1/zoneA/sensor/temperature", qos=0)
        
        # Skenario 4: Penggunaan Single-Level Wildcard (+)
        client.subscribe("tani/field1/+/sensor/soil_moisture", qos=0)
        
        # Skenario 5: Penggunaan Multi-Level Wildcard (#)
        client.subscribe("tani/field1/zoneA/#", qos=0)
        print("[SUBSCRIBER] Seluruh topik pengujian berhasil didaftarkan ke broker.")
    else:
        print(f"[SUBSCRIBER] Koneksi gagal dengan kode alasan: {reason_code}")

def on_message(client, userdata, message):
    try:
        topic = message.topic
        payload = message.payload.decode("utf-8")
        qos = message.qos
        
        print("\n" + "="*70)
        print(f" ALIRAN DATA DITERIMA")
        print(f"Topik Penerima: {topic}")
        print(f"Isi Paket Data: {payload}")
        print(f"Tingkat QoS   : {qos}")
        
        # Identifikasi Skenario Berdasarkan Struktur Topik Masuk
        if "soil_moisture" in topic:
            print("--> COCOK: Skenario 4 (Wildcard '+' Kelembapan Tanah Lintas Zona)")
        elif "zoneA" in topic:
            print("--> COCOK: Skenario 5 (Wildcard '#' Aktivitas Menyeluruh di Zona A)")
        else:
            print("--> COCOK: Skenario 1 (Topik Spesifik Tunggal Tanpa Wildcard)")
        print("="*70)
    except Exception as e:
        print(f"[ERROR] Kesalahan pemrosesan payload masuk: {str(e)}")

def on_subscribe(client, userdata, mid, reason_codes, properties):
    print(f"[SUBSCRIBER] Pendaftaran subskripsi diakui broker. ID Transaksi: {mid}")

def main():
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="CentralAgri Monitor")
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    print(f"Menghubungkan ke broker Mosquitto di {BROKER_HOST}:{BROKER_PORT}...")
    client.connect(BROKER_HOST, BROKER_PORT, 60)

    try:
        print("Menjalankan loop penerimaan pesan aktif...")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[SUBSCRIBER] Layanan pemantauan dinonaktifkan.")

if __name__ == "__main__":
    main()