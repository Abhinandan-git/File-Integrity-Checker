import os
import argparse
import hashlib
import json

def compute_hash(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def initialize_hashes(path: str, hash_file='hashes.json') -> None:
    hashes = dict()
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                hashes[file_path] = compute_hash(file_path)
    else:
        hashes[path] = compute_hash(path)
    with open(hash_file, 'w') as f:
        json.dump(hashes, f)
    print("Hashes stored successfully.")

def check_integrity(path, hash_file='hashes.json'):
    with open(hash_file, 'r') as f:
        stored_hashes = json.load(f)
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                current_hash = compute_hash(file_path)
                stored_hash = stored_hashes.get(file_path)
                if stored_hash:
                    if current_hash != stored_hash:
                        print(f"{file_path}: Modified (Hash mismatch)")
                    else:
                        print(f"{file_path}: Unmodified")
                else:
                    print(f"{file_path}: No stored hash found.")
    else:
        current_hash = compute_hash(path)
        stored_hash = stored_hashes.get(path)
        if stored_hash:
            if current_hash != stored_hash:
                print(f"{path}: Modified (Hash mismatch)")
            else:
                print(f"{path}: Unmodified")
        else:
            print(f"{path}: No stored hash found.")

def update_hash(path, hash_file='hashes.json'):
    with open(hash_file, 'r') as f:
        stored_hashes = json.load(f)
    stored_hashes[path] = compute_hash(path)
    with open(hash_file, 'w') as f:
        json.dump(stored_hashes, f)
    print("Hash updated successfully.")

def main():
    parser = argparse.ArgumentParser(description='File Integrity Checker')
    parser.add_argument('command', choices=['init', 'check', 'update'], help='Command to execute')
    parser.add_argument('path', help='Path to file or directory')
    args = parser.parse_args()

    if args.command == 'init':
        initialize_hashes(args.path)
    elif args.command == 'check':
        check_integrity(args.path)
    elif args.command == 'update':
        update_hash(args.path)

if __name__ == "__main__":
    main()
