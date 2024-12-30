#!/usr/bin/env sh

TAGVAL=0.1.1

git tag $TAGVAL
git push --all

# AMD64
docker buildx build --platform linux/amd64 -t joshburnsxyz/generik:latest .
docker buildx build --platform linux/amd64 -t joshburnsxyz/generik:$TAGVAL .

# ARM64
docker buildx build --platform linux/arm64 -t joshburnsxyz/generik:latest-arm .
docker buildx build --platform linux/arm64 -t joshburnsxyz/generik:$TAGVAL-arm .

# Publish
docker push -a joshburnsxyz/generik