# Molecular-Orbital-Diagram-Generator
                               ENERGY ↑
                                 |
                antibonding     |          antibonding
                   σ*  π*  σ*   |     σ*  π*  σ*
                     \   |   /  |  \   |   /
                      \  |  /   |   \  |  /
                       \ | /    |    \ | /
 -----------------------  M O L E C U L E  -----------------------
                       / | \    |    / | \
                      /  |  \   |   /  |  \
                 bonding  σ  π   |   π  σ   bonding
                                 |
                  ← A T O M  A        A T O M  B →
                     (1s, 2s, 2p)      (1s, 2s, 2p)

**A computational chemistry project for visualizing MO formation,
electron filling, bond order, and magnetic behavior.**


## Project Overview

The **Molecular Orbital Diagram Generator** is a computational chemistry project designed to visually represent how molecular bonding emerges from the interaction of atomic orbitals using Molecular Orbital Theory (MOT). The program automatically constructs accurate MO diagrams for homonuclear diatomic molecules, calculates bond order, predicts magnetic properties, and displays electron occupation across bonding and antibonding orbitals.

The tool supports:

* Generating an MO diagram for a **specific molecule**.
* Generating MO diagrams for **all supported molecules**.

The system follows proper MOT rules, including correct electron filling, energy ordering exceptions (such as O₂/F₂), and clean diagram visualization using Matplotlib.

---

## Features

* Generate complete Molecular Orbital diagrams for supported diatomic molecules
* Algorithmic electron filling based on Aufbau principle and Hund’s rule
* Computes:

  * Bond order
  * Magnetic behavior (paramagnetic/diamagnetic)
  * Electron distribution across orbitals
* Uses separate MO energy ordering for lighter (B₂–N₂) and heavier (O₂–F₂) molecules
* Batch-generation mode for producing diagrams for all molecules
* Cleanly structured Python code with comments
* Matplotlib-based visual diagrams
* User-friendly input flow

---

## Technologies / Tools Used

* Python 3.x
* Matplotlib
* Object-Oriented Programming
* Computational Chemistry Concepts (MOT, electron configuration, molecular bonding)

---

## Steps to Install and Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Molecular-Orbital-Diagram-Generator.git
cd Molecular-Orbital-Diagram-Generator
```

### 2. Install Dependencies

```bash
pip install matplotlib
```

### 3. Run the Program

```bash
python main.py
```

### 4. Choose an Option Inside the Program

* Enter a molecule (for example: `O2`, `N2`, `B2`, `F2`)
* OR select the option to generate diagrams for all molecules

---

## Instructions for Testing

1. Run the script using `python main.py`.
2. When prompted, enter any supported molecule name or choose batch generation.
3. The program will:

   * Draw the MO diagram
   * Calculate bond order
   * Determine magnetic properties
   * Display electron filling
   * Save diagrams as PNG files
4. Ensure that:

   * O₂ appears **paramagnetic**
   * N₂ shows **bond order 3**
   * F₂ uses correct MO ordering for heavier diatomic molecules
