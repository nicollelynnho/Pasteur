# Pasteur
Automated data processing from tuberculosis growth experiments during an internship at l'Institut Pasteur

Title:
Automated Analysis of Mycobacterial Microcolonies Growth on a Chip

Introduction:
Tuberculosis (TB) is a deadly infectious disease caused by Mycobacterium tuberculosis. Though curable by lengthy multidrug therapy, drug-resistance spreads (PMID:2784885). Existence of non-genetic cell-to-cell heterogenity further exacerbates this problem by making bacilli also phenotypically tolerant to drugs (PMID:27837741). To elucidate the mechanisms of drug tolerance, we study phenotypic heterogeneity by monitoring the growth and behavior of live bacilli inside a microfluidic chip with live microscope imaging. However, this approach produces vast amounts of data that need robust computational strategies to be analyzed and processed more efficiently, which is the purpose of this summer project.

Description:
This project tracks the growth and division of microcolonies of Mycobacterium smegmatis, a TB model. cell_vis.py creates a map of the microfluidic cell microchamber. exp_growth.py organizes the microcolony growth data automatically in Python, and it fit exponential curves to microcolony growth data to calculate the growth rate.
Your description is an extremely important aspect of your project. A well-crafted description allows you to show off your work to other developers as well as potential employers.

Analysis and Results:
View nho_pasteur_poster_resize.pdf for a flow chart of how the technologies work together. 

Conclusions:
Cell Visualization tool reads a folder of data files, maps the chamber, and writes a .csv with file name, cell location, and distance from center. Exponential Bacteria Growth tool reads bacterial movies, estimates exponential fit, and graphs total growth and rate. The Python tools automate and accelerate analysis, and can be applied to other TB research.

