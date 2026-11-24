# Тесты kazbilliard (перед каждым выпуском)
1. `sh tests/mkcopy.sh` — тестовая копия сайта (подставная база вместо Supabase).
2. `node tests/t2.js` — логика сеток (должно быть «fails 0» дважды).
3. `node tests/merge_done.js; node tests/edge.js` — завершённый матч не затирается старой вкладкой.
4. `python3 tests/console_errors.py` — 0 ошибок на странице.
5. `python3 tests/stale_response.py` — старый ответ сервера не перекрывает новый (ожидается «NEW NEW NEWER»).
6. `python3 tests/xss.py` — подстановка вредного кода во все поля: hits 0, jslinks 0.
- python3 tests/fora.py — фора в шарах во встрече (ожидается «fora ok» и [])
- python3 tests/guest.py — столы «гостям» (ожидается «guest ok» и [])
