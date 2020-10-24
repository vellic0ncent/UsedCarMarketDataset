def no_throw(f, default):
    try:
        return f()
    except Exception:
        return default