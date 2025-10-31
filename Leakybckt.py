import time
import random

def leaky_bucket(bucket_size, leak_rate, simulation_time):
    storage = 0  # Current bucket content (in KB)

    print("\n--- Real-Time Leaky Bucket Simulation ---")
    print(f"Bucket Size: {bucket_size} KB | Leak Rate: {leak_rate} KB/sec\n")

    for t in range(1, simulation_time + 1):
        # Random incoming data (0 to 10 KB per second)
        incoming = random.randint(0, 10)
        print(f"Time {t}s: Incoming Packet = {incoming} KB")

        # Add incoming data  
        if storage + incoming > bucket_size:
            dropped = (storage + incoming) - bucket_size
            storage = bucket_size
            print(f"  Bucket Overflow! Dropped {dropped} KB")
        else:
            storage += incoming
            print(f"Added to bucket. Current storage = {storage} KB")

        # Leak out at fixed rate   
        if storage == 0:
            print("Bucket is empty, nothing to send.")
        elif storage < leak_rate:
            print(f"Sent out {storage} KB (bucket emptied)")
            storage = 0
        else:
            storage -= leak_rate
            print(f"Sent out {leak_rate} KB | Remaining in bucket: {storage} KB")

        # Visualize bucket fill
        filled = int((storage / bucket_size) * 20)  # 20 = bar length
        bar = "█" * filled + "-" * (20 - filled)
        print(f"[{bar}] {storage}/{bucket_size} KB\n")

        # Wait 1 second before next cycle
        time.sleep(1)

    # After simulation, empty remaining data
    print("\nSimulation complete. Emptying remaining data...")
    while storage > 0:
        if storage < leak_rate:
            print(f"Sent out {storage} KB (final leak)")
            storage = 0
        else:
            storage -= leak_rate
            print(f"Sent out {leak_rate} KB | Remaining: {storage} KB")
        time.sleep(1)

    print("\n✅ Bucket emptied successfully!")

# Example: bucket_size=15KB, leak_rate=3KB/sec, simulate 10 seconds
leaky_bucket(bucket_size=15, leak_rate=3, simulation_time=10)
