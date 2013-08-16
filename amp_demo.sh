DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR > /dev/null
# Spawn server
python dig-amp.py unix:/tmp/foo &

# Wait a second before spawning clients
sleep 1

# Spawn client 1
python launchampclient.py unix:/tmp/foo &

# Spawn client 2
python launchampclient.py unix:/tmp/foo &

wait
popd > /dev/null