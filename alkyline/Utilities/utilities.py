import datetime

def get_date(date, show=False):
    now = datetime.datetime.now()
    time_delta = now - date
    how_long_ago = ""
    if show:
        months = time_delta.days // 30
        years = months // 12
        if time_delta.days:
            how_long_ago = f"{time_delta.days} days ago"
        if time_delta.days > 30:
            how_long_ago = f"{months} months ago"
        if months > 12:
            how_long_ago = f"{years} years, {months - years*12} months ago"
        how_long_ago = f"({how_long_ago})"
    return date.strftime(f"%a %b %d %Y %H:%M:%M {how_long_ago}")


def try_except(*args):
    returning = []
    for arg in args:
        try:
            returning.append(eval(arg))
        except Exception:
            pass
    if len(returning) == 1:
        returning = "".join(returning)
    return returning
