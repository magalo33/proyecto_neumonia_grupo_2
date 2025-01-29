import pytest
import numpy as np
from app.read_img import read_dicom_file, read_jpg_file, read_image_file
from unittest.mock import patch, MagicMock
import os


@pytest.fixture
def sample_dicom_path(tmp_path):
    """Crea un archivo DICOM de prueba válido."""
    dcm_path = tmp_path / "test.dcm"

    import pydicom
    from pydicom.dataset import Dataset, FileDataset
    from pydicom.uid import ExplicitVRLittleEndian

    meta = pydicom.dataset.FileMetaDataset()
    meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset(dcm_path, {}, file_meta=meta, preamble=b"\0" * 128)
    ds.PixelData = np.random.randint(0, 256, (128, 128), dtype=np.uint8).tobytes()
    ds.Rows = 128
    ds.Columns = 128
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1  # Añadir SamplesPerPixel
    ds.PixelRepresentation = 0  # Añadir PixelRepresentation (0 para datos sin signo, 1 para datos con signo)

    ds.save_as(dcm_path)
    return str(dcm_path)




@pytest.fixture
def sample_jpg_path(tmp_path):
    """Crea una imagen JPG de prueba."""
    jpg_path = tmp_path / "test.jpg"

    import cv2

    # Crear una imagen en escala de grises de 128x128
    img = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    cv2.imwrite(str(jpg_path), img)

    return str(jpg_path)


def test_read_dicom_file_valid(sample_dicom_path):
    """Verifica que se pueda leer correctamente un archivo DICOM válido."""

    img_rgb, img_pil = read_dicom_file(sample_dicom_path)
    
    assert img_rgb is not None
    assert img_pil is not None
    assert isinstance(img_rgb, np.ndarray)
    assert img_rgb.shape[-1] == 3  # Debe ser una imagen RGB


def test_read_dicom_file_invalid():
    """Verifica que leer un archivo DICOM inexistente retorne (None, None)."""
    img_rgb, img_pil = read_dicom_file("archivo_inexistente.dcm")
    
    assert img_rgb is None
    assert img_pil is None


def test_read_jpg_file_valid(sample_jpg_path):
    """Verifica que se pueda leer correctamente un archivo JPG válido."""
    img_gray, img_pil = read_jpg_file(sample_jpg_path)

    assert img_gray is not None
    assert img_pil is not None
    assert isinstance(img_gray, np.ndarray)


def test_read_jpg_file_invalid():
    """Verifica que leer un archivo JPG inexistente retorne (None, None)."""
    img_gray, img_pil = read_jpg_file("archivo_inexistente.jpg")
    
    assert img_gray is None
    assert img_pil is None


def test_read_image_file_dicom(sample_dicom_path):
    """Verifica que read_image_file detecte un DICOM correctamente."""
    sample_dicom_path = "Modelo de Neumonia .h5-20250126/DICOM/normal (2).dcm"
    img, img_pil = read_image_file(sample_dicom_path)

    assert img is not None
    assert img_pil is not None


def test_read_image_file_jpg(sample_jpg_path):
    """Verifica que read_image_file detecte un JPG correctamente."""
    img, img_pil = read_image_file(sample_jpg_path)

    assert img is not None
    assert img_pil is not None


def test_read_image_file_invalid():
    """Verifica que read_image_file maneje archivos desconocidos."""
    img, img_pil = read_image_file("archivo_desconocido.xyz")

    assert img is None
    assert img_pil is None


def test_read_dicom_mock():
    """Prueba `read_dicom_file` con un mock de pydicom."""
    
    with patch("pydicom.dcmread") as mock_dcmread, patch("os.path.exists", return_value=True):
        mock_dicom = MagicMock()
        mock_dicom.pixel_array = np.random.randint(0, 256, (128, 128), dtype=np.uint8)

        # Simula un archivo DICOM con atributos mínimos necesarios
        mock_dicom.Rows = 128
        mock_dicom.Columns = 128
        mock_dicom.BitsAllocated = 8
        mock_dicom.BitsStored = 8
        mock_dicom.HighBit = 7
        mock_dicom.PhotometricInterpretation = "MONOCHROME2"

        # Se añade un objeto file_meta simulado
        mock_dicom.file_meta = MagicMock()

        mock_dcmread.return_value = mock_dicom  # Se devuelve el objeto simulado

        img, img_pil = read_dicom_file("fake.dcm")

        assert img is not None
        assert img_pil is not None
        assert isinstance(img, np.ndarray)


def test_read_jpg_mock():
    """Prueba `read_jpg_file` con un mock de `cv2.imread`."""
    with patch("cv2.imread", return_value=np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)), \
         patch("os.path.exists", return_value=True):
        img, img_pil = read_jpg_file("fake.jpg")

        assert img is not None
        assert img_pil is not None
        assert isinstance(img, np.ndarray)
