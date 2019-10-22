#!/usr/bin/env python
"""
Created on Thur July 18 20:19:14 2019

@authors: Derek Pisner & Ryan Hammonds

"""
try:
    import cPickle as pickle
except ImportError:
    import _pickle as pickle
from pathlib import Path
import nibabel as nib


def test_create_density_map():
    """
    Test for create_density_map functionality
    """
    from pynets.dmri import track

    base_dir = str(Path(__file__).parent/"examples")
    dir_path = base_dir + '/001/dmri'
    dwi_file = dir_path + '/HARDI150.nii.gz'

    dwi_img = nib.load(dwi_file)

    # Load output from test_filter_streamlines: dictionary of streamline info
    streamlines_trk = dir_path + '/tractography/streamlines_Default_csa_10_5mm_curv[2_4_6]_step[0.1_0.2_0.5].trk'
    streamlines = nib.streamlines.load(streamlines_trk).streamlines

    conn_model = 'csa'
    target_samples = 10
    node_size = 5
    curv_thr_list = [2, 4, 6]
    step_list = [0.1, 0.2, 0.5]
    network = 'Default'
    roi = None

    [streams, dir_path, dm_path] = track.create_density_map(dwi_img, dir_path, streamlines, conn_model,
                                                            target_samples, node_size, curv_thr_list, step_list,
                                                            network, roi)

    assert streams is not None
    assert dir_path is not None
    assert dm_path is not None


def test_prep_tissues():
    """
    Test for prep_tissues functionality
    """
    from pynets.dmri import track
    base_dir = str(Path(__file__).parent/"examples")
    dir_path = base_dir + '/003/dmri'
    B0_mask = dir_path + '/sub-003_b0_brain_mask.nii.gz'
    gm_in_dwi = dir_path + '/gm_mask_dmri.nii.gz'
    vent_csf_in_dwi = dir_path + '/csf_mask_dmri.nii.gz'
    wm_in_dwi = dir_path + '/wm_mask_dmri.nii.gz'
    
    for tiss_class in ['act', 'bin', 'cmc', 'wb']:
        tiss_classifier = track.prep_tissues(B0_mask, gm_in_dwi, vent_csf_in_dwi, wm_in_dwi, tiss_class,
                                             cmc_step_size=0.2)
        assert tiss_classifier is not None
        
        
def test_reconstruction():
    """
    Test for reconstruction functionality
    """
    from pynets.dmri import track
    from dipy.core.gradients import gradient_table
    base_dir = str(Path(__file__).parent/"examples")

    dir_path = base_dir + '/003/dmri'
    bvals = dir_path + '/sub-003_dwi.bval'
    bvecs = dir_path + '/sub-003_dwi.bvec'
    gtab = gradient_table(bvals, bvecs)
    dwi_file = dir_path + '/sub-003_dwi.nii.gz'
    wm_in_dwi = dir_path + '/wm_mask_dmri.nii.gz'

    dwi_img = nib.load(dwi_file)
    dwi_data = dwi_img.get_fdata()

    for conn_model in ['csa', 'csd']:
        mod = track.reconstruction(conn_model, gtab, dwi_data, wm_in_dwi)
        assert mod is not None
