curl --data-binary '{"jsonrpc":"2.0","id":"curltext","method":"branch","params":["TATGGAGGACTTGGGCATATTTGGCCAATGTAACACATTTTTATGGTGATTGTTTTCTAG"]}' -H 'content-type:text/json;' http://127.0.0.1:7000
curl --data-binary '{"jsonrpc":"2.0","id":"introns","method":"introns","params":["STAT1"]}' -H 'content-type:text/json;' http://127.0.0.1:7000
