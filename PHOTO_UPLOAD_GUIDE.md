# Photo Upload System - Quick Start Guide

## ✅ What's Been Implemented

### 1. **Image Upload Utility** (`app/utils/file_upload.py`)
Complete image processing system with:
- ✅ File validation (type, size)
- ✅ Automatic compression
- ✅ Multiple size generation (original, large, thumbnail)
- ✅ Unique filename generation
- ✅ Single & multiple image upload
- ✅ Image deletion
- ✅ Error handling

### 2. **Configuration** (`config.py`)
- Upload folder path
- Max file size (16MB)
- Allowed extensions

### 3. **Test Routes** (`app/routes/upload_routes.py`)
API endpoints for testing:
- `/test-upload` - Test page
- `/upload-image` - Single upload
- `/upload-multiple-images` - Multiple upload
- `/delete-image` - Delete images

### 4. **Test UI** (`app/templates/test_upload.html`)
Beautiful drag-and-drop interface with:
- Single image upload
- Multiple image upload (up to 5)
- Live preview
- Progress indicators
- Error messages

---

## 🚀 How to Test

### Step 1: Start the server
```bash
python main.py
```

### Step 2: Login to your account
Navigate to: `http://localhost:8080/login`

### Step 3: Go to test page
Navigate to: `http://localhost:8080/test-upload`

### Step 4: Try uploading images!
- **Single Upload**: Drag & drop or click to select one image
- **Multiple Upload**: Select up to 5 images at once

---

## 📁 Generated Files

When you upload an image, 3 versions are created:

1. **Original** - Untouched uploaded file
   - Path: `app/static/uploads/books/original/`
   - Use: Backup, future reprocessing

2. **Large** (1200×1200 max)
   - Path: `app/static/uploads/books/large/`
   - Use: Book detail pages, zoom view
   - Quality: 90%

3. **Thumbnail** (300×300 max)
   - Path: `app/static/uploads/books/thumbnails/`
   - Use: List views, cards, previews
   - Quality: 80%

**All images maintain aspect ratio!**

---

## 🔧 How to Use in Your Code

### Example 1: Single Image Upload

```python
from app.utils.file_upload import ImageUploader

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    
    uploader = ImageUploader()
    result = uploader.upload_image(file, subfolder='books')
    
    # result contains:
    # {
    #     'original': 'uploads/books/original/20241111_143022_abc123.jpg',
    #     'large': 'uploads/books/large/20241111_143022_abc123.jpg',
    #     'thumbnail': 'uploads/books/thumbnails/20241111_143022_abc123.jpg',
    #     'filename': '20241111_143022_abc123.jpg'
    # }
    
    # Save to database
    book.image_path = result['large']
    book.thumbnail_path = result['thumbnail']
```

### Example 2: Multiple Images Upload

```python
from app.utils.file_upload import ImageUploader

@app.route('/upload-multiple', methods=['POST'])
def upload_multiple():
    files = request.files.getlist('images')
    
    uploader = ImageUploader()
    results = uploader.upload_multiple_images(files, max_images=5)
    
    # results is a list of image path dicts
    # Save each to database
    for img_data in results:
        image = BookImage(
            book_id=book.id,
            image_path=img_data['large'],
            thumbnail_path=img_data['thumbnail']
        )
        db.session.add(image)
```

### Example 3: Delete Image

```python
from app.utils.file_upload import ImageUploader

uploader = ImageUploader()
uploader.delete_image({
    'original': 'uploads/books/original/image.jpg',
    'large': 'uploads/books/large/image.jpg',
    'thumbnail': 'uploads/books/thumbnails/image.jpg'
})
```

---

## 🎨 Frontend Usage

### HTML Form

```html
<form id="uploadForm">
    <!-- Single file -->
    <input type="file" name="image" accept="image/*">
    
    <!-- Multiple files -->
    <input type="file" name="images" accept="image/*" multiple>
    
    <button type="submit">Upload</button>
</form>
```

### JavaScript Upload

```javascript
async function uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await fetch('/upload-image', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (response.ok) {
        console.log('Upload successful:', result.data);
        // Display image: /static/${result.data.thumbnail}
    } else {
        console.error('Upload failed:', result.error);
    }
}
```

---

## 📊 File Size Optimization

### Before Upload
- User uploads 5MB photo

### After Processing
- Original: 5MB (preserved)
- Large: ~500KB (compressed, max 1200px)
- Thumbnail: ~50KB (compressed, max 300px)

**Total savings: ~90% for display images!**

---

## 🔒 Security Features

1. **File Type Validation**
   - Only allows: PNG, JPG, JPEG, WEBP, GIF
   - Checks file extension

2. **File Size Limits**
   - Per file: 5MB
   - Request: 16MB total

3. **Unique Filenames**
   - Timestamp + random token
   - Prevents overwrites
   - Prevents guessing

4. **Secure Paths**
   - Uses `secure_filename()`
   - Prevents directory traversal

---

## 🛠️ Configuration Options

Edit `config.py` to customize:

```python
# Upload folder
UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

# Max request size
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
```

Edit `app/utils/file_upload.py` for advanced options:

```python
class ImageUploader:
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB per file
    THUMBNAIL_SIZE = (300, 300)      # Thumbnail dimensions
    LARGE_SIZE = (1200, 1200)        # Large image dimensions
```

---

## 🐛 Troubleshooting

### Error: "No file provided"
**Solution**: Ensure form has `enctype="multipart/form-data"`

### Error: "File type not allowed"
**Solution**: Only upload PNG, JPG, JPEG, WEBP, GIF

### Error: "File size exceeds maximum"
**Solution**: Compress image before upload or increase `MAX_FILE_SIZE`

### Images not showing
**Solution**: Check path includes `/static/` prefix
```html
<img src="/static/{{ image_path }}">
```

---

## 📝 Next Steps

Now that photo upload is working, you can integrate it into:

1. **User Book Marketplace** (next feature!)
   - Users upload photos of books they're selling
   - Multiple images per listing
   
2. **User Profile**
   - Profile pictures
   - Cover photos
   
3. **Book Reviews**
   - Users can attach photos to reviews
   
4. **Admin Panel**
   - Upload book covers
   - Upload promotional images

---

## ✨ Features

- ✅ Drag & drop upload
- ✅ Multiple file selection
- ✅ Automatic compression
- ✅ 3 size variants
- ✅ Preview before upload
- ✅ Progress indicators
- ✅ Error handling
- ✅ Responsive design
- ✅ Aspect ratio preservation
- ✅ RGBA to RGB conversion
- ✅ File validation
- ✅ Unique naming
- ✅ Easy deletion

---

## 🎯 Ready for Production!

The upload system is production-ready. When deploying:

1. **Local Storage** (Current)
   - Works for small-medium apps
   - Files in `app/static/uploads/`
   
2. **Cloud Storage** (Recommended for scale)
   - Integrate Cloudinary, AWS S3, or similar
   - Modify `ImageUploader` class
   - Keep same API interface

**Current setup is perfect for development and MVP!**
