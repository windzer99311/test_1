#!/bin/bash
set -e

echo "Installing FFmpeg..."

mkdir -p api/bin
cd api/bin

curl -sL https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz

tar -xf ffmpeg.tar.xz
cp ffmpeg-*-amd64-static/ffmpeg ./ffmpeg
chmod +x ffmpeg

rm -rf ffmpeg-*-amd64-static ffmpeg.tar.xz

echo "FFmpeg installed"
