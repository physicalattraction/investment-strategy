Investment Strategy
===================

This repository contains a method to calculate the ideal portfolio position taken from a list of stocks, their current value and their expected values. It takes risk spreading into account by buying all stocks relative to their respective upside, and by capping the position in any single stock.

# Usage

General remarks:
- Make sure you're using Python 3.6 or up.
- Execute all scripts from the `src` directory.
- For all scripts, run it with flag `--help` to get more information about the usage and input arguments.

## Rebalance a portfolio
- Make sure you have a portfolio file in the correct csv format in the directory `portfolios`. Check out `demo.csv` for an example input file.
- Run the following script:
    ```shell script
    python -m calculator --input demo.csv --output ideal.csv
    ```
    Where you can of course specify the input and output filenames accordingly.
- The rebalanced portfolio is exported as a csv in the specified output location.

## Run a simulation
A simulation makes use of the strategy employed in Calculator, and repeats the scenario under a number of steps under which the value of stocks change.

- Write a `start.csv` file with which you want to start the scenario.
- Place it in the directory of the simulation: `simulations/<scenario>`
- Run the following script:
  ```shell script
  python -m simulator --scenario up_and_down --steps 10
  ```
- Find the results in the directory of the simulation. Per step, we have the portfolio under investigation after rebalancing and after updating of the reality, and for reference the initial portfolio without any rebalancing under the same market fluctuations.