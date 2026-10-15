import time
import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:9991")
    print("Publisher is bound to port 9991. Waiting for subscribers...")
    time.sleep(2)

    # My members data
    members = [
        {"id": "103012340448", "name": "Amalina", "game": "Cooking Mama"},
        {"id": "103012440018", "name": "Axella", "game": "Roblox"},
        {"id": "103012440020", "name": "Rayhan", "game": "Mobile Legends"},
        {"id": "103012440022", "name": "Anita", "game": "Baby Hazel"}
    ]

    while True:
        for member in members:
            topic = member["id"]
            name = member["name"]
            game = member["game"]
            
            message = f"Hey, I got a new message for {name} - It is from {game}"
            
            socket.send_string(f"{topic} {message}")
            print(f"Published -> Topic [{topic}]: {message}")
            
        time.sleep(3)

if __name__ == "__main__":
    main()
