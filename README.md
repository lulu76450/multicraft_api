# MultiListe
**An API that allows you to obtain a list of MultiCraft game servers**



## Sinon

faites 
`curl -s \
  -H "Host: menu2.multicraft.network" \
  -H "User-Agent: MultiCraft/2.0.14 Android [Linux/5.15.180-android13-3-32001549 aarch64]" \
  -H "Accept: */*" \
  -H "Accept-Language: fr" \
  -H "Content-Type: application/json" \
  -d '{"proto_version_min":37,"proto_version_max":39,"platform":"Android"}' \
  -o servers.json \
  "https://menu2.multicraft.network/v1/find-nearby-servers"`

dans le terminal, puis accédez au fichier `servers.json`
