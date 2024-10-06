#!/usr/bin/env python3

import os
import hashlib

def get_file_paths(directory):
    """
    Recursively collects the paths of all files within a given directory.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if 'recoverfile19' in root and 'logseq' in file:
                continue
            file_paths.append(file_path)
    return file_paths



def calculate_sha256(file_path):
    """
    Calculates the SHA-256 hash of a file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def remove_duplicate_hashes(file_hashes):
    """
    Removes duplicate hashes from the list of file paths and their hashes.
    """
    unique_files = {}
    for file_path, file_hash in file_hashes:
        if file_hash not in unique_files:
            unique_files[file_hash] = file_path
    return unique_files

def main(directory):
    # Get all file paths from the directory
    file_paths = get_file_paths(directory)
    
    # List to store (file_path, sha256_hash) tuples
    file_hashes = []
    
    # Compute the SHA-256 hash for each file
    for file_path in file_paths:
        file_hash = calculate_sha256(file_path)
        file_hashes.append((file_path, file_hash))
    
    # Remove duplicate hashes
    unique_files = remove_duplicate_hashes(file_hashes)
    
    # Print unique files with their SHA-256 hash
    print("Unique files and their SHA-256 hashes:")
    for file_hash, file_path in unique_files.items():
        #print(f"File: {file_path} | Hash: {file_hash}")
        print(file_hash)


if __name__ == "__main__":
    # Replace 'your_directory_path_here' with the directory you want to scan
    directory = '/home/kali/Desktop/NSACODE/ZFS'
    main(directory)
