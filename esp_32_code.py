'''
it's only for a basic working simulator prototype 
'''


import random
import time

CO2_THRESHOLD = 1000  # ppm
CO_THRESHOLD = 50     # ppm

print("System Started...\n")

while True:
    # Simulated sensor values
    co2 = random.randint(400, 1500)
    co = random.randint(10, 80)

    print(f"CO2: {co2} ppm | CO: {co} ppm")

    if co2 > CO2_THRESHOLD:
        print("⚠️ ALERT: CO2 LEVEL HIGH!")

    if co > CO_THRESHOLD:
        print("🚨 ALERT: CO LEVEL DANGEROUS!")

    print("----------------------------")
    time.sleep(2)
