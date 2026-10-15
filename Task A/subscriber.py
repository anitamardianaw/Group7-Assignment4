import sys
import zmq

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    my_topic = sys.argv[1]

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    socket.connect("tcp://localhost:9991")
    
    socket.setsockopt_string(zmq.SUBSCRIBE, my_topic)
    
    while True:
        string = socket.recv_string()
        topic, message = string.split(" ", 1)
        print(f"Received -> Topic: {topic} | Message: {message}")

if __name__ == "__main__":
    main()