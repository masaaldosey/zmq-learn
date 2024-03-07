#!/usr/bin/env bash

# Function to handle termination
cleanup() {
    echo "Terminating..."
    # Send termination signal to both background processes
    kill $exec1_pid $exec2_pid $exec3_pid $exec4_pid $exec5_pid $exec6_pid 6>/dev/null
    # kill $exec1_pid $exec2_pid $exec3_pid $exec4_pid $exec5_pid $exec6_pid $exec7_pid 7>/dev/null
    exit 1
}

# Trap SIGINT signal (Ctrl+C) to call the cleanup function
trap cleanup SIGINT


echo "Starting sub1"
./build/sub &
exec1_pid=$!

echo "Starting sub2"
./build/sub &
exec2_pid=$!

echo "Starting sub3"
./build/sub &
exec3_pid=$!

echo "Starting sub4"
./build/sub &
exec4_pid=$!

echo "Starting sub5"
./build/sub &
exec5_pid=$!


echo "Starting sub6"
./build/sub &
exec6_pid=$!


# echo "Starting sub7"
# ./build/sub &
# exec7_pid=$!

# Wait for a Ctrl+C signal
echo "Press Ctrl+C to terminate the processes."

# Wait for both background processes to finish
wait
