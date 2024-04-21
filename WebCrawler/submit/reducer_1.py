import sys


def reduce_urls(input_stream):
    current_url = None
    current_count = 0
    state = False

    for line in input_stream:
        line = line.strip().split()

        if line[1] in {'0', '1'}:
            if current_url == line[0]:
                state = state or bool(int(line[1]))
            else:
                if current_url:
                    yield current_url, int(state)
                state = bool(int(line[1]))
                current_url = line[0]
        else:
            print(*line)
            current_url = None
            current_count = 0
            state = False
    if current_url:
        yield current_url, int(state)


def process_input(input_stream):
    for url, state in reduce_urls(input_stream):
        print(url, state)


# Call process_input to start processing input from stdin
if __name__ == "__main__":
    process_input(sys.stdin)
