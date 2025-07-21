import os
from inotify_simple import INotify, flags
from datetime import datetime

files_to_monitor = ['/home/karim/.ssh', '/etc/passwd']

inotify = INotify()
watch_flags = flags.MODIFY | flags.DELETE | flags.ATTRIB  # Modify, delete, attribute change

# Map watch descriptor (wd) to its path
wd_path_map = {}

for path in files_to_monitor:
    wd = inotify.add_watch(path, watch_flags)
    wd_path_map[wd] = path

print(f"Starting monitoring at {datetime.now()}")

try:
    while True:
        for event in inotify.read():
            watched_path = wd_path_map.get(event.wd, 'Unknown')
            # event.name might be empty for a file watch, so handle that:
            if event.name:
                full_path = os.path.join(watched_path, event.name)
            else:
                full_path = watched_path

            for flag in flags.from_mask(event.mask):
                if flag == flags.MODIFY:
                    print(f"[{datetime.now()}] File modified: {full_path}")
                elif flag == flags.DELETE:
                    print(f"[{datetime.now()}] File deleted: {full_path}")
                elif flag == flags.ATTRIB:
                    print(f"[{datetime.now()}] File metadata changed (permissions, owner, timestamps): {full_path}")
                else:
                    print(f"[{datetime.now()}] Event {flag} on {full_path}")

except KeyboardInterrupt:
    print("User cancelled monitoring")
