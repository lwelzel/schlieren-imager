import numpy as np
import matplotlib as mpl
from astropy.io import fits
from pathlib import Path
from natsort import natsorted
from PIL import Image
import matplotlib.pyplot as plt
from moviepy.editor import ImageSequenceClip
from tqdm import tqdm

def bmp2fits(directory, name="fits_from_bmp", **kwargs):
    path = Path(directory)
    files = path.rglob("*.bmp")
    files = [f.as_posix() for f in files]
    files = np.array(natsorted(files))

    cube = np.zeros((len(files), *plt.imread(files[0]).shape), dtype=float)
    print(f"Saving reading cube.\tShape: {cube.shape}\tIn memory: {cube.nbytes / 2 ** 20:.0f} MB")
    for i, file in tqdm(enumerate(files),
                        leave=False):
        img = plt.imread(file)
        # TODO: imgs might have channels that are not needed and should be removed
        cube[i] = img

    if len(cube.shape) == 4:
        cube = np.moveaxis(cube, -1, 0)
        hdu = fits.PrimaryHDU(cube[0])
        hdul = fits.HDUList([hdu])
        for i in range(1, cube.shape[0]):
            hdu = fits.ImageHDU(cube[i])
            hdul.append(hdu)
    else:
        hdu = fits.PrimaryHDU(cube)
        hdul = fits.HDUList([hdu])

    hdul.writeto(path / f'{name}.fits', overwrite=True)
    return

def bmp2mp4(directory, name="mp4_from_bmp", fps=10, **kwargs):
    path = Path(directory)
    files = path.rglob("*.bmp")
    files = [f.as_posix() for f in files]
    files = natsorted(files)

    clip = ImageSequenceClip(files, fps=fps, with_mask=True)
    # ImageSequenceClip()
    # my moviepy needed a fix in
    # "...\moviepy\decorators.py", line 118, in use_clip_fps_by_default
    # the line
    # names = inspect.getfullargspec(func).args[1:]
    # needs to be changed to
    # names = inspect.getfullargspec(f).args[1:]
    # issue is known
    # same needs to be done in
    # "...\moviepy\decorators.py", line 79, in wrapper
    clip.write_videofile(directory + f"/{name}.mp4", fps=fps, audio=False)

def do_all_conv(dir):
    bmp2fits(dir)
    # bmp2mp4(dir)

def iter_over_runs(directory="./data"):
    path = Path(directory)
    runs = [
        "candle_1",
        "candle_2",
        "cylinder",
        "flow_down_fast",
        "flow_down_slow",
        "flow_paper",
        "flow_up_fast",
        "flow_up_slow",
        "soldering_iron",
    ]
    for run in tqdm(runs):
        do_all_conv(path / run)


if __name__ == '__main__':
    iter_over_runs()