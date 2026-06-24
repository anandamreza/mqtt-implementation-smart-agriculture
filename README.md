# Smart Agriculture Monitoring System - MQTT Python

Aplikasi sistem komunikasi IoT menggunakan arsitektur publish-subscribe MQTT untuk memantau kondisi microclimate pertanian lokal.

## Persyaratan Awal
1. Python 3.8+
2. Eclipse Mosquitto Broker v2.0+
3. Pustaka Paho-MQTT v2.0+ (`pip install "paho-mqtt>=2.0.0"`)

## Cara Menjalankan Program
1. Pastikan Mosquitto Broker telah berjalan dengan otentikasi aktif menggunakan port default `1883`.
2. Jalankan pusat pemantauan (Subscriber):
   ```bash
   python subscriber.py
3. Jalankan node simulasi lapangan (Publisher) di terminal terpisah:
   ```bash
   python publisher.py
