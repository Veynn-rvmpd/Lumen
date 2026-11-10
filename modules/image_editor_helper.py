"""
Image Manipulation & Web Asset Optimization Helper.
Provides headless routines for resizing, watermarking, WebP compression,
and format conversions via Pillow without graphic interface dependencies.
"""

import os
from typing import Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageOps


def inspect_image(sourcePath: str) -> Dict[str, Any]:
    """
    Reads image dimensions, color profile, and file size metrics.
    """
    if not os.path.exists(sourcePath):
        return {"status": "[ERROR]", "message": f"File not found: {sourcePath}"}

    fileSizeBytes = os.path.getsize(sourcePath)
    with Image.open(sourcePath) as targetImage:
        return {
            "status": "[OK]",
            "filePath": sourcePath,
            "format": targetImage.format,
            "mode": targetImage.mode,
            "width": targetImage.width,
            "height": targetImage.height,
            "aspectRatio": round(targetImage.width / max(targetImage.height, 1), 3),
            "fileSizeKb": round(fileSizeBytes / 1024, 2)
        }


def crop_image(
    sourcePath: str,
    outputPath: str,
    boxCoordinates: Tuple[int, int, int, int]
) -> Dict[str, Any]:
    """
    Crops image to (left, upper, right, lower) bounding coordinates.
    """
    try:
        with Image.open(sourcePath) as targetImage:
            cropped = targetImage.crop(boxCoordinates)
            cropped.save(outputPath)
        return {
            "status": "[OK]",
            "action": "crop",
            "outputPath": outputPath,
            "dimensions": f"{cropped.width}x{cropped.height}"
        }
    except Exception as processError:
        return {"status": "[ERROR]", "message": str(processError)}


def add_text_watermark(
    sourcePath: str,
    outputPath: str,
    watermarkText: str = "CONFIDENTIAL",
    opacityPercentage: int = 40,
    position: str = "bottom_right"
) -> Dict[str, Any]:
    """
    Overlays a subtle monochrome text watermark on an RGBA alpha buffer.
    """
    try:
        with Image.open(sourcePath).convert("RGBA") as baseImage:
            watermarkOverlay = Image.new("RGBA", baseImage.size, (255, 255, 255, 0))
            drawContext = ImageDraw.Draw(watermarkOverlay)

            # Use default raster font when specific TTF is absent
            fontInstance = ImageFont.load_default()
            boundingBox = drawContext.textbbox((0, 0), watermarkText, font=fontInstance)
            textWidth = boundingBox[2] - boundingBox[0]
            textHeight = boundingBox[3] - boundingBox[1]

            margin = 20
            if position == "bottom_right":
                xCoord = baseImage.width - textWidth - margin
                yCoord = baseImage.height - textHeight - margin
            elif position == "center":
                xCoord = (baseImage.width - textWidth) // 2
                yCoord = (baseImage.height - textHeight) // 2
            else:
                xCoord = margin
                yCoord = margin

            alphaChannel = int((opacityPercentage / 100.0) * 255)
            drawContext.text((xCoord, yCoord), watermarkText, fill=(255, 255, 255, alphaChannel), font=fontInstance)

            blendedImage = Image.alpha_composite(baseImage, watermarkOverlay)
            outputFormat = "PNG" if outputPath.lower().endswith(".png") else "JPEG"
            if outputFormat == "JPEG":
                blendedImage = blendedImage.convert("RGB")

            blendedImage.save(outputPath, outputFormat)

        return {
            "status": "[OK]",
            "action": "watermark",
            "outputPath": outputPath,
            "text": watermarkText
        }
    except Exception as watermarkError:
        return {"status": "[ERROR]", "message": str(watermarkError)}


def compress_for_web(
    sourcePath: str,
    outputPath: str,
    maxDimension: int = 1920,
    qualityLevel: int = 82,
    outputFormat: str = "WEBP"
) -> Dict[str, Any]:
    """
    Downsamples oversized dimensions and exports with lossy WebP/JPEG compression
    to minimize network payload while preserving perceptual clarity.
    """
    try:
        with Image.open(sourcePath) as targetImage:
            # Auto-orient based on EXIF tags before resizing
            correctedImage = ImageOps.exif_transpose(targetImage)
            width, height = correctedImage.size

            if max(width, height) > maxDimension:
                scalingFactor = maxDimension / max(width, height)
                newWidth = int(width * scalingFactor)
                newHeight = int(height * scalingFactor)
                correctedImage = correctedImage.resize((newWidth, newHeight), Image.Resampling.LANCZOS)

            normalizedFormat = outputFormat.upper()
            if normalizedFormat in ["JPEG", "JPG"] and correctedImage.mode != "RGB":
                correctedImage = correctedImage.convert("RGB")

            correctedImage.save(outputPath, normalizedFormat, quality=qualityLevel, optimize=True)

        originalBytes = os.path.getsize(sourcePath)
        compressedBytes = os.path.getsize(outputPath)
        savedRatio = round((1 - (compressedBytes / max(originalBytes, 1))) * 100, 1)

        return {
            "status": "[OK]",
            "action": "web_compress",
            "originalSizeKb": round(originalBytes / 1024, 1),
            "compressedSizeKb": round(compressedBytes / 1024, 1),
            "spaceSavedPercent": savedRatio,
            "format": normalizedFormat,
            "outputPath": outputPath
        }
    except Exception as compressError:
        return {"status": "[ERROR]", "message": str(compressError)}


def convert_format(
    sourcePath: str,
    outputPath: str,
    targetFormat: str = "JPEG"
) -> Dict[str, Any]:
    """
    Converts between raster formats (PNG, JPEG, WEBP, BMP).
    """
    try:
        with Image.open(sourcePath) as targetImage:
            normalizedFormat = targetFormat.upper()
            if normalizedFormat in ["JPEG", "JPG"] and targetImage.mode in ("RGBA", "P"):
                targetImage = targetImage.convert("RGB")
            targetImage.save(outputPath, normalizedFormat)

        return {
            "status": "[OK]",
            "action": "convert_format",
            "targetFormat": normalizedFormat,
            "outputPath": outputPath
        }
    except Exception as convertError:
        return {"status": "[ERROR]", "message": str(convertError)}
