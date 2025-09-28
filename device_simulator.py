import asyncio
import random
import aiomqtt
import os
import json

# --- استيراد مكتبات Pandapower و Pandas ---
import pandapower as pp
import pandapower.networks as pn
import pandas as pd # <-- تمت إضافة هذا السطر

# --- إعدادات المحاكاة ---
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
VOLTAGE_DATA_TOPIC = "power/cigre_mv/bus_voltages"

async def run_grid_simulation():
    """
    تقوم هذه الدالة بعمل محاكاة لشبكة CIGRE MV الكهربائية وإرسال البيانات بشكل مستمر.
    """
    client_id = "cigre-mv-grid-simulator"
    print(f"[{client_id}] Starting up...")

    try:
        net = pn.mv_oberrhein()
        print(f"[{client_id}] CIGRE MV (mv_oberrhein) grid model loaded successfully.")
        print(f"[{client_id}] Network contains {len(net.bus)} buses and {len(net.load)} loads.")
    except Exception as e:
        print(f"[{client_id}] Failed to create CIGRE network: {e}")
        return

    try:
        async with aiomqtt.Client(hostname=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, identifier=client_id) as client:
            print(f"[{client_id}] Connected to EMQX Broker at {MQTT_BROKER_HOST}.")
            
            while True:
                load_scaling_factor = round(random.uniform(0.8, 1.2), 2)
                net.load.scaling = load_scaling_factor
                
                pp.runpp(net)

                # ** <<< هذا هو الجزء الذي تم تعديله >>> **
                # دمج أسماء الـ bus من الجدول الأصلي مع نتائج الجهد
                voltages = pd.concat([net.bus['name'], net.res_bus['vm_pu']], axis=1)
                
                payload = voltages.to_json(orient='records')

                print(f"[{client_id}] (Load scaling: {load_scaling_factor * 100}%) Publishing {len(voltages)} bus voltage readings to '{VOLTAGE_DATA_TOPIC}'")
                await client.publish(VOLTAGE_DATA_TOPIC, payload, qos=1)

                sleep_interval = random.uniform(5, 10)
                await asyncio.sleep(sleep_interval)

    except Exception as e:
        print(f"[{client_id}] An error occurred: {e}. Stopping simulation.")


async def main():
    """
    الدالة الرئيسية التي تقوم بتشغيل المحاكاة.
    """
    print("--- Starting CIGRE MV Power Grid Simulation ---")
    await run_grid_simulation()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- Simulation stopped by user ---")
