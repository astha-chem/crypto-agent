#!/bin/bash

# Setup crypto-agent environment
echo "Setting up crypto-agent environment..."

# Create/update conda environment
~/miniconda3/bin/conda env create -f environment.yml --force

# Activate environment and install playwright browsers
source ~/miniconda3/bin/activate crypto-agent
playwright install

echo "Environment setup complete!"
echo "To activate: source ~/miniconda3/bin/activate crypto-agent"