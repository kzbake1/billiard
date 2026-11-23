#!/bin/sh
# тестовая копия сайта: без integrity, чтобы подставная база (mock) подменяла supabase-js
mkdir -p /home/claude/site_t
sed -e 's# integrity="[^"]*" crossorigin="anonymous"##' -e "s#sc.integrity='[^']*';sc.crossOrigin='anonymous';##g" /home/claude/site/index.html > /home/claude/site_t/index.html
for f in /home/claude/site/*; do b=$(basename $f); [ "$b" = index.html ] || ln -sfn $f /home/claude/site_t/$b; done
