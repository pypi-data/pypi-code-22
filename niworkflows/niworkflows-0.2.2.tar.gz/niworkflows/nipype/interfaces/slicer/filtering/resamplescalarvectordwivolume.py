# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-
"""Autogenerated file - DO NOT EDIT
If you spot a bug, please report it on the mailing list and/or change the generator."""

from nipype.interfaces.base import CommandLine, CommandLineInputSpec, SEMLikeCommandLine, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os


class ResampleScalarVectorDWIVolumeInputSpec(CommandLineInputSpec):
    inputVolume = File(position=-2, desc="Input Volume to be resampled", exists=True, argstr="%s")
    outputVolume = traits.Either(traits.Bool, File(), position=-1, hash_files=False, desc="Resampled Volume", argstr="%s")
    Reference = File(desc="Reference Volume (spacing,size,orientation,origin)", exists=True, argstr="--Reference %s")
    transformationFile = File(exists=True, argstr="--transformationFile %s")
    defField = File(desc="File containing the deformation field (3D vector image containing vectors with 3 components)", exists=True, argstr="--defField %s")
    hfieldtype = traits.Enum("displacement", "h-Field", desc="Set if the deformation field is an h-Field", argstr="--hfieldtype %s")
    interpolation = traits.Enum("linear", "nn", "ws", "bs", desc="Sampling algorithm (linear or nn (nearest neighborhoor), ws (WindowedSinc), bs (BSpline) )", argstr="--interpolation %s")
    transform_order = traits.Enum("input-to-output", "output-to-input", desc="Select in what order the transforms are read", argstr="--transform_order %s")
    notbulk = traits.Bool(desc="The transform following the BSpline transform is not set as a bulk transform for the BSpline transform", argstr="--notbulk ")
    spaceChange = traits.Bool(desc="Space Orientation between transform and image is different (RAS/LPS) (warning: if the transform is a Transform Node in Slicer3, do not select)", argstr="--spaceChange ")
    rotation_point = traits.List(desc="Rotation Point in case of rotation around a point (otherwise useless)", argstr="--rotation_point %s")
    centered_transform = traits.Bool(desc="Set the center of the transformation to the center of the input image", argstr="--centered_transform ")
    image_center = traits.Enum("input", "output", desc="Image to use to center the transform (used only if \'Centered Transform\' is selected)", argstr="--image_center %s")
    Inverse_ITK_Transformation = traits.Bool(desc="Inverse the transformation before applying it from output image to input image", argstr="--Inverse_ITK_Transformation ")
    spacing = InputMultiPath(traits.Float, desc="Spacing along each dimension (0 means use input spacing)", sep=",", argstr="--spacing %s")
    size = InputMultiPath(traits.Float, desc="Size along each dimension (0 means use input size)", sep=",", argstr="--size %s")
    origin = traits.List(desc="Origin of the output Image", argstr="--origin %s")
    direction_matrix = InputMultiPath(traits.Float, desc="9 parameters of the direction matrix by rows (ijk to LPS if LPS transform, ijk to RAS if RAS transform)", sep=",", argstr="--direction_matrix %s")
    number_of_thread = traits.Int(desc="Number of thread used to compute the output image", argstr="--number_of_thread %d")
    default_pixel_value = traits.Float(desc="Default pixel value for samples falling outside of the input region", argstr="--default_pixel_value %f")
    window_function = traits.Enum("h", "c", "w", "l", "b", desc="Window Function , h = Hamming , c = Cosine , w = Welch , l = Lanczos , b = Blackman", argstr="--window_function %s")
    spline_order = traits.Int(desc="Spline Order", argstr="--spline_order %d")
    transform_matrix = InputMultiPath(traits.Float, desc="12 parameters of the transform matrix by rows ( --last 3 being translation-- )", sep=",", argstr="--transform_matrix %s")
    transform = traits.Enum("rt", "a", desc="Transform algorithm, rt = Rigid Transform, a = Affine Transform", argstr="--transform %s")


class ResampleScalarVectorDWIVolumeOutputSpec(TraitedSpec):
    outputVolume = File(position=-1, desc="Resampled Volume", exists=True)


class ResampleScalarVectorDWIVolume(SEMLikeCommandLine):
    """title: Resample Scalar/Vector/DWI Volume

category: Filtering

description: This module implements image and vector-image resampling through  the use of itk Transforms.It can also handle diffusion weighted MRI image resampling. "Resampling" is performed in space coordinates, not pixel/grid coordinates. It is quite important to ensure that image spacing is properly set on the images involved. The interpolator is required since the mapping from one space to the other will often require evaluation of the intensity of the image at non-grid positions.

Warning: To resample DWMR Images, use nrrd input and output files.

Warning: Do not use to resample Diffusion Tensor Images, tensors would  not be reoriented

version: 0.1

documentation-url: http://www.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/ResampleScalarVectorDWIVolume

contributor: Francois Budin (UNC)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149. Information on the National Centers for Biomedical Computing can be obtained from http://nihroadmap.nih.gov/bioinformatics

"""

    input_spec = ResampleScalarVectorDWIVolumeInputSpec
    output_spec = ResampleScalarVectorDWIVolumeOutputSpec
    _cmd = "ResampleScalarVectorDWIVolume "
    _outputs_filenames = {'outputVolume': 'outputVolume.nii'}
