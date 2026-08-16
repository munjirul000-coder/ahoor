#!/usr/bin/env bash
# Regression runner: fresh DB + server restart before each suite
set -u
cd /home/user/ahoor
FAILED=0
run_suite() {
  local name=$1; shift
  pkill -f "node server.js" 2>/dev/null; sleep 1
  rm -f data/db.json
  (ADMIN_EMAIL=admin@ahoor.com nohup node server.js > /tmp/ahoor-server.log 2>&1 &)
  sleep 2
  echo "===== RUNNING $name ====="
  timeout 600 python3 -u "$@" 2>&1 | grep -E "FAIL |ERROR|Traceback|SUMMARY" | tail -8
  if [ ${PIPESTATUS[0]} -ne 0 ]; then echo "!! $name FAILED (timeout/error)"; FAILED=1; else echo "!! $name done"; fi
}
run_suite test_auth test_auth.py
run_suite test_marketplace test_marketplace.py
run_suite test_quotes test_quotes.py
run_suite test_business test_business.py
run_suite test_chat test_chat.py
run_suite test_notifications test_notifications.py
run_suite test_matching test_matching.py
run_suite test_verification test_verification.py
run_suite test_admin test_admin.py
run_suite test_analytics test_analytics.py
pkill -f "node server.js" 2>/dev/null
echo "REGRESSION DONE failed=$FAILED"
