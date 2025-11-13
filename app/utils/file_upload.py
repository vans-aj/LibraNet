"""
Image Upload Utility for LibraNet
Handles file upload, validation, compression, and storage
"""

import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime


class ImageUploader:
    """Handle image upload operations"""
    
    # Allowed image extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    
    # Image size constraints
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    THUMBNAIL_SIZE = (300, 300)
    LARGE_SIZE = (1200, 1200)
    
    def __init__(self, upload_folder=None):
        """
        Initialize uploader
        
        Args:
            upload_folder: Custom upload folder path, defaults to config value
        """
        self.upload_folder = upload_folder or current_app.config.get('UPLOAD_FOLDER')
        self._ensure_upload_folders()
    
    def _ensure_upload_folders(self):
        """Create upload directories if they don't exist"""
        folders = [
            self.upload_folder,
            os.path.join(self.upload_folder, 'books'),
            os.path.join(self.upload_folder, 'books', 'thumbnails'),
            os.path.join(self.upload_folder, 'books', 'large'),
            os.path.join(self.upload_folder, 'books', 'original'),
        ]
        
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
    
    def allowed_file(self, filename):
        """
        Check if file has allowed extension
        
        Args:
            filename: Name of the file
            
        Returns:
            bool: True if extension is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def generate_unique_filename(self, original_filename):
        """
        Generate unique filename while preserving extension
        
        Args:
            original_filename: Original uploaded filename
            
        Returns:
            str: Unique filename
        """
        # Get file extension
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
        
        # Generate unique name with timestamp and random string
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = secrets.token_hex(8)
        unique_name = f"{timestamp}_{random_str}.{ext}"
        
        return secure_filename(unique_name)
    
    def compress_image(self, image_path, output_path, max_size=(800, 800), quality=85):
        """
        Compress and resize image
        
        Args:
            image_path: Path to source image
            output_path: Path to save compressed image
            max_size: Maximum dimensions (width, height)
            quality: JPEG quality (1-100)
        """
        try:
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize maintaining aspect ratio
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save with optimization
                img.save(output_path, optimize=True, quality=quality)
                
        except Exception as e:
            raise Exception(f"Error compressing image: {str(e)}")
    
    def create_thumbnail(self, image_path, thumbnail_path):
        """
        Create thumbnail version of image
        
        Args:
            image_path: Path to source image
            thumbnail_path: Path to save thumbnail
        """
        self.compress_image(image_path, thumbnail_path, 
                          max_size=self.THUMBNAIL_SIZE, quality=80)
    
    def upload_image(self, file, subfolder='books'):
        """
        Upload and process image file
        
        Args:
            file: FileStorage object from request.files
            subfolder: Subfolder within upload directory
            
        Returns:
            dict: Paths to saved images
            {
                'original': 'path/to/original.jpg',
                'large': 'path/to/large.jpg',
                'thumbnail': 'path/to/thumbnail.jpg',
                'filename': 'unique_filename.jpg'
            }
        """
        # Validate file
        if not file or file.filename == '':
            raise ValueError("No file provided")
        
        if not self.allowed_file(file.filename):
            raise ValueError(f"File type not allowed. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}")
        
        # Generate unique filename
        filename = self.generate_unique_filename(file.filename)
        
        # Define paths
        original_path = os.path.join(self.upload_folder, subfolder, 'original', filename)
        large_path = os.path.join(self.upload_folder, subfolder, 'large', filename)
        thumbnail_path = os.path.join(self.upload_folder, subfolder, 'thumbnails', filename)
        
        # Save original
        file.save(original_path)
        
        # Create processed versions
        try:
            # Create large version (for detail view)
            self.compress_image(original_path, large_path, 
                              max_size=self.LARGE_SIZE, quality=90)
            
            # Create thumbnail (for listings)
            self.create_thumbnail(original_path, thumbnail_path)
            
            # Return relative paths (for database storage)
            return {
                'original': os.path.join('uploads', subfolder, 'original', filename),
                'large': os.path.join('uploads', subfolder, 'large', filename),
                'thumbnail': os.path.join('uploads', subfolder, 'thumbnails', filename),
                'filename': filename
            }
            
        except Exception as e:
            # Clean up on error
            self._cleanup_files([original_path, large_path, thumbnail_path])
            raise Exception(f"Error processing image: {str(e)}")
    
    def upload_multiple_images(self, files, subfolder='books', max_images=5):
        """
        Upload multiple image files
        
        Args:
            files: List of FileStorage objects
            subfolder: Subfolder within upload directory
            max_images: Maximum number of images allowed
            
        Returns:
            list: List of image path dictionaries
        """
        if len(files) > max_images:
            raise ValueError(f"Maximum {max_images} images allowed")
        
        uploaded_images = []
        
        for file in files:
            try:
                result = self.upload_image(file, subfolder)
                uploaded_images.append(result)
            except Exception as e:
                # If one fails, clean up already uploaded images
                self._cleanup_uploaded_images(uploaded_images)
                raise Exception(f"Failed to upload image: {str(e)}")
        
        return uploaded_images
    
    def delete_image(self, image_paths):
        """
        Delete image files
        
        Args:
            image_paths: Dictionary with 'original', 'large', 'thumbnail' paths
        """
        for key in ['original', 'large', 'thumbnail']:
            if key in image_paths:
                file_path = os.path.join(current_app.static_folder, image_paths[key])
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")
    
    def _cleanup_files(self, file_paths):
        """Clean up files on error"""
        for path in file_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
    
    def _cleanup_uploaded_images(self, uploaded_images):
        """Clean up previously uploaded images on batch upload failure"""
        for img_dict in uploaded_images:
            self.delete_image(img_dict)
    
    def validate_file_size(self, file):
        """
        Validate file size
        
        Args:
            file: FileStorage object
            
        Returns:
            bool: True if valid
        """
        # Seek to end to get size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)  # Reset position
        
        if size > self.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {self.MAX_FILE_SIZE / (1024*1024):.1f}MB")
        
        return True


def allowed_file(filename):
    """
    Standalone function to check if file extension is allowed
    
    Args:
        filename: Name of the file
        
    Returns:
        bool: True if extension is allowed
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
