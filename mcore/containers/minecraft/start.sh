#!/bin/bash
cd "$(dirname "$0")"

exec "$JAVA_BIN" \
  -Xms"$JAVA_XMS" \
  -Xmx"$JAVA_XMX" \
  $JAVA_FLAGS \
  -jar "$SERVER_JAR" \
  $SERVER_ARGS
