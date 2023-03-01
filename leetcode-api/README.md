# How to use python-leetcode

```cmd
python3 -m venv /leetcode_venv
```

```cmd
source /leetcode_venv/python/activate
pip3 install python-leetcode
```

```python
# Get the next two values from your browser cookies
leetcode_session = "yyy"
csrf_token = "xxx"
```

1. Open leetcode page in browser, `F12` or right click to inspect elements.
2. Go to Network
3. Refresh page
4. Randomly choose a file, Click `header` sub section.
5. Locate `Cookie` section, copy it, for example mine,

```
Cookie: 87b5a3c3f1a55520_gr_cs1=EXBORN; 87b5a3c3f1a55520_gr_last_sent_cs1=EXBORN; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=ebfa2d81-2730-4f3c-9ebb-b2d614d79b89; 87b5a3c3f1a55520_gr_session_id=ebfa2d81-2730-4f3c-9ebb-b2d614d79b89; 87b5a3c3f1a55520_gr_session_id_ebfa2d81-2730-4f3c-9ebb-b2d614d79b89=true; _ga=GA1.1.1634303155.1675635933; _ga_CDRWKZTDEX=GS1.1.1677707060.333.1.1677714333.0.0.0; _gat=1; _gid=GA1.2.1881355915.1675635933; gr_user_id=3d96b63d-5cce-4fa3-8672-491d3e706cf4; csrftoken=7oAfAKkxhGSWx7GzfGlXxjXCuudpRloqvQLTOz77K4lEYvO79ZFKlwqphAILP6qv; __stripe_mid=b42cb0e7-ada0-4d31-84bc-f17bc67a6ab30a5674; __atuvc=11%7C5%2C3%7C6%2C4%7C7%2C5%7C8%2C5%7C9; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTQ4NTQ4MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZhNjBlMzhlYmY2MTViOWQ2NGIzZWY4MTA3NDQyMTc4YmRlYmYzODgiLCJpZCI6MTQ4NTQ4MiwiZW1haWwiOiI4NTEwMjM1NjFAcXEuY29tIiwidXNlcm5hbWUiOiJFWEJPUk4iLCJ1c2VyX3NsdWciOiJFWEJPUk4iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2NTExMjMwNS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2Nzc1OTY4ODAsImlwIjoiMjYwMDo0MDQxOjQxYzY6YTIwMDo3NDI1OjdjYzQ6MjA2Yjo5OGViIiwiaWRlbnRpdHkiOiI4ZjZhMjM4ZTNhZDM4MmRhYmMyYTU1ZjE0YjBmMTRkYyIsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMCwic2Vzc2lvbl9pZCI6MzQyNjgyMTJ9.2q_YHcbVC-_PiM5R0EhO3Du3tg0bhmJULGNI9_YqZT8; NEW_PROBLEMLIST_PAGE=1; _ga_DKXQ03QCVK=GS1.1.1673476879.1.1.1673476919.20.0.0; _gcl_au=1.1.1446556967.1673476879; intercom-device-id-pq9rak4o=2f9a2434-3550-4083-8298-7ecfc0563bd6; intercom-id-pq9rak4o=f8a189e8-4773-4755-b8a9-7d677e2b1df2
```

Search `leetcode_session` and `csrftoken` in here.