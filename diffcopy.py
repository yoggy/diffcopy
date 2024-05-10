#!/usr/bin/python3

import sys
import os
import argparse
from pprint import pprint
import hashlib
import shutil

exclude_filenames = []
exclude_exts = []

def is_ignore_file(filename):
    global exclude_filenames, exclude_exts

    if filename in exclude_filenames:
        return True
    
    (_, target_ext) = os.path.splitext(filename)
    target_ext = target_ext[1:]
    for exclude_ext in exclude_exts:
        if target_ext == exclude_ext:
            return True

    return False

def compare_dir(original_dir:str, target_dir:str, destination_dir:str, dry_run_mode:bool) -> None:
    target_names = os.listdir(target_dir)
    original_names = os.listdir(original_dir)

    # 再帰をしないディレクトリ
    ignore_dirs = []

    for target_name in target_names:
        if is_ignore_file(target_name):
            continue

        if target_name in original_names:
            if os.path.isdir(os.path.join(target_dir, target_name)):
                continue

            target_hash = ""
            original_hash = ""
            with open(os.path.join(target_dir, target_name),'rb') as f:
                target_data = f.read()
                target_hash = hashlib.sha256(target_data).hexdigest()
            with open(os.path.join(original_dir, target_name),'rb') as f:
                original_data = f.read()
                original_hash = hashlib.sha256(original_data).hexdigest()

            if original_hash != target_hash:
                print(f"target_dirで変化しているファイル = {target_name}")
                if dry_run_mode == False:
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir)
                    shutil.copy(os.path.join(target_dir, target_name), destination_dir)
        else:
            # target_dirにしかない場合は、丸ごとコピーする
            print(f"target_dirにしかないファイル・ディレクトリ = {target_name}")
            if dry_run_mode == False:
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                if os.path.isdir(os.path.join(target_dir, target_name)):
                    shutil.copytree(os.path.join(target_dir, target_name), os.path.join(destination_dir, target_name), dirs_exist_ok=True)
                else:
                    shutil.copy(os.path.join(target_dir, target_name), destination_dir)

            if os.path.isdir(os.path.join(target_dir, target_name)):
                ignore_dirs.append(target_name)

    # 再帰処理
    for target_name in target_names:
        if is_ignore_file(target_name):
            continue

        # target_dirにしかないディレクトリはパスする
        if target_name in ignore_dirs:
            continue

        if os.path.isdir(os.path.join(target_dir, target_name)):
            compare_dir(os.path.join(original_dir, target_name), os.path.join(target_dir, target_name), os.path.join(destination_dir, target_name), dry_run_mode)


def main():
    global exclude_filenames, exclude_exts

    parser = argparse.ArgumentParser(description="Copy only the files that have changed.")

    parser.add_argument("original_dir", help="Original Directory")
    parser.add_argument("target_dir", help="Target Directory")
    parser.add_argument("destination_dir", help="Destination directory")
    parser.add_argument('-d', '--dry-run', action='store_true', help="dry run mode")  
    parser.add_argument('--exclude-filenames', help="exclude filenames", nargs='+')  
    parser.add_argument('--exclude-exts', help="exclude extentions", nargs='+')  

    args = parser.parse_args()

    exclude_filenames = args.exclude_filenames
    exclude_exts = args.exclude_exts

    print(f"original_dir={args.original_dir}, target_dir={args.target_dir}, destination_dir={args.destination_dir}, exclude_filenames={exclude_filenames}, exclude_exts={exclude_exts}")

    compare_dir(args.original_dir, args.target_dir, args.destination_dir, args.dry_run)

if __name__ == "__main__":
    main()
