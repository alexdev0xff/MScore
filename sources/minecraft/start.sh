#!/bin/bash
cd "$(dirname "$0")"

JAVA=java
XMS=1024M
XMX=4096M
JAR=server/server.jar

exec $JAVA -Xms$XMS -Xmx$XMX -jar $JAR nogui
