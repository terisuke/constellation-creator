import os
import sys
import logging
from PIL import Image
import io
import cv2
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.image_processing import validate_image, save_uploaded_image, optimize_image
from app.core.star_detection import detect_stars
from app.core.constellation import draw_constellation_lines

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
            stars = detect_stars(optimized_path)
            logger.info(f"Detected {len(stars)} stars")
            
            constellation_points = []
            for i in range(0, len(stars), 5):
                cluster = stars[i:i+5]
                if len(cluster) >= 3:
                    points = [(star["x"], star["y"]) for star in cluster]
                    constellation_points.append(points)
            
            logger.info(f"Created {len(constellation_points)} constellation clusters")
            
            if constellation_points:
                constellation_path = draw_constellation_lines(optimized_path, constellation_points)
                logger.info(f"Generated constellation image: {constellation_path}")
                logger.info(f"Image exists: {os.path.exists(constellation_path)}")
            else:
                logger.info("No constellation clusters created")
        except Exception as e:
            logger.error(f"Error during star detection or constellation generation: {e}")
        
        logger.info("Image processing test completed successfully")
        
    except Exception as e:
        logger.error(f"Error during image processing test: {e}")

if __name__ == "__main__":
    test_image_processing()
