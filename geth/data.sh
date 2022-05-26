#!/bin/bash

geth  --allow-insecure-unlock --http --http.addr %Node_Address% --http.port %Port_Address% --identity node1 --networkid %NetworkId% --datadir data --nodiscover --port 30303 --ipcpath data/geth.ipc --verbosity 5 console 2> console.log

