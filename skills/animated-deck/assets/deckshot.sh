#!/bin/bash
# usage: deckshot.sh <url-of-built-html> <out-dir> <prefix> N:t ...
# N = slide number, t = seconds into it; a "notes" suffix (N:3.5notes) opens the notes panel.
# Serve the built file over http first (snap chromium cannot read /tmp); out-dir must be writable by chromium, e.g. ~/snapshots.
url=$1; out=$2; pre=$3; shift 3
mkdir -p "$out"
sep='?'; [[ $url == *\?* ]] && sep='&'
for st in "$@"; do
  n=${st%%:*}; t=${st#*:}; extra=""
  [[ $t == *notes ]] && { t=${t%notes}; extra="&notes"; }
  timeout 60 chromium --headless --disable-gpu --hide-scrollbars --window-size=1920,1080 --virtual-time-budget=2500 \
    --screenshot="$out/$pre-s$n-t$t${extra:+n}.png" "$url${sep}slide=$n&t=$t$extra" >/dev/null 2>&1
done
ls "$out/$pre"-* | wc -l
