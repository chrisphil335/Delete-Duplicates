
def track_duration(duration_milliseconds):
    duration = ""
    seconds = (duration_milliseconds // 1000) % 60
    minutes = (duration_milliseconds // (1000 * 60)) % 60
    hours = (duration_milliseconds // (1000 * 60 * 60)) % 24
    if hours:
        duration += f"{hours}:{minutes:02}:"
    else:
        duration += f"{minutes}:"
    duration += f"{seconds:02}"
    return duration


def playlist_duration():
    pass
