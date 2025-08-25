⚙️ Main Features

1. Data File Reading

The user selects a .txt file containing the experimental results. The script automatically detects the ***DATA*** section and extracts pairs of values: Magnetic field (Oe), Magnetic moment (emu). 

2. Mass Normalization (optional)

The user can normalize the data by the sample mass (emu/g).
If selected, the program requests the sample mass in grams and adjusts the values accordingly.

3. Curve Centering

The curve is centered at the origin to remove experimental offsets.

4. Initial Curve Plotting
Displays the hysteresis curve with centered axes for better visualization.

5. Linear Fit (Antiferromagnetic Contribution)

The user chooses how many points to use for the linear fit.
Points can be selected from either the positive or negative field region.
A linear regression is performed to represent the antiferromagnetic contribution.

6. Magnetic Contribution Separation

The linear fit is subtracted from the experimental curve.
Three curves are displayed: Experimental hysteresis curve (total), Linear fit (antiferromagnetic contribution), Ferromagnetic contribution (residual curve).

7. Zoom Around the Origin (optional)

The user can zoom into the origin region to analyze coercivity and remanent magnetization.

8. Export Results

Graphs: saved as .png with 300 dpi resolution.
Data: exported as .txt containing: Magnetic Field | Experimental Curve | Linear Fit | Ferromagnetic Contribution

🖥️ Graphical Interface:

The program launches a simple GUI window with the following buttons:
Read File → Selects the experimental data file.
Start Fitting → Starts the workflow (normalization, centering, linear fit, and plotting).


🚀 How to Use:

Click Read File and select the experimental data file.
Click Start Fitting.
Choose whether to normalize by mass.
Enter the number of points for the linear fit.
Visualize the generated plots.
Choose whether to apply zoom at the origin.
Export plots and processed data.
