#!/usr/bin/env bash
IMAGES_UNTAGGED=$(docker images | grep -i none)
if [ -n "$IMAGES_UNTAGGED" ]; then
  docker rmi -f $(docker images | grep -i none | awk '{print $3}')
fi
