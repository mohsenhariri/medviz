from typing import Any, Dict, List, Optional, Union

import numpy as np


def _metadata_nibabel(image_and_properties) -> Dict[str, Any]:
    """
    Extracts metadata from a NIfTI image using Nibabel.

    Parameters:
    image_and_properties (nib.Nifti1Image): A NIfTI image object.

    Returns:
    Dict[str, Any]: A dictionary containing image metadata.
    """
    try:
        image_info: Dict[str, Any] = {}

        image_data = image_and_properties.get_fdata()
        image_header = image_and_properties.header
        image_obj = image_and_properties.dataobj
        affine = image_and_properties.affine

        slope_obj, intercept_obj = image_obj.slope, getattr(image_obj, "inter", 0)

        is_hu_obj = slope_obj == 1 and intercept_obj <= 0

        dimensions = image_data.shape
        voxel_size = image_header.get_zooms()[:3]

        # Get spatial and temporal units
        spatial_units, temporal_units = image_header.get_xyzt_units()

        # Get slope and intercept for Hounsfield Unit (HU) conversion
        slope, intercept = image_header.get_slope_inter()[:2]

        # Determine if the image is in HU format
        is_hu_format = slope == 1 and intercept <= 0

        # Check if the image is isotropic
        is_isotropic = np.allclose(voxel_size, voxel_size[0])

        # Store the information in the dictionary
        image_info = {
            "dimensions": dimensions,
            "voxel_size": voxel_size,
            "spatial_units": spatial_units,
            "temporal_units": temporal_units,
            "slope": slope,
            "slope_obj": slope_obj,
            "intercept": intercept,
            "intercept_obj": intercept_obj,
            "is_hu_obj": is_hu_obj,
            "is_hu": is_hu_format,
            "is_isotropic": is_isotropic,
        }

        return image_info
    except AttributeError as e:
        raise ValueError(f"An attribute error occurred: {e}")


def _metadata_pydicom(image_and_properties) -> Dict[str, Any]:
    """
    Extracts extended metadata from a DICOM file using pydicom.

    Parameters:
    file_path (str): The file path to the DICOM image.

    Returns:
    Dict[str, Any]: A dictionary containing extended image metadata.
    """
    try:
        # Read the DICOM file
        ds = image_and_properties

        # Extracting basic metadata
        patient_id = getattr(ds, "PatientID", "N/A")
        patient_name = getattr(ds, "PatientName", "N/A")
        study_id = getattr(ds, "StudyID", "N/A")
        study_date = getattr(ds, "StudyDate", "N/A")
        series_number = getattr(ds, "SeriesNumber", "N/A")
        modality = getattr(ds, "Modality", "N/A")
        manufacturer = getattr(ds, "Manufacturer", "N/A")

        # Extracting pixel spacing, slice thickness, image position and orientation if available
        pixel_spacing = getattr(ds, "PixelSpacing", "N/A")
        slice_thickness = getattr(ds, "SliceThickness", "N/A")
        image_position = getattr(ds, "ImagePositionPatient", "N/A")
        image_orientation = getattr(ds, "ImageOrientationPatient", "N/A")

        # Extracting image dimensions
        dimensions = (
            (int(ds.Rows), int(ds.Columns))
            if "Rows" in ds and "Columns" in ds
            else "N/A"
        )

        # Store the information in the dictionary
        image_info = {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "study_id": study_id,
            "study_date": study_date,
            "series_number": series_number,
            "modality": modality,
            "manufacturer": manufacturer,
            "pixel_spacing": pixel_spacing,
            "slice_thickness": slice_thickness,
            "image_position": image_position,
            "image_orientation": image_orientation,
            "dimensions": dimensions,
        }

        return image_info
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the DICOM file: {e}")


def _metadata_sitk(image_and_properties) -> Dict[str, Any]:
    """
    Extracts metadata from an image file using SimpleITK.

    Parameters:
    file_path (str): The file path to the image.

    Returns:
    Dict[str, Any]: A dictionary containing image metadata.
    """
    try:
        # Read the image file
        # image = sitk.ReadImage(file_path)
        image = image_and_properties

        # Extracting metadata
        metadata_keys = image.GetMetaDataKeys()

        # metadata = {key: image.GetMetaData(key) for key in metadata_keys}
        metadata = {}

        # Adding additional information about the image
        metadata["spacing"] = image.GetSpacing()
        metadata["origin"] = image.GetOrigin()
        metadata["direction"] = image.GetDirection()
        metadata["size"] = image.GetSize()
        metadata[
            "number_of_components_per_pixel"
        ] = image.GetNumberOfComponentsPerPixel()

        return metadata
    except RuntimeError as e:
        raise RuntimeError(f"An error occurred while reading the image file: {e}")
