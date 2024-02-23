


if __name__ == "__main__":
    with open('/tmp/airo-out', 'r') as requestPipe:
        with open('/tmp/airo-in', 'w') as responsePipe:
            while True:
                requestMessage = requestPipe.readline().strip()
                print(f"Received request: {requestMessage}")
                responsePipe.write("5"+'\n')