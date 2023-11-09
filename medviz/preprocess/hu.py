import numpy as np
import pydicom

from ..utils import path2loader, path_in, save_path_file


#     return pydicom.tag.Tag(int(group, 16), int(element, 16))
def convert_tag(tag_str):
    if "|" in tag_str:
        group, element = tag_str.split("|")
        return pydicom.tag.Tag(int(group, 16), int(element, 16))
    else:
        return None  # Return None for strings that don't contain "|"


def get_hu(file_path, save_path=None):
    file_path = path_in(file_path)

    dicom_file = pydicom.dcmread(file_path)
    pixel_array = dicom_file.pixel_array

    rescale_slope = dicom_file.RescaleSlope
    rescale_intercept = dicom_file.RescaleIntercept

    hu_pixel_array = pixel_array * rescale_slope + rescale_intercept
    hu_pixel_array = hu_pixel_array.astype(np.int16)
    dicom_file.PixelData = hu_pixel_array.tobytes()
    if save_path is not None:
        name = f"{file_path.stem}_hu"
        save_path = save_path + "/" + name

        save_path = save_path_file(save_path, suffix=".dcm")
        dicom_file.save_as(save_path)


# def get_hu(path):
#     image = path2loader(path)
#     image_and_properties, reader, image_and_properties_itk = image

#     if reader == "pydicom":
#         ds = image_and_properties


#     else:
#         image = image_and_properties_itk

#         metadata_keys = image.GetMetaDataKeys()

#         metadata = {
#         pydicom.datadict.keyword_for_tag(convert_tag(key)): image.GetMetaData(key)
#         for key in metadata_keys
#         if convert_tag(key) is not None
#         and pydicom.datadict.keyword_for_tag(
#             convert_tag(key)
#         )  # Only include known tags with "|"
#     }


#         rescale_intercept = (
#             float(image.GetMetaData("0028|1052"))
#             if "0028|1052" in metadata_keys
#             else metadata.get("scl_inter", None)
#         )

#         rescale_slope = (
#             float(image.GetMetaData("0028|1053"))
#             if "0028|1053" in metadata_keys
#             else metadata.get("scl_slope", None)
#         )


#         metadata["itk_HU"] = rescale_intercept == -1024 and rescale_slope == 1

#         return metadata["itk_HU"]
