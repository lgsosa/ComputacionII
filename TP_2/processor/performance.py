def analyze_performance(html, load_time, num_req):
    size_kb = round(len(html.encode("utf-8")) / 1024, 2)
    return {
        "load_time_ms": int(load_time),
        "total_size_kb": size_kb,
        "num_requests": num_req
    }
