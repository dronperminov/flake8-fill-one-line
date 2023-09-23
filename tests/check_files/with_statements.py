import tempfile


with open("another.txt", "w", encoding="utf-8"):
    pass

with open("some_file.txt") as \
        f:
    f.read()

with open("f1.txt") as f1, \
        open("f2.txt", "w") as f2:
    f2.write(f1.read())


def func():
    with tempfile.TemporaryDirectory() as \
            tmpdir:
        file_path = save_upload_file(file, tmpdir)
