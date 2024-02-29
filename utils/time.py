from datetime import datetime

def get_human_readable_timestamp():
    # Get Unix timestamp
    current_timestamp = datetime.now().timestamp()
    # Convert Unix timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(current_timestamp)

    # Format the datetime object as a human-readable string
    human_readable_time = datetime_obj.strftime("%Y-%m-%d_%H-%M-%S")

    return human_readable_time