# RECAST3D

REConstruction of Arbitrary Slices in Tomography

![](https://raw.githubusercontent.com/cicwi/RECAST3D/develop/docs/preview_usage.gif)

This project contains a full-stack implementation of a tomographic reconstruction and visualization pipeline.

RECAST3D is visualization software for tomographic imaging based on on-demand reconstruction of arbitrary slices, and is built for use in a distributed,
real-time, and online reconstruction pipeline.

The repository also contains two support libraries, *TomoPackets* and *SliceRecon*.

The TomoPackets library defines a protocol for sending messages between the different
components (scanners, reconstruction nodes, visualization workstations) for
real-time tomographic reconstruction and we encourage its use also outside of RECAST3D.

SliceRecon contains efficient implementations for reconstructing
arbitrarily oriented slices through a 3D volume. It defines servers that are
able to communicate to data sources (using TomoPackets) and visualization
software (such as, but not exclusively, RECAST3D).

## Useful Link
- [Recast3D Home Page]
- [Recast3D official github repo]
- [Installation documentation]

# Installation and Deploy
1. Recastd3D is deployed in CLFENGSERV7
-	ip address: 130.246.71.84
-	user account: swdev
-	Hardware in CLFENGSERV7
    - CPU: Intel(R) Core(TM) i7-6800K CPU @ 3.40GHz
    - Memory: 64 GB
    - GPU: Nvidia GeForce RTX-3080, 12 GB
    - Motherboard: ROG STRIX X99 Gaming
-	Operation System: Ubuntu 20.04

2. Before the deploy of Recast3D, we need to install Nvidia driver 
-	Installation Tutorails: [Ubuntu Linux Install Nvidia Driver (Latest Proprietary Driver)](https://www.cyberciti.biz/faq/ubuntu-linux-install-nvidia-driver-latest-proprietary-driver/)
-	Please install NVIDIA RTX / QUADRO DESKTOP AND NOTEBOOK DRIVER RELEASE 515 or higher version

3. Recast3D installation
-	We can install Recast3D by following The best way to install Recast3D is via using anaconda, thus we need to install anaconda environment at first
    - [Installing on Linux — conda 4.13.0.post12+892c22bf documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
-	Recast3D requires python version 3.6 or 3.7, thus we need to upgrade/downgrade python version
    - ``conda install python=3.7``
-	Then we can use anaconda to install Recast3D
    - `conda install -c cicwi -c astra-toolbox/label/dev recast3d tomopackets slicerecon`
-	If conda doesn’t work, please following [Installation documentation] to install
-	Requirement python library:
    - swmr_tools

## Run Recast3D
1. Start recast3d
    - `recast3d `
2. Start slicecon
    - `slicerecon_server --slice-size 1024 –-tilt`
    - All the configurable parameters:
        -	`--slice-size`
        -	`--preview-size`
        -	`--group-size`
        -	`--filter-cores`
        -	`--plugin`
        -	`--tilt`
        -	`--pyplugin`
        -	`--recast-host`
        -	`--reqrep`
        -	`--gaussian`
        -	`--phase`
        -	`--bench`
        -	`--filter`
        -	`--pixelsiz`
        -	`--lambda`
        -	`--delta`
        -	`--beta`
        -	`--distance`
3. Reconstruct .nxs file
    - `python ~/source/repos/RECAST3D/examples/adapters/diad_swmr.py ~/source/repos/TomoData/h5Data/mouse_tomo_flat_shifted.nxs --sample 1`
    - `diad_swmr.py is the adapter file we used to reconstruct, .nxs is the object.
    - You can downsample .nxs file with parameter **–sample**, it will reduce resolution & images, and speed up reconstruction time

## Authors

RECAST3D is developed by the Computational Imaging group at CWI. Original author:

- Jan-Willem Buurlage (@jwbuurlage)

Contributions by:

- Holger Kohr (@kohr-h)
- Willem Jan Palenstijn (@wjp)
- Allard Hendriksen (@ahendriksen)
- Adriaan Graas (@adriaangraas)
- Daan Pelt (@dmpelt)

## Contributing

We welcome contributions. Please submit pull requests against the develop
branch.

If you have any issues, questions, or remarks, then please open an issue on
GitHub.

## Publications using RECAST3D

| Article      |  Code  |
|------------------|--------|
| *Real-time reconstruction and visualisation ... at TOMCAT*. Sci.Rep. [DOI](https://doi.org/10.1038/s41598-019-54647-4) |  |
| *Real-time quasi-3D tomographic reconstruction*. MST. [DOI](https://doi.org/10.1088/1361-6501/aab754)  | [<img src="https://github.com/favicon.ico" width="24">](https://github.com/cicwi/RECAST3D) |

## Please cite us

If you have used RECAST3D for a scientific publication, we would appreciate
citations to the following paper:

[Real-time quasi-3D tomographic reconstruction. JW Buurlage, H Kohr, WJ
Palenstijn, KJ Batenburg. Measurement Science and Technology
(2018)](https://doi.org/10.1088/1361-6501/aab754)

## License

This project is licensed under the GPL. See `LICENSE.md` for details.

[TomoPackets]: https://www.github.com/cicwi/TomoPackets
[SliceRecon]: https://www.github.com/cicwi/SliceRecon
[installation documentation]: https://cicwi.github.io/RECAST3D/installation_instructions/
[Recast3D Home Page]: https://cicwi.github.io/RECAST3D/installation_instructions/
[Recast3D official github repo]: https://github.com/cicwi/RECAST3D
