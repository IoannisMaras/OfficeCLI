#!/bin/bash
set -e

cp -r /src /app && cd /app

echo "Building Linux binaries (Standard JIT & ReadyToRun AOT)..."
dotnet publish src/officecli/officecli.csproj -c Release -r linux-x64 -o /app/bin-jit --nologo >/dev/null
dotnet publish src/officecli/officecli.csproj -c Release -r linux-x64 -o /app/bin-r2r /p:PublishReadyToRun=true /p:EnableCompressionInSingleFile=false --nologo >/dev/null

echo "Installing Python3..."
apt-get update -qq && apt-get install -y -qq python3 >/dev/null

python3 /app/benchmarks/benchmark.py
