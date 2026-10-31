import json
import os
import tempfile
from typing import SupportsIndex


class ReactiveTaskList(list):
    """
    Reactive persistent list: Automatically writes to a JSON file on any change, and reads on initialization.
    """

    def __init__(self, filename="tasks_data.json"):
        super().__init__()
        self.filename = filename
        self.load()

    def on_change(self):
        """Trigger save on any change event."""
        self.save()

    def load(self):
        """Load from file on startup, catching only specific exceptions."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Ensure the loaded data is a list
                if isinstance(data, list):
                    self.extend(data)
                else:
                    print(
                        f"[Persistence] Warning: Data in {self.filename} is not in list format."
                    )
            except json.JSONDecodeError:
                print(
                    f"[Persistence] Error: {self.filename} is corrupted and cannot be parsed as JSON."
                )
            except OSError as e:
                print(f"[Persistence] File read error (I/O): {e}")

    def save(self):
        """Atomically save task data to a JSON file."""
        target_path = os.path.abspath(self.filename)
        target_dir = os.path.dirname(target_path)
        temp_path = None

        try:
            # 1. Create a temporary file in the same directory
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=target_dir,
                prefix=f".{os.path.basename(target_path)}.",
                suffix=".tmp",
                delete=False,
            ) as f:
                temp_path = f.name

                # 2. Write the complete JSON document
                json.dump(self, f, ensure_ascii=False, indent=4)
                f.write("\n")

                # 3. Flush Python buffers and request OS-level sync
                f.flush()
                os.fsync(f.fileno())

            # 4. Atomically replace the original file
            os.replace(temp_path, target_path)
            temp_path = None

            print("[Persistence] Data auto-saved.")

        except (TypeError, ValueError) as e:
            print(f"[Persistence] JSON serialization failed: {e}")

        except OSError as e:
            print(f"[Persistence] File write error (I/O): {e}")

        finally:
            # 5. Clean up the temporary file if anything failed
            if temp_path is not None:
                try:
                    os.unlink(temp_path)
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"[Persistence] Temporary file cleanup failed: {e}")

    # Override methods that modify the list to trigger saving
    def append(self, item):
        super().append(item)
        self.on_change()

    def extend(self, iterable):
        super().extend(iterable)
        self.on_change()

    def insert(self, index, item):
        super().insert(index, item)
        self.on_change()

    def remove(self, item):
        super().remove(item)
        self.on_change()

    def pop(
        self, index: SupportsIndex = -1
    ):  # Fixed the previous SupportsIndex type warning
        item = super().pop(index)
        self.on_change()
        return item

    def clear(self):
        super().clear()
        self.on_change()

    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)
        self.on_change()

    def reverse(self):
        super().reverse()
        self.on_change()

    def __setitem__(self, index, item):
        super().__setitem__(index, item)
        self.on_change()

    def __delitem__(self, index):
        super().__delitem__(index)
        self.on_change()

    def __iadd__(self, other):
        result = super().__iadd__(other)
        self.on_change()
        return result

    def __imul__(self, other):
        result = super().__imul__(other)
        self.on_change()
        return result
