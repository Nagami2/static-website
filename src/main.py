import os
import shutil

from generate_page import generate_page, generate_pages_recursive


def main():
    # define source and destination paths
    source_path = "static"
    destination_path = "public"

    print(f"Preparing to copy from '{source_path}' to '{destination_path}'...")

    def copy_directory_recursively(src, dst):
        # create the destination directory if it doesn't exist
        if not os.path.exists(dst):
            os.makedirs(dst)
            print(f"Created directory '{dst}'.")

        # iterate over all items in the source directory
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            
            if os.path.isdir(s):
                # recursively copy subdirectory
                copy_directory_recursively(s, d)
            else:
                # copy file
                shutil.copy2(s, d)
                print(f"Copied file '{s}' to '{d}'.")
    
    # 1. delete the destination directory if it exists
    if os.path.exists(destination_path):
        print(f"Deleting existing directory '{destination_path}'...")
        shutil.rmtree(destination_path) # recursive delete
        print(f"Deleted '{destination_path}'.")

    # 2. call the recursive copy function
    print(f"Copying contents from '{source_path}' to '{destination_path}'...")
    copy_directory_recursively(source_path, destination_path)
    print("Copy operation completed.")

    # # call the new generate_page function
    # generate_page(
    #     from_path="content/index.md",
    #     template_path="template.html",
    #     dest_path="public/index.html"
    # )
    # --- Step 2: Generate content recursively ---
    print("Generating pages from content...")
    content_dir = "content"
    template_path = "template.html"
    dest_dir = "public"
    
    generate_pages_recursive(content_dir, template_path, dest_dir)
    
    print("Static site generation complete!")
    
if __name__ == "__main__":
    main()