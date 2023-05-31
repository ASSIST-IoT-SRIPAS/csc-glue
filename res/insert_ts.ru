PREFIX wsc: <https://assist-iot.eu/ontologies/wsc#>

INSERT {
  wsc:graph wsc:modified ?ts .
}
WHERE {
      BIND (NOW() AS ?ts)
}
