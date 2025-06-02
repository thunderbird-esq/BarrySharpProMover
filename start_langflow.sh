# start_langflow.sh  (chmod +x)
#!/usr/bin/env bash
ulimit -n 8192                          # raise soft limit for this shell *and* children
exec langflow run \
     --host 127.0.0.1 --port 7860 \

