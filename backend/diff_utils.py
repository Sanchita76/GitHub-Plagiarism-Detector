import difflib, os

def get_diffs(user_path, original_path):
    diffs = []
    for root, _, files in os.walk(user_path):
        for file in files:
            if file.endswith(".py"):
                path1 = os.path.join(root, file)
                path2 = path1.replace(user_path, original_path)
                if os.path.exists(path2):
                    with open(path1) as f1, open(path2) as f2:
                        l1 = f1.readlines()
                        l2 = f2.readlines()
                        diff = difflib.unified_diff(l2, l1, fromfile='Original', tofile='Submitted')
                        diffs.append({"file": file, "diff": ''.join(diff)})
    return diffs