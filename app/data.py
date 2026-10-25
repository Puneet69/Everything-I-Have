topics = [
    {"title": "Python basics", "status": "learning"},
    {"title": "FastAPI routes", "status":"done"},
    {"title": "Learning 1", "status":"pending"},
    {"title": "Learning 2", "status":"not yet"},
    {"title": "Learning 3", "status":"done"}
]

def get_topics():
    return topics

def count_done():
    return len([t for t in topics if t["status"]== "done"])
