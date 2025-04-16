import os
import sys
import logging
from PIL import Image
import io
import cv2
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.image_processing import validate_image, save_uploaded_image, optimize_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_image_processing():
    """Test the image processing functions with the sample image"""
    try:
        sample_path = "../frontend/public/sample.jpg"
        
        with open(sample_path, "rb") as f:
            image_data = f.read()
        
        logger.info(f"Sample image size: {len(image_data)} bytes")
        
        is_valid = validate_image(image_data)
        logger.info(f"Image validation result: {is_valid}")
        
        if not is_valid:
            logger.error("Image validation failed")
            return
        
        saved_path = save_uploaded_image(image_data)
        logger.info(f"Saved image path: {saved_path}")
        
        if not os.path.exists(saved_path):
            logger.error(f"Saved image does not exist at {saved_path}")
            return
        
        optimized_path = optimize_image(saved_path)
        logger.info(f"Optimized image path: {optimized_path}")
        
        if not os.path.exists(optimized_path):
            logger.error(f"Optimized image does not exist at {optimized_path}")
            return
        
        try:
            img = Image.open(optimized_path)
            logger.info(f"Successfully opened optimized image with PIL: {img.format}, {img.size}, {img.mode}")
        except Exception as e:
            logger.error(f"Failed to open optimized image with PIL: {e}")
        
        try:
            img_cv = cv2.imread(optimized_path)
            if img_cv is None:
                logger.error("OpenCV failed to read the optimized image")
            else:
                logger.info(f"Successfully opened optimized image with OpenCV: shape={img_cv.shape}")
        except Exception as e:
            logger.error(f"Failed to open optimized image with OpenCV: {e}")
        
        logger.info("Image processing test completed successfully")
        
    except Exception as e:
        logger.error(f"Error during image processing test: {e}")

if __name__ == "__main__":
    test_image_processing()
