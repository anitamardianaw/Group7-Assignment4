import time
import RNS

APP_NAME = "task_d"
ASPECT = "announcement"

def main():
    reticulum = RNS.Reticulum()

    identity = RNS.Identity()

    destination = RNS.Destination(
        identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        APP_NAME,
        ASPECT
    )

    message = "Hello from Node A!"

    print("Node A ready.")
    print("Destination:", RNS.prettyhexrep(destination.hash))
    print("Message:", message)

    input("\nPress ENTER to send announcement...")

    destination.announce(app_data=message.encode("utf-8"))

    print("Announcement sent.")

    time.sleep(3)

if __name__ == "__main__":
    main()
