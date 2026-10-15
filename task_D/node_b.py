import time
import RNS

APP_NAME = "task_d"
ASPECT = "announcement"

class AnnouncementHandler:
    def received_announce(self, destination_hash, announced_identity, app_data):
        print("\n=== ANNOUNCEMENT RECEIVED ===")
        print("Destination:", RNS.prettyhexrep(destination_hash))

        if app_data:
            message = app_data.decode("utf-8")
            print("Message from Node A:", message)

        print("=============================\n")

def main():
    reticulum = RNS.Reticulum()

    handler = AnnouncementHandler()
    handler.aspect_filter = f"{APP_NAME}.{ASPECT}"
    RNS.Transport.register_announce_handler(handler)

    print("Node B ready.")
    print("Waiting for announcement from Node A...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nNode B stopped.")

if __name__ == "__main__":
    main()