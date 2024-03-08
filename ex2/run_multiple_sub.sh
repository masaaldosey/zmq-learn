#!/usr/bin/env bash

# Function to handle termination
cleanup() {
    echo "Terminating..."
    # Send termination signal to both background processes
    for i in {1..10}
    do
        kill ${exec_pid[$i]} 9>/dev/null
    done
    exit 1
}

# Trap SIGINT signal (Ctrl+C) to call the cleanup function
trap cleanup SIGINT

# Placeholder for the process IDs
exec_pid = {}

# Launch loop to start the background processes
for i in {1..10}
do
    echo "Starting sub$i"
    ./build/sub &
    exec_pid[$i]=$!
done

# Wait for a Ctrl+C signal
echo "Press Ctrl+C to terminate the processes."

# Wait for both background processes to finish
wait
