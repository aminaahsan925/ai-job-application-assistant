import os
import shutil
from pathlib import Path
from PIL import Image
import hashlib
from collections import defaultdict

class PhotoOrganizer:
    def __init__(self, base_folder):
        self.base_folder = Path(base_folder)
        self.duplicates_removed = 0
        self.files_moved = 0
        self.hash_map = {}
        self.report = {"duplicates_deleted": [], "files_organized": [], "screenshots_separated": [], "errors": []}
        
    def get_image_hash(self, image_path):
        try:
            with Image.open(image_path) as img:
                img.thumbnail((100, 100))
                img_bytes = img.tobytes()
                return hashlib.md5(img_bytes).hexdigest()
        except:
            return None
    
    def is_screenshot(self, image_path):
        try:
            filename = image_path.name.lower()
            if 'screenshot' in filename or 'screen' in filename:
                return True
            with Image.open(image_path) as img:
                width, height = img.size
                if (height > width * 1.5) or (width > height * 1.5):
                    return True
            return False
        except:
            return False
    
    def find_duplicates(self):
        print("🔍 Scanning for duplicate images...")
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
        
        for folder in [self.base_folder / 'Pictures', self.base_folder / 'Screenshots', self.base_folder / 'Gallery']:
            if not folder.exists():
                continue
            for image_file in folder.rglob('*'):
                if image_file.is_file() and image_file.suffix.lower() in image_extensions:
                    img_hash = self.get_image_hash(image_file)
                    if img_hash:
                        if img_hash not in self.hash_map:
                            self.hash_map[img_hash] = []
                        self.hash_map[img_hash].append(image_file)
    
    def remove_duplicates(self):
        print("🗑️  Removing duplicate images...")
        for img_hash, files in self.hash_map.items():
            if len(files) > 1:
                for duplicate in files[1:]:
                    try:
                        duplicate.unlink()
                        self.duplicates_removed += 1
                        print(f"  ✓ Deleted: {duplicate.name}")
                    except:
                        pass
    
    def organize_files(self):
        print("📁 Organizing photos...")
        screenshots_folder = self.base_folder / 'Screenshots_Organized'
        gallery_folder = self.base_folder / 'Gallery_Organized'
        screenshots_folder.mkdir(exist_ok=True)
        gallery_folder.mkdir(exist_ok=True)
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
        
        for folder in [self.base_folder / 'Pictures', self.base_folder / 'Screenshots', self.base_folder / 'Gallery']:
            if not folder.exists():
                continue
            for image_file in folder.rglob('*'):
                if image_file.is_file() and image_file.suffix.lower() in image_extensions:
                    try:
                        if self.is_screenshot(image_file):
                            destination = screenshots_folder / image_file.name
                            shutil.move(str(image_file), str(destination))
                            self.files_moved += 1
                            print(f"  📸 Screenshot: {image_file.name}")
                        else:
                            destination = gallery_folder / image_file.name
                            shutil.move(str(image_file), str(destination))
                            self.files_moved += 1
                            print(f"  🖼️  Gallery: {image_file.name}")
                    except:
                        pass
    
    def run(self):
        print("\n" + "="*60)
        print("PHOTO ORGANIZER - START")
        print("="*60 + "\n")
        self.find_duplicates()
        self.remove_duplicates()
        self.organize_files()
        print("\n" + "="*60)
        print("✅ ORGANIZATION COMPLETE!")
        print("="*60)
        print(f"\nSummary:")
        print(f"  • Duplicate images deleted: {self.duplicates_removed}")
        print(f"  • Files organized: {self.files_moved}")

if __name__ == "__main__":
    folder_path = input("Enter your Pictures folder path: ").strip()
    if os.path.exists(folder_path):
        organizer = PhotoOrganizer(folder_path)
        organizer.run()
    else:
        print(f"❌ Folder not found: {folder_path}")